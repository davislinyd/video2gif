---
name: video2gif
description: Convert MP4 video files to high-quality GIF files using ffmpeg's palette workflow with automatic gifsicle optimization. Can configure FPS, width, colors, duration, loop, and optimization settings.
---

# video2gif

Use this skill to convert MP4 video files to high-quality GIF images using ffmpeg's two-pass palette generation workflow and automatic gifsicle optimization (if gifsicle is available).

## Usage

When the user asks to convert an MP4 video (or any compatible video) to a GIF, you can execute the Python script located in this skill's `scripts/` directory.

### Execution

Run the script using Python 3:

```bash
python3 [SKILL_DIR]/scripts/video2gif.py <input_video_path> [output_gif_path] [options]
```

### Parameters

- `input`: (Required) Path to the input video file (e.g. `.mp4`).
- `output`: (Optional) Path to the output GIF file. If omitted, defaults to the input filename with a `.gif` extension.

### Options

- `--fps <int>`: GIF frame rate (default: `12`).
- `--width <int>`: Output width in pixels. Height will scale automatically to keep the aspect ratio.
- `--start <float>`: Start time in seconds.
- `--duration <float>`: Maximum clip duration in seconds.
- `--colors <int>`: Number of colors in the generated palette (`2` to `256`, default: `256`).
- `--once`: Generate a non-looping GIF (default loops endlessly).
- `-y`, `--overwrite`: Overwrite the destination file if it exists.
- `--no-optimize`: Disable automatic gifsicle optimization (optimization is enabled by default if gifsicle is found in PATH).
