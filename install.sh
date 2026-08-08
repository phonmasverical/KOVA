#!/bin/bash
# KOVΛ Installer — Setup kovarun command
# Author: Nguyễn Khôi

echo "╔══════════════════════════════════════╗"
echo "║     KOVΛ Language Installer v1.0     ║"
echo "║     Author: Nguyễn Khôi             ║"
echo "╚══════════════════════════════════════╝"
echo ""

INSTALL_DIR="$HOME/.kova"
BIN_DIR="$HOME/.local/bin"

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Copy files
cp kovarun "$INSTALL_DIR/kovarun"
cp kova_core.py "$INSTALL_DIR/kova_core.py"

# Create wrapper script
cat > "$BIN_DIR/kovarun" << 'WRAPPER'
#!/bin/bash
python3 "$HOME/.kova/kovarun" "$@"
WRAPPER

chmod +x "$BIN_DIR/kovarun"

# Add to PATH if not already
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "" >> "$HOME/.bashrc"
    echo "# KOVΛ Language" >> "$HOME/.bashrc"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$HOME/.bashrc"
    echo ""
    echo "Added $BIN_DIR to PATH in ~/.bashrc"
    echo "Run: source ~/.bashrc"
fi

echo ""
echo "✅ KOVΛ installed successfully!"
echo ""
echo "Usage:"
echo "  kovarun              — Launch REPL"
echo "  kovarun file.kva     — Run a .kva file"
echo "  kovarun --help       — Show help"
echo "  kovarun --version    — Show version"
echo ""
echo "Create your first program:"
echo "  nano hello.kva"
echo "  # Type: emit(\"Hello KOVΛ!\")"
echo "  kovarun hello.kva"
echo ""
echo "🔥 Happy coding with KOVΛ!"
