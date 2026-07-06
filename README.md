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

### One-liner Installation (Direct from GitHub)

You can copy and run this command directly in your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/davislinyd/video2gif/main/install.sh | bash
```

### Manual Installation (From Local Repository)

If you have already cloned the repository:

```bash
chmod +x install.sh
./install.sh
```

### Supported OS
- **macOS** (Requires Homebrew)
- **Linux** (Supports `apt-get`, `dnf`, `yum`, and `pacman`)

---

## Agent Integration

This tool is automatically registered to the default directories of major AI coding agents.

### 1. Antigravity (agy)
The installer script registers this as a global skill at `~/.gemini/antigravity-cli/skills/video2gif`. You can trigger the skill directly in Antigravity chat using `/video2gif` or simply describing what you want to convert.

### 2. Claude Code
The installer creates a custom slash command at `~/.claude/commands/video2gif.md`.
- You can now execute `/video2gif` inside the Claude Code CLI.
- Claude Code will automatically run the underlying CLI command with correct arguments.

### 3. Codex / Agents
The installer registers the skill globally at both `~/.agents/skills/video2gif` and `~/.codex/skills/video2gif` for backward compatibility. This allows Codex to discover it during task planning.

### 4. General Terminal CLI
A wrapper script is installed at `~/.local/bin/video2gif`. Make sure to add this directory to your `PATH` (typically in `~/.bashrc` or `~/.zshrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```
Once configured, you or any coding agent can run it natively:
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
