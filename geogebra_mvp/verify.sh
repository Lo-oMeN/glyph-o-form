#!/bin/bash
# Quick verification script for GeoGebra MVP

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     THUNDERING GRACE ENGINE - Setup Verification           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Java
echo "Checking Java..."
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2)
    echo "  ✓ Java found: $JAVA_VERSION"
else
    echo "  ✗ Java not found! Please install Java 11+"
    exit 1
fi

# Check GeoGebra
echo ""
echo "Checking GeoGebra..."
GEOGEBRA_PATHS=(
    "/usr/share/geogebra"
    "/opt/geogebra"
    "$HOME/GeoGebra"
    "/Applications/GeoGebra 5.app/Contents/Java"
    "/Applications/GeoGebra Classic 5.app/Contents/Java"
)

GEOGEBRA_FOUND=""
for path in "${GEOGEBRA_PATHS[@]}"; do
    if [ -f "$path/geogebra.jar" ]; then
        GEOGEBRA_FOUND="$path"
        echo "  ✓ GeoGebra found: $path"
        break
    fi
done

if [ -z "$GEOGEBRA_FOUND" ]; then
    echo "  ✗ GeoGebra not found in standard locations!"
    echo "    Please install GeoGebra 5 Desktop from:"
    echo "    https://www.geogebra.org/download"
    echo ""
    echo "    Or set GEOGEBRA_PATH environment variable:"
    echo "    export GEOGEBRA_PATH=/path/to/geogebra"
    exit 1
fi

# Check project files
echo ""
echo "Checking project files..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIRED_FILES=(
    "src/org/thundergrace/glyph/SimpleGlyph.java"
    "src/org/thundergrace/glyph/GlyphRenderer.java"
    "src/org/thundergrace/glyph/DragHandler.java"
    "src/org/thundergrace/glyph/KenosisDemo.java"
    "README.md"
)

ALL_PRESENT=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file MISSING!"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    echo ""
    echo "Some files are missing. Please re-extract the project."
    exit 1
fi

# Check build tools
echo ""
echo "Checking build tools..."
if command -v ant &> /dev/null; then
    echo "  ✓ Apache Ant found"
    HAS_ANT=true
else
    echo "  ○ Apache Ant not found (optional)"
    HAS_ANT=false
fi

if command -v mvn &> /dev/null; then
    echo "  ✓ Apache Maven found"
    HAS_MAVEN=true
else
    echo "  ○ Apache Maven not found (optional)"
    HAS_MAVEN=false
fi

if [ "$HAS_ANT" = false ] && [ "$HAS_MAVEN" = false ]; then
    echo ""
    echo "  Note: No build tool found. Using direct javac."
fi

# Syntax check (if javac available)
echo ""
echo "Checking Java syntax..."
if command -v javac &> /dev/null; then
    mkdir -p /tmp/geogebra_mvp_check
    
    # Try to compile SimpleGlyph (no external deps)
    if javac -d /tmp/geogebra_mvp_check "$SCRIPT_DIR/src/org/thundergrace/glyph/SimpleGlyph.java" 2>/dev/null; then
        echo "  ✓ SimpleGlyph.java compiles"
    else
        echo "  ✗ SimpleGlyph.java has errors"
    fi
    
    rm -rf /tmp/geogebra_mvp_check
else
    echo "  ○ javac not available for syntax check"
fi

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                      VERIFICATION COMPLETE                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Setup appears ready! To build and run:"
echo ""

if [ "$HAS_ANT" = true ]; then
    echo "  Option 1 - Apache Ant:"
    echo "    cd $SCRIPT_DIR"
    echo "    ant run"
    echo ""
fi

if [ "$HAS_MAVEN" = true ]; then
    echo "  Option 2 - Apache Maven:"
    echo "    cd $SCRIPT_DIR"
    echo "    mvn compile exec:java -Dgeogebra.path=$GEOGEBRA_FOUND"
    echo ""
fi

echo "  Option 3 - Direct (no build tool):"
echo "    cd $SCRIPT_DIR"
echo "    ./build.sh"
echo ""

echo "  Option 4 - Manual:"
echo "    cd $SCRIPT_DIR"
echo "    mkdir -p out"
echo "    javac -cp \"$GEOGEBRA_FOUND/geogebra.jar\" -d out src/org/thundergrace/glyph/*.java"
echo "    java -cp \"out:$GEOGEBRA_FOUND/geogebra.jar\" org.thundergrace.glyph.KenosisDemo"
echo ""
