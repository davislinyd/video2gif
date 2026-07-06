# video2gif

Convert video files (such as `.mp4`, `.mov`, etc.) to high-quality GIF images using `ffmpeg`'s two-pass palette generation workflow, with automatic `gifsicle` optimization.

This project is packaged as a **Global Skill / CLI Tool** that supports direct usage by users, as well as seamless integration with AI coding agents like **Claude Code, Codex, and Antigravity (agy)**.

## Features

- **High-Quality output**: Uses ffmpeg's `palettegen` and `paletteuse` filters with Lanczos scaling and Bayer dithering to output visually stunning GIFs.
- **Auto Optimization**: Automatically runs `gifsicle -O3` after conversion to shrink GIF file sizes if `gifsicle` is available.
- **Safe Fallback**: If `gifsicle` is missing, the tool successfully falls back to standard output and alerts you to install it, rather than failing.
- **Comprehensive Options**: Easily adjust width (keeps aspect ratio), FPS, start time, duration, color palette size, loop count, and overwrite behavior.

## Installation

We provide a universal installer script that automatically installs system dependencies (`ffmpeg` and `gifsicle`) and registers the tool for system terminal, Antigravity, Claude, and Codex.

To install, simply run:

```bash
chmod +x install.sh
./install.sh
```

### Supported OS
- **macOS** (Requires Homebrew)
- **Linux** (Supports `apt-get`, `dnf`, `yum`, and `pacman`)

---

## Agent Integration

### 1. Antigravity (agy)
The installer script automatically copies [SKILL.md](file:///Users/lindav/git/video2gif/SKILL.md) and the conversion script into the global Antigravity skills directory (`~/.gemini/antigravity-cli/skills/video2gif`). Once installed, you can trigger this skill directly in Antigravity chat.

### 2. Claude / Codex / General Terminal
The installer sets up a wrapper binary in `~/.local/bin/video2gif` pointing to the script. Make sure `~/.local/bin` is in your terminal's `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```
Once configured, you or any coding agent (like Claude Code) can invoke it natively:
```bash
video2gif input.mov output.gif --width 480 --fps 10
```

---

## Usage

```bash
video2gif <input_video_path> [output_gif_path] [options]
```

### Parameters
- `input`: (Required) Path to the input video file.
- `output`: (Optional) Path to the output GIF file. If omitted, defaults to the input filename with a `.gif` extension.

### Options
- `--fps <int>`: GIF frame rate (default: `12`).
- `--width <int>`: Output width in pixels; height will scale automatically to keep the aspect ratio.
- `--start <float>`: Start time in seconds.
- `--duration <float>`: Maximum clip duration in seconds.
- `--colors <int>`: Palette color count from `2` to `256` (default: `256`).
- `--once`: Prevent the GIF from looping (default loops endlessly).
- `-y`, `--overwrite`: Overwrite the destination file if it exists.
- `--no-optimize`: Disable automatic `gifsicle` optimization.

### Examples

1. **Basic Conversion**
   ```bash
   video2gif input.mp4
   ```

2. **Resize and Lower Frame Rate (recommended for smaller files)**
   ```bash
   video2gif input.mov output.gif --width 480 --fps 8 -y
   ```

3. **Clip a 5-second segment starting from 10 seconds**
   ```bash
   video2gif input.mp4 clip.gif --start 10 --duration 5 -y
   ```
