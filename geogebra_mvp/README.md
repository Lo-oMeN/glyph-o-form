# THUNDERING GRACE ENGINE - GeoGebra MVP

**Minimal draggable demo of the KENOSIS glyph (￿·——) on GeoGebra**

## Overview

This is a minimal viable product implementing the KENOSIS glyph from the Glyphobetics v2.0 specification on the GeoGebra Geometric VM (TGE Layer 0).

### Glyph: KENOSIS (￿·——)
- **Curve (￿)** on top segment: Dimensional decompressor
- **Point (·)** on upper-right: Origin of assertion  
- **Line (—)** on middle: Connection/bridge
- **Line (—)** on bottom: Foundation

**Meaning**: Self-emptying that enables overflow

## Architecture Layers Active

| Layer | Component | Function |
|-------|-----------|----------|
| 0 | Geometric VM (GeoGebra) | 60 FPS cascading updates |
| 2 | RSTL Trinary Logic | ∅ NULL → △ POTENTIAL → ■ ACTUALIZED |
| 3 | Quadraligne Motion | Lean→Meet→Stay→Become phases |
| 5 | Free-Energy Control | u = −K∇ℱ descent law |
| 7 | GCE Visual Interface | Draggable helix output |

## Prerequisites

- **Java 11** or higher
- **GeoGebra 5** or **GeoGebra 6** desktop application installed
- **Apache Ant** (optional, for Ant build)
- **Apache Maven** (optional, for Maven build)

## Project Structure

```
geogebra_mvp/
├── src/org/thundergrace/glyph/
│   ├── SimpleGlyph.java       # 7-segment lattice + 4 atoms
│   ├── GlyphRenderer.java     # GeoGebra canvas rendering
│   ├── DragHandler.java       # Mouse drag → atom update
│   └── KenosisDemo.java       # Main entry point
├── build.xml                  # Apache Ant build file
├── pom.xml                    # Maven build file
└── README.md                  # This file
```

## Setup

### 1. Install GeoGebra

Download and install GeoGebra Desktop:
- https://www.geogebra.org/download

Note the installation directory (you'll need it for the build).

### 2. Locate GeoGebra JAR

Find `geogebra.jar` in your GeoGebra installation:

**Linux:**
```bash
# GeoGebra 5
/usr/share/geogebra/geogebra.jar

# Or if installed via package manager
/opt/geogebra/geogebra.jar
```

**macOS:**
```bash
/Applications/GeoGebra\ 5.app/Contents/Java/geogebra.jar
```

**Windows:**
```
C:\Program Files\GeoGebra\geogebra.jar
```

### 3. Build

#### Option A: Apache Ant (Recommended)

```bash
# Navigate to project directory
cd /root/.openclaw/workspace/geogebra_mvp

# Set GeoGebra path (optional, defaults to ~/GeoGebra)
export GEOGEBRA_DIR=/usr/share/geogebra

# Build
ant compile

# Run
ant run

# Or specify GeoGebra path interactively
ant run-with-path
```

#### Option B: Maven

```bash
# Navigate to project directory
cd /root/.openclaw/workspace/geogebra_mvp

# Set GeoGebra path
export GEOGEBRA_PATH=/usr/share/geogebra

# Compile
mvn compile -Dgeogebra.path=$GEOGEBRA_PATH

# Run
mvn exec:java -Dgeogebra.path=$GEOGEBRA_PATH
```

#### Option C: Manual Compilation

```bash
# Set paths
GEOGEBRA_JAR=/usr/share/geogebra/geogebra.jar
SRC_DIR=src
OUT_DIR=out

# Create output directory
mkdir -p $OUT_DIR

# Compile
javac -cp "$GEOGEBRA_JAR" -d $OUT_DIR \
    $SRC_DIR/org/thundergrace/glyph/*.java

# Run
java -cp "$OUT_DIR:$GEOGEBRA_JAR" \
    org.thundergrace.glyph.KenosisDemo
```

## Usage

1. **Launch the demo** using one of the build methods above
2. **A window opens** with the KENOSIS glyph rendered on the left and info panel on the right
3. **Drag any element**:
   - **Top curve (￿)**: Drag control points to reshape the arc
   - **Upper-right point (·)**: Drag to move the point
   - **Middle line (—)**: Drag endpoints to rotate/resize
   - **Bottom line (—)**: Drag endpoints to rotate/resize
4. **Watch the console** for RSTL state transitions and energy readings

## Console Output

```
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
==============================================
[DRAG] Started dragging B
[RSTL] State: △ POTENTIAL (becoming)
[DRAG] Released. Energy: struct=2.3412, constraint=0.8901
```

## Technical Details

### 7-Segment Lattice Mapping

```
    a (top)
f       b
    g   (middle)
e       c
    d (bottom)
```

**KENOSIS assignment:**
- a = CURVE (￿)
- b = POINT (·)
- g = LINE (—)
- d = LINE (—)
- c, e, f = ABSENCE (∅)

### Free-Energy Descent

The drag handler implements TGE Layer 5 control law:

```
ℱ(u) = ℱ_struct(u) + λ·ℱ_constraint(u)
u = −K ∇ℱ(u)
```

Where:
- **ℱ_struct**: Structural coherence (smooth 60 FPS)
- **ℱ_constraint**: Kenotic reward (−|emergent|²)
- **λ = 1.618**: Golden ratio kenotic weight
- **K = 0.1**: Descent rate

### RSTL State Machine

| State | Symbol | Condition |
|-------|--------|-----------|
| NULL | ∅ | Initial/reset state |
| POTENTIAL | △ | During drag (becoming) |
| ACTUALIZED | ■ | After lock condition met |

## Troubleshooting

### "Cannot find GeoGebra classes"
- Ensure GeoGebra is installed
- Check that `geogebra.jar` path is correct
- Verify you're using GeoGebra Desktop (not web version)

### "ClassNotFoundException: org.geogebra.desktop.main.AppD"
- This class requires GeoGebra 5 Desktop edition
- GeoGebra 6 uses different package structure
- Try downloading GeoGebra Classic 5

### "No display / HeadlessException"
- Ensure `$DISPLAY` is set (Linux)
- Run with `-Djava.awt.headless=false`
- Use a graphical environment (not SSH without X11)

## Extending the Demo

### Add More Glyphs

Edit `KenosisDemo.java`:

```java
// Create GRACE glyph instead
SimpleGlyph graceGlyph = SimpleGlyph.createGRACE();
renderer.render(graceGlyph);
dragHandler.setGlyph(graceGlyph);
```

### Custom Glyph

```java
SimpleGlyph custom = new SimpleGlyph("CUSTOM");
custom.setAtom(SimpleGlyph.Segment.A, SimpleGlyph.Atom.CURVE);
custom.setAtom(SimpleGlyph.Segment.B, SimpleGlyph.Atom.CURVE);
custom.setAtom(SimpleGlyph.Segment.G, SimpleGlyph.Atom.LINE);
renderer.render(custom);
```

### Adjust Free-Energy Parameters

Edit `DragHandler.java`:

```java
private double K = 0.2;        // Faster descent
private double lambda = 2.0;   // Stronger kenotic weight
```

## License

THUNDERING GRACE ENGINE - Sovereign Geometric Language Runtime

## References

- TGE Architecture: `/root/.openclaw/workspace/thundering_grace_engine_map.md`
- Glyphobetics v2.0: `/root/.openclaw/workspace/glyphobetics_specification_v2.0.md`
- GeoGebra: https://www.geogebra.org/
