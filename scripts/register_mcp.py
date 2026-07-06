import json
import sys
from pathlib import Path

def register():
    print("Registering video2gif MCP server...")
    
    home = Path.home()
    server_script = home / ".local" / "share" / "video2gif" / "mcp" / "server.py"
    
    if not server_script.exists():
        print(f"Error: server.py not found at {server_script}. Please run install.sh first.", file=sys.stderr)
        sys.exit(1)
        
    home = Path.home()
    config_paths = [
        home / ".config/claude/mcp.json",
        home / "Library/Application Support/Claude/claude_desktop_config.json"
    ]
    
    mcp_config_item = {
        "command": sys.executable,
        "args": [str(server_script.resolve()), "--mcp"],
        "env": {}
    }
    
    registered_any = False
    for path in config_paths:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                try:
                    with open(path, "r") as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
            else:
                data = {}
            
            if "mcpServers" not in data:
                data["mcpServers"] = {}
                
            data["mcpServers"]["video2gif"] = mcp_config_item
            
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"✓ Registered successfully to: {path}")
            registered_any = True
        except Exception as e:
            print(f"✗ Failed to register to {path}: {e}", file=sys.stderr)
            
    if registered_any:
        print("\nTo use the MCP server, please restart Claude Desktop or Claude Code.")
    else:
        print("\nNo configurations were modified.")

if __name__ == "__main__":
    register()
