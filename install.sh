#!/bin/bash
set -e

echo "=== video2gif Skill Installer ==="

# Check if we are running in the repo directory. If not, clone the repo into a temp directory and run from there.
if [ ! -f "scripts/video2gif.py" ] || [ ! -f "SKILL.md" ]; then
    echo "Running from remote script. Downloading repository to complete installation..."
    if ! command -v git &> /dev/null; then
        echo "Error: git is required to download the installer."
        exit 1
    fi
    TMP_DIR=$(mktemp -d -t video2gif-installer-XXXXXX)
    git clone --depth 1 https://github.com/davislinyd/video2gif.git "$TMP_DIR"
    cd "$TMP_DIR"
fi

# 1. Detect OS and install system dependencies (ffmpeg, gifsicle)
OS="$(uname -s)"
case "${OS}" in
    Linux*)
        echo "Detected Linux..."
        if [ -x "$(command -v apt-get)" ]; then
            echo "Using apt-get to install dependencies..."
            sudo apt-get update && sudo apt-get install -y ffmpeg gifsicle
        elif [ -x "$(command -v dnf)" ]; then
            echo "Using dnf to install dependencies..."
            sudo dnf install -y ffmpeg gifsicle
        elif [ -x "$(command -v yum)" ]; then
            echo "Using yum to install dependencies..."
            sudo yum install -y epel-release && sudo yum install -y ffmpeg gifsicle
        elif [ -x "$(command -v pacman)" ]; then
            echo "Using pacman to install dependencies..."
            sudo pacman -Syu --noconfirm ffmpeg gifsicle
        else
            echo "Warning: Package manager not recognized. Please install ffmpeg and gifsicle manually."
        fi
        ;;
    Darwin*)
        echo "Detected macOS..."
        if [ -x "$(command -v brew)" ]; then
            echo "Using Homebrew to install dependencies..."
            brew install ffmpeg gifsicle
        else
            echo "Error: Homebrew is required on macOS. Please install Homebrew first: https://brew.sh/"
            exit 1
        fi
        ;;
    *)
        echo "Unsupported OS: ${OS}. Please install ffmpeg and gifsicle manually."
        ;;
esac

# 2. Install to Antigravity (agy) Global Skill
echo "Installing for Antigravity (agy)..."
AGY_SKILL_DIR="${HOME}/.gemini/antigravity-cli/skills/video2gif"
mkdir -p "${AGY_SKILL_DIR}/scripts"
cp SKILL.md "${AGY_SKILL_DIR}/"
cp scripts/video2gif.py "${AGY_SKILL_DIR}/scripts/"
echo "Antigravity skill installed at: ${AGY_SKILL_DIR}"

# 3. Install to Codex / Agents Global Skill Directories
echo "Installing for Codex / Agents..."
CODEX_SKILL_DIR1="${HOME}/.agents/skills/video2gif"
CODEX_SKILL_DIR2="${HOME}/.codex/skills/video2gif"

mkdir -p "${CODEX_SKILL_DIR1}/scripts"
cp SKILL.md "${CODEX_SKILL_DIR1}/"
cp scripts/video2gif.py "${CODEX_SKILL_DIR1}/scripts/"

mkdir -p "${CODEX_SKILL_DIR2}/scripts"
cp SKILL.md "${CODEX_SKILL_DIR2}/"
cp scripts/video2gif.py "${CODEX_SKILL_DIR2}/scripts/"
echo "Codex / Agents skill installed."

# 4. Install to Claude Code Custom Commands Directory
echo "Installing for Claude Code..."
CLAUDE_COMMANDS_DIR="${HOME}/.claude/commands"
mkdir -p "${CLAUDE_COMMANDS_DIR}"
cp SKILL.md "${CLAUDE_COMMANDS_DIR}/video2gif.md"
echo "Claude Code custom command installed at: ${CLAUDE_COMMANDS_DIR}/video2gif.md"

# 5. Install as CLI tool for Claude, Codex, and general shell
echo "Installing CLI wrapper for Claude, Codex, and system terminal..."
INSTALL_BIN_DIR="${HOME}/.local/bin"
INSTALL_SHARE_DIR="${HOME}/.local/share/video2gif"

mkdir -p "${INSTALL_SHARE_DIR}"
cp scripts/video2gif.py "${INSTALL_SHARE_DIR}/"
chmod +x "${INSTALL_SHARE_DIR}/video2gif.py"

mkdir -p "${INSTALL_BIN_DIR}"
cat << 'EOF' > "${INSTALL_BIN_DIR}/video2gif"
#!/bin/bash
python3 "$HOME/.local/share/video2gif/video2gif.py" "$@"
EOF
chmod +x "${INSTALL_BIN_DIR}/video2gif"

echo "CLI tool installed at: ${INSTALL_BIN_DIR}/video2gif"
echo "Make sure ${INSTALL_BIN_DIR} is in your PATH. If not, add this to your ~/.bashrc or ~/.zshrc:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "================================="
echo "Installation complete!"
