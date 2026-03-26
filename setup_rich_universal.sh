#!/bin/bash
# setup_rich_universal.sh - Cross-platform Rich installation
# Works on macOS, Ubuntu, and other Linux distributions

echo "================================"
echo "Rich Library Installation Script"
echo "================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    OS="Unknown"
fi

echo "Detected OS: $OS"
echo ""

# Try different installation methods
echo "Attempting to install Rich..."
echo ""

# Method 1: Standard pip (works on macOS, older Linux)
echo "Method 1: Standard pip3 install..."
pip3 install rich 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Success! Rich installed with standard pip3"
    exit 0
fi

# Method 2: User install (for permission issues)
echo "Method 1 failed. Trying Method 2: User install..."
pip3 install rich --user 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Success! Rich installed with --user flag"
    exit 0
fi

# Method 3: Break system packages (for Ubuntu 24+)
echo "Method 2 failed. Trying Method 3: System packages override..."
pip3 install rich --break-system-packages 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Success! Rich installed with --break-system-packages"
    exit 0
fi

# If all methods fail
echo ""
echo "✗ All installation methods failed."
echo ""
echo "Please try manually:"
echo "  1. pip3 install rich"
echo "  2. pip3 install rich --user"
echo "  3. pip3 install rich --break-system-packages"
echo ""
echo "Or ask your instructor for help."
exit 1
