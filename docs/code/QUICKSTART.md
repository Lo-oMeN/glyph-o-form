# QUICKSTART.md - Get Started with Glyph-o-betics

> **Get up and running in 5 minutes with the complete Glyph-o-betics toolkit.**

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Quick Test - Run First Conversion](#quick-test---run-first-conversion)
4. [Build GeoGebra Demo](#build-geogebra-demo)
5. [Test Vision Processing](#test-vision-processing)
6. [Next Steps](#next-steps)

---

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.8+ | Core converter scripts |
| Java | 11+ | GeoGebra demo |
| OpenCV | 4.x+ | Vision processing |

### Check Your Environment

```bash
# Check Python
python3 --version
# Expected: Python 3.8.x or higher

# Check Java
java -version
# Expected: openjdk version "11" or higher

# Check pip
pip3 --version
```

---

## Installation

### Step 1: Clone/Navigate to Project

```bash
cd /root/.openclaw/workspace
```

### Step 2: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install numpy pillow

# For vision processing
pip install opencv-python
```

### Step 3: Verify Installation

```bash
# Test Python imports
python3 -c "import numpy; import cv2; print('✓ Python dependencies OK')"

# Check Java
java -version && echo "✓ Java OK"
```

**Expected Output:**
```
✓ Python dependencies OK
openjdk version "11.0.x" ...
✓ Java OK
```

---

## Quick Test - Run First Conversion

### Convert Your First Word

```bash
# Convert a single word
python3 mvp_glyph_converter.py LOVE
```

**Expected Output:**
```
============================================================
  GLYPH-o-BETICS CONVERSION
============================================================

  English Input: LOVE
  Glyph Output:  ￿·￿∅—￿—

  Descent Pathways:
    Phonetic:     ￿·￿∅—￿—
    Orthographic: —￿·——∅∅
    Semantic:     ￿·￿∅—￿—
    ─────────────────────────
    Final (fused): ￿·￿∅—￿—

  Segment Mapping:
    a b c d e f g
    ￿ · ￿ ∅ — ￿ —

┌─ GLYPH: LOVE
│          
│     ￿   
│  —     ·
│     ——  
│  ∅     ￿
│     ——  
└──────────

  Atom Composition:
    · (Point   ): █░░░░░░ (1/7)
    — (Line    ): ██░░░░░ (2/7)
    ￿ (Curve   ): ███░░░░ (3/7)
    ∅ (Absence ): █░░░░░░ (1/7)
```

### Convert Multiple Words

```bash
# Compare multiple words (resonance analysis)
python3 mvp_glyph_converter.py LOVE TRUTH FREEDOM
```

**Expected Output:**
```
======================================================================
  GLYPH-o-BETICS RESONANCE ANALYSIS
======================================================================

  LOVE         → ￿·￿∅—￿—
  TRUTH        → ·—·∅—￿∅
  FREEDOM      → ￿—∅∅—￿—

  ...visualizations...

  Resonance Matrix
  ────────────────────────────────────────────────────────────
            LOVE    TRUTH  FREEDOM
  LOVE   │   1.00   0.45    0.72
  TRUTH  │   0.45   1.00    0.38
  FREEDOM│   0.72   0.38    1.00

  Pair Analysis
  ────────────────────────────────────────────────────────────
  LOVE ↔ TRUTH: 0.452 ◐ MODERATE CONNECTION
  LOVE ↔ FREEDOM: 0.723 ☯ STRONG HARMONY
  TRUTH ↔ FREEDOM: 0.378 ◐ MODERATE CONNECTION
```

### Run Self-Test

```bash
# Verify everything works correctly
python3 mvp_glyph_converter.py --test
```

**Expected Output:**
```
============================================================
  GLYPH-o-BETICS SELF-TEST
============================================================

  ✓ LOVE → ￿·￿∅—￿—
  ✓ TRUTH → ·—·∅—￿∅
  ✓ FREEDOM → ￿—∅∅—￿—

  Resonance Tests:
    LOVE-LOVE: 1.000
    LOVE-TRUTH: 0.452
    LOVE-FREEDOM: 0.723
    TRUTH-TRUTH: 1.000
    TRUTH-FREEDOM: 0.378
    FREEDOM-FREEDOM: 1.000

  ✓ All tests passed!
```

---

## Build GeoGebra Demo

### Prerequisites

1. **Install GeoGebra Classic 5**
   - Download: https://www.geogebra.org/download
   - **Important**: Get version 5, not version 6
   - GeoGebra 5 has `org.geogebra.desktop.main.AppD`
   - GeoGebra 6 uses different packages

2. **Find GeoGebra Installation**

   **Linux:**
   ```bash
   # Check common locations
   ls /usr/share/geogebra/geogebra.jar
   ls /opt/geogebra/geogebra.jar
   
   # Or search
   find /usr -name "geogebra.jar" 2>/dev/null
   ```

   **macOS:**
   ```bash
   ls "/Applications/GeoGebra 5.app/Contents/Java/geogebra.jar"
   ```

   **Windows:**
   ```cmd
   dir "C:\Program Files\GeoGebra\geogebra.jar"
   ```

### Build Method A: Automated Script (Easiest)

```bash
cd /root/.openclaw/workspace/geogebra_mvp

# Run build script (auto-detects GeoGebra)
./build.sh
```

**Expected Output:**
```
============================================
  THUNDERING GRACE ENGINE - Build Script
============================================
Found GeoGebra at: /usr/share/geogebra
Compiling...
Compilation successful!
Starting KENOSIS Demo...

==============================================
  THUNDERING GRACE ENGINE - KENOSIS Demo
  Glyph: ￿·—— (Self-emptying enabling overflow)
==============================================
[INIT] Created glyph: KENOSIS
[INIT] Atomic sequence: ￿·——
[INIT] Glyph rendered to canvas
[INIT] Drag handler active
==============================================
  DEMO RUNNING - Drag any glyph element!
  - Curve (top): Drag control points
  - Upper-right point (·): Drag to move
  - Middle line (—): Drag endpoints
  - Bottom line (—): Drag endpoints
==============================================
```

### Build Method B: Manual Compilation

```bash
cd /root/.openclaw/workspace/geogebra_mvp

# Set GeoGebra path
export GEOGEBRA_JAR=/usr/share/geogebra/geogebra.jar

# Create output directory
mkdir -p out

# Compile
javac -cp "$GEOGEBRA_JAR" \
    -d out \
    src/org/thundergrace/glyph/SimpleGlyph.java \
    src/org/thundergrace/glyph/GlyphRenderer.java \
    src/org/thundergrace/glyph/DragHandler.java \
    src/org/thundergrace/glyph/KenosisDemo.java

# Run
java -cp "out:$GEOGEBRA_JAR" \
    -Djava.awt.headless=false \
    org.thundergrace.glyph.KenosisDemo
```

### Interacting with the Demo

Once the demo window opens:

1. **Drag the Top Curve (￿)**
   - Click and drag any of the 3 control points
   - Reshapes the arc

2. **Drag the Point (·)**
   - Click and drag the gold point
   - Moves it around

3. **Drag the Lines (—)**
   - Click and drag either endpoint
   - Rotates and resizes the line

4. **Watch the Console**
   - See RSTL state changes
   - Monitor energy descent values

**RSTL States:**
- `△ POTENTIAL` - While dragging (becoming)
- `■ ACTUALIZED` - After sufficient energy descent (locked)

---

## Test Vision Processing

### Create a Test Image

Draw a simple 7-segment glyph on paper or digitally:

```
    ￿       ← Curve on top
   ·  —     ← Point upper-right, Line middle
    —       ← Line bottom
```

Save as `my_glyph.png`

### Run Vision Analysis

```bash
cd /root/.openclaw/workspace

python3 vision_processor.py my_glyph.png
```

**Expected Output:**
```
╔════════════════════════════════════════╗
║     GLYPH VISION ANALYSIS              ║
╚════════════════════════════════════════╝

Detected Glyph: ￿·—∅—∅∅
Confidence: 75.0%

Segment Breakdown:
  a: ￿
  b: ·
  c: —
  d: —
  e: ∅
  f: ∅
  g: ∅

Visualization:

      ￿
   ∅     ·
      ∅
   ∅     —
      —
```

### Validate Against Expected

```bash
# Compare to known glyph
python3 vision_processor.py my_glyph.png '￿·—∅—∅∅'
```

**Expected Output:**
```
╔════════════════════════════════════════╗
║     GLYPH VISION ANALYSIS              ║
╚════════════════════════════════════════╝

Detected Glyph: ￿·—∅—∅∅
Confidence: 75.0%
...
Expected: ￿·—∅—∅∅
Similarity: 100.0%
Match: ✓ YES
```

### Test with Sample Images

Create test images for quick validation:

```bash
# Create test directory
mkdir -p vision_tests
cd vision_tests

# If you have sample images
echo "Testing vision processor with samples..."
for img in *.png *.jpg; do
    echo "Testing: $img"
    python3 ../vision_processor.py "$img"
    echo "---"
done
```

---

## Next Steps

### 1. Explore the Converter

```python
# Create a Python script to batch convert
from mvp_glyph_converter import GlyphConverter

converter = GlyphConverter()

words = ["PEACE", "JOY", "HOPE", "GRACE"]
for word in words:
    glyph = converter.english_to_glyph(word)
    print(f"{word} → {glyph}")
```

### 2. Experiment with Resonance

```python
# Find resonant word pairs
from mvp_glyph_converter import GlyphConverter

converter = GlyphConverter()

# Find words that resonate with LOVE
love_glyph = converter.english_to_glyph("LOVE")

test_words = ["HEART", "SOUL", "MIND", "BODY", "SPIRIT"]
for word in test_words:
    r = converter.compute_resonance("LOVE", word)
    print(f"LOVE ↔ {word}: {r:.3f}")
```

### 3. Customize the GeoGebra Demo

Edit `geogebra_mvp/src/org/thundergrace/glyph/KenosisDemo.java`:

```java
// Change to GRACE glyph
SimpleGlyph graceGlyph = SimpleGlyph.createGRACE();
renderer.render(graceGlyph);
dragHandler.setGlyph(graceGlyph);
```

### 4. Calibrate Vision Processor

```python
from vision_processor import GlyphVisionProcessor
import cv2

# Adjust thresholds for your setup
processor = GlyphVisionProcessor()

# Test and calibrate
result = processor.analyze_image('your_image.png')
print(f"Confidence: {result['analysis_confidence']}")

# If confidence is low, try preprocessing
img = cv2.imread('your_image.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imwrite('processed.png', blurred)

result = processor.analyze_image('processed.png')
```

### 5. Read Full Documentation

- [mvp_glyph_converter.md](docs/code/mvp_glyph_converter.md) - Detailed converter docs
- [geogebra_mvp.md](docs/code/geogebra_mvp.md) - Java classes reference
- [vision_processor.md](docs/code/vision_processor.md) - Vision processing guide
- [TESTS.md](docs/code/TESTS.md) - Testing procedures

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'cv2'"

```bash
pip install opencv-python
```

### "Cannot find GeoGebra classes"

```bash
# Find geogebra.jar
find / -name "geogebra.jar" 2>/dev/null

# Set the path
export GEOGEBRA_PATH=/path/to/geogebra
```

### "No X11 DISPLAY variable was set"

```bash
# If running via SSH, enable X11 forwarding
ssh -X user@host

# Or use virtual display
sudo apt-get install xvfb
xvfb-run ./build.sh
```

### "Java version mismatch"

```bash
# Check Java version
java -version

# Install Java 11 if needed
sudo apt-get install openjdk-11-jdk
```

---

## Summary

You now have:

✅ **Installed** all dependencies  
✅ **Converted** your first words to glyphs  
✅ **Built** the interactive GeoGebra demo  
✅ **Tested** the vision processor  

**Ready to explore the THUNDERING GRACE ENGINE!**

Try these commands:
```bash
# Convert words
python3 mvp_glyph_converter.py PEACE GRACE HOPE

# Run the interactive demo
cd geogebra_mvp && ./build.sh

# Analyze an image
python3 vision_processor.py your_image.png
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Convert word | `python3 mvp_glyph_converter.py WORD` |
| Compare words | `python3 mvp_glyph_converter.py WORD1 WORD2` |
| Self-test | `python3 mvp_glyph_converter.py --test` |
| Build GeoGebra demo | `cd geogebra_mvp && ./build.sh` |
| Analyze image | `python3 vision_processor.py image.png` |
| Validate image | `python3 vision_processor.py image.png GLYPH` |

---

*Welcome to Glyph-o-betics - Where language becomes geometry.*
