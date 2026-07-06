#!/usr/bin/env python3
"""Convert an MP4 video to a GIF with ffmpeg's palette workflow."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive number")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert an MP4 video to a GIF using ffmpeg.",
    )
    parser.add_argument("input", type=Path, help="Input MP4 file")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="Output GIF file. Defaults to the input file name with .gif.",
    )
    parser.add_argument(
        "--fps",
        type=positive_int,
        default=12,
        help="GIF frame rate. Default: 12",
    )
    parser.add_argument(
        "--width",
        type=positive_int,
        help="Output width in pixels; height keeps aspect ratio. Defaults to original width.",
    )
    parser.add_argument(
        "--start",
        type=positive_float,
        help="Start time in seconds.",
    )
    parser.add_argument(
        "--duration",
        type=positive_float,
        help="Maximum clip duration in seconds.",
    )
    parser.add_argument(
        "--colors",
        type=positive_int,
        default=256,
        help="Palette color count from 2 to 256. Default: 256",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Do not loop the GIF. Default is endless loop.",
    )
    parser.add_argument(
        "-y",
        "--overwrite",
        action="store_true",
        help="Overwrite the output file if it exists.",
    )
    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="Disable gifsicle optimization (enabled by default if gifsicle is available).",
    )
    return parser


def validate_args(args: argparse.Namespace) -> tuple[Path, Path]:
    input_path = args.input.expanduser().resolve()
    output_path = (
        args.output.expanduser().resolve()
        if args.output
        else input_path.with_suffix(".gif")
    )

    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required but was not found in PATH.")

    if not input_path.exists():
        raise SystemExit(f"Input file does not exist: {input_path}")

    if input_path == output_path:
        raise SystemExit("Input and output paths must be different.")

    if args.colors < 2 or args.colors > 256:
        raise SystemExit("--colors must be between 2 and 256.")

    if output_path.exists() and not args.overwrite:
        raise SystemExit(
            f"Output file already exists: {output_path}\n"
            "Use --overwrite to replace it."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    return input_path, output_path


def convert(args: argparse.Namespace) -> int:
    input_path, output_path = validate_args(args)

    video_filters = [f"fps={args.fps}"]
    if args.width is not None:
        video_filters.append(f"scale={args.width}:-1:flags=lanczos")
    filter_complex = (
        f"[0:v]{','.join(video_filters)},split[s0][s1];"
        f"[s0]palettegen=max_colors={args.colors}:stats_mode=diff[p];"
        "[s1][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle"
    )

    command = ["ffmpeg"]
    if args.overwrite:
        command.append("-y")
    else:
        command.append("-n")
    if args.start is not None:
        command += ["-ss", str(args.start)]
    command += ["-i", str(input_path)]
    if args.duration is not None:
        command += ["-t", str(args.duration)]
    command += [
        "-filter_complex",
        filter_complex,
        "-loop",
        "-1" if args.once else "0",
        str(output_path),
    ]

    print("Running:", " ".join(command), flush=True)
    completed = subprocess.run(command, check=False)
    if completed.returncode == 0:
        print(f"Created: {output_path}")
        if not args.no_optimize:
            gifsicle_path = shutil.which("gifsicle")
            if gifsicle_path:
                print("Optimizing with gifsicle...", flush=True)
                opt_command = ["gifsicle", "-b", "-O3", str(output_path)]
                opt_completed = subprocess.run(opt_command, check=False)
                if opt_completed.returncode == 0:
                    print("Optimization complete.")
                else:
                    print("Warning: gifsicle optimization failed.")
            else:
                print("Notice: gifsicle not found in PATH. Install gifsicle for better GIF compression.", flush=True)
    return completed.returncode


def main() -> int:
    parser = build_parser()
    return convert(parser.parse_args())


if __name__ == "__main__":
    sys.exit(main())
