#!/bin/bash
# Build and run script for GeoGebra MVP

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  THUNDERING GRACE ENGINE - Build Script${NC}"
echo -e "${GREEN}============================================${NC}"

# Detect GeoGebra installation
GEOGEBRA_PATH=""

if [ -f "/usr/share/geogebra/geogebra.jar" ]; then
    GEOGEBRA_PATH="/usr/share/geogebra"
elif [ -f "/opt/geogebra/geogebra.jar" ]; then
    GEOGEBRA_PATH="/opt/geogebra"
elif [ -f "$HOME/GeoGebra/geogebra.jar" ]; then
    GEOGEBRA_PATH="$HOME/GeoGebra"
elif [ -f "/Applications/GeoGebra 5.app/Contents/Java/geogebra.jar" ]; then
    GEOGEBRA_PATH="/Applications/GeoGebra 5.app/Contents/Java"
fi

# Check for GeoGebra
if [ -z "$GEOGEBRA_PATH" ]; then
    echo -e "${RED}Error: GeoGebra not found!${NC}"
    echo "Please install GeoGebra Desktop from: https://www.geogebra.org/download"
    echo "Or set GEOGEBRA_PATH environment variable:"
    echo "  export GEOGEBRA_PATH=/path/to/geogebra"
    exit 1
fi

echo -e "${GREEN}Found GeoGebra at: $GEOGEBRA_PATH${NC}"

# Allow override
if [ -n "$GEOGEBRA_PATH" ]; then
    GEOGEBRA_PATH="${GEOGEBRA_PATH}"
fi

# Setup directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/src"
OUT_DIR="$SCRIPT_DIR/out"

# Create output directory
mkdir -p "$OUT_DIR"

# Compile
echo -e "${YELLOW}Compiling...${NC}"
javac -cp "$GEOGEBRA_PATH/geogebra.jar" \
      -d "$OUT_DIR" \
      "$SRC_DIR/org/thundergrace/glyph/SimpleGlyph.java" \
      "$SRC_DIR/org/thundergrace/glyph/GlyphRenderer.java" \
      "$SRC_DIR/org/thundergrace/glyph/DragHandler.java" \
      "$SRC_DIR/org/thundergrace/glyph/KenosisDemo.java"

echo -e "${GREEN}Compilation successful!${NC}"

# Run
echo -e "${YELLOW}Starting KENOSIS Demo...${NC}"
echo ""

java -cp "$OUT_DIR:$GEOGEBRA_PATH/geogebra.jar" \
     -Djava.awt.headless=false \
     org.thundergrace.glyph.KenosisDemo
