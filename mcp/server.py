import argparse
import sys
from pathlib import Path

# Add repo root to PATH to allow importing scripts.video2gif
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from scripts.video2gif import convert as run_convert

class FakeArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def execute_conversion(
    input_path: str,
    output_path: str = None,
    fps: int = 12,
    width: int = None,
    start: float = None,
    duration: float = None,
    colors: int = 256,
    once: bool = False,
    overwrite: bool = False,
    no_optimize: bool = False
) -> tuple[int, str]:
    args = FakeArgs(
        input=Path(input_path),
        output=Path(output_path) if output_path else None,
        fps=fps,
        width=width,
        start=start,
        duration=duration,
        colors=colors,
        once=once,
        overwrite=overwrite,
        no_optimize=no_optimize
    )
    
    try:
        exit_code = run_convert(args)
        if exit_code == 0:
            actual_output = args.output if args.output else args.input.with_suffix(".gif")
            return 0, f"Successfully converted to {actual_output.resolve()}"
        else:
            return exit_code, f"ffmpeg conversion failed with exit code {exit_code}"
    except SystemExit as e:
        return 1, str(e)
    except Exception as e:
        return 1, f"An unexpected error occurred: {str(e)}"

# ==============================================================================
# MCP Server Implementation
# ==============================================================================
try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("video2gif")

    @mcp.tool()
    def convert_video_to_gif(
        input_path: str,
        output_path: str = None,
        fps: int = 12,
        width: int = None,
        start: float = None,
        duration: float = None,
        colors: int = 256,
        once: bool = False,
        overwrite: bool = False,
        no_optimize: bool = False
    ) -> str:
        """Convert a video file to a high-quality GIF using ffmpeg.
        
        Args:
            input_path: Absolute path to the input video file (e.g. .mp4, .mov).
            output_path: Path to the output GIF file. If not provided, defaults to the input path with .gif.
            fps: GIF frame rate (default: 12).
            width: Output width in pixels; height scales to keep aspect ratio.
            start: Start time in seconds.
            duration: Maximum clip duration in seconds.
            colors: Number of colors in the generated palette (2 to 256, default: 256).
            once: Generate a non-looping GIF (default is endless loop).
            overwrite: Overwrite the output file if it exists.
            no_optimize: Disable automatic gifsicle optimization.
        """
        code, msg = execute_conversion(
            input_path=input_path,
            output_path=output_path,
            fps=fps,
            width=width,
            start=start,
            duration=duration,
            colors=colors,
            once=once,
            overwrite=overwrite,
            no_optimize=no_optimize
        )
        return msg
except ImportError:
    mcp = None

# ==============================================================================
# HTTP FastAPI Server Implementation
# ==============================================================================
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
    from typing import Optional

    app = FastAPI(title="video2gif API Server", description="HTTP API for converting video to GIF")

    class ConvertRequest(BaseModel):
        input_path: str = Field(..., description="Path to the input video file")
        output_path: Optional[str] = Field(None, description="Path to the output GIF file")
        fps: int = Field(12, description="GIF frame rate")
        width: Optional[int] = Field(None, description="Output width in pixels")
        start: Optional[float] = Field(None, description="Start time in seconds")
        duration: Optional[float] = Field(None, description="Maximum clip duration in seconds")
        colors: int = Field(256, description="Palette color count (2-256)")
        once: bool = Field(False, description="Disable looping")
        overwrite: bool = Field(False, description="Overwrite output file if exists")
        no_optimize: bool = Field(False, description="Disable gifsicle optimization")

    @app.post("/convert")
    def convert_api(req: ConvertRequest):
        code, msg = execute_conversion(
            input_path=req.input_path,
            output_path=req.output_path,
            fps=req.fps,
            width=req.width,
            start=req.start,
            duration=req.duration,
            colors=req.colors,
            once=req.once,
            overwrite=req.overwrite,
            no_optimize=req.no_optimize
        )
        if code != 0:
            raise HTTPException(status_code=400, detail=msg)
        return {"status": "success", "message": msg}
except ImportError:
    app = None

# ==============================================================================
# Main Entry Point
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="video2gif MCP & HTTP Server")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mcp", action="store_true", help="Run in Stdio MCP mode")
    group.add_argument("--http", action="store_true", help="Run in HTTP API mode")
    parser.add_argument("--host", default="127.0.0.1", help="HTTP server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="HTTP server port (default: 8000)")
    
    args = parser.parse_args()
    
    if args.mcp:
        if mcp is None:
            print("Error: mcp package is not installed. Run 'pip install -r mcp/requirements.txt'", file=sys.stderr)
            sys.exit(1)
        print("Starting MCP server in stdio mode...", file=sys.stderr)
        mcp.run()
    elif args.http:
        if app is None:
            print("Error: fastapi/uvicorn packages are not installed. Run 'pip install -r mcp/requirements.txt'", file=sys.stderr)
            sys.exit(1)
        import uvicorn
        print(f"Starting HTTP API server on {args.host}:{args.port}...", file=sys.stderr)
        uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
