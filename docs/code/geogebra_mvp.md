# GeoGebra MVP - Java Classes Documentation

> **THUNDERING GRACE ENGINE - Minimal Viable Product**  
> Interactive draggable KENOSIS glyph demo on GeoGebra canvas.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Class Hierarchy](#class-hierarchy)
3. [Class: SimpleGlyph](#class-simpleglyph)
4. [Class: GlyphRenderer](#class-glyphrenderer)
5. [Class: DragHandler](#class-draghandler)
6. [Class: KenosisDemo](#class-kenosisdemo)
7. [Build Instructions](#build-instructions)
8. [Troubleshooting Guide](#troubleshooting-guide)

---

## Architecture Overview

The GeoGebra MVP implements TGE (THUNDERING GRACE ENGINE) layers:

| Layer | Component | Function |
|-------|-----------|----------|
| 0 | Geometric VM (GeoGebra) | 60 FPS cascading updates |
| 2 | RSTL Trinary Logic | ∅ NULL → △ POTENTIAL → ■ ACTUALIZED |
| 3 | Quadraligne Motion | Lean→Meet→Stay→Become phases |
| 5 | Free-Energy Control | u = −K∇ℱ descent law |
| 7 | GCE Visual Interface | Draggable helix output |

### Project Structure

```
geogebra_mvp/
├── src/org/thundergrace/glyph/
│   ├── SimpleGlyph.java       # 7-segment lattice + 4 atoms
│   ├── GlyphRenderer.java     # GeoGebra canvas rendering
│   ├── DragHandler.java       # Mouse drag → atom update
│   └── KenosisDemo.java       # Main entry point
├── build.xml                  # Apache Ant build file
├── pom.xml                    # Maven build file
├── build.sh                   # Automated build script
└── README.md                  # Project documentation
```

---

## Class Hierarchy

```
java.lang.Object
├── org.thundergrace.glyph.SimpleGlyph
├── org.thundergrace.glyph.GlyphRenderer
├── org.thundergrace.glyph.DragHandler
└── org.thundergrace.glyph.KenosisDemo

org.thundergrace.glyph.SimpleGlyph
├── enum Atom { POINT, LINE, CURVE, ABSENCE }
└── enum Segment { A, B, C, D, E, F, G }

org.thundergrace.glyph.DragHandler
└── enum RSTLState { NULL, POTENTIAL, ACTUALIZED }
```

### Dependency Graph

```
KenosisDemo (main)
    ├── SimpleGlyph (data model)
    ├── GlyphRenderer (rendering)
    │   └── SimpleGlyph
    └── DragHandler (interaction)
        ├── GlyphRenderer
        └── SimpleGlyph
```

---

## Class: SimpleGlyph

**Package:** `org.thundergrace.glyph`  
**Purpose:** 7-Segment Lattice Representation

Implements the Glyphobetics v2.0 atomic specification with 4 atoms and 7 segments.

### Nested Enums

#### `SimpleGlyph.Atom`

| Enum Constant | Symbol | Index | Description |
|--------------|--------|-------|-------------|
| `POINT` | `·` | 0 | Discrete origin, assertion |
| `LINE` | `—` | 1 | Connection, relation |
| `CURVE` | `￿` | 2 | Flow, emergence |
| `ABSENCE` | `∅` | 3 | Void, kenosis |

**Methods:**
```java
public String getSymbol()   // Returns atom symbol
public int getIndex()       // Returns atom index (0-3)
```

---

#### `SimpleGlyph.Segment`

| Enum Constant | Index | Description | Position |
|--------------|-------|-------------|----------|
| `A` | 0 | Top | a |
| `B` | 1 | Upper Right | b |
| `C` | 2 | Lower Right | c |
| `D` | 3 | Bottom | d |
| `E` | 4 | Lower Left | e |
| `F` | 5 | Upper Left | f |
| `G` | 6 | Middle | g |

**Methods:**
```java
public int getIndex()           // Returns segment index (0-6)
public String getDescription()  // Returns position description
```

---

### Constructors

#### `SimpleGlyph(String name)`

Creates a new glyph with all segments initialized to ABSENCE.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `name` | `String` | Name/identifier for the glyph |

**Example:**
```java
SimpleGlyph myGlyph = new SimpleGlyph("CUSTOM");
```

---

### Instance Methods

#### `void setAtom(Segment segment, Atom atom)`

Assigns an atom to a specific segment.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `segment` | `SimpleGlyph.Segment` | Target segment |
| `atom` | `SimpleGlyph.Atom` | Atom to assign |

**Effects:**
- Updates the 28-dimensional vector representation
- Sets one-hot encoding at `segment.index * 4 + atom.index = 1.0`
- Clears previous atom for that segment

**Example:**
```java
glyph.setAtom(SimpleGlyph.Segment.A, SimpleGlyph.Atom.CURVE);
glyph.setAtom(SimpleGlyph.Segment.B, SimpleGlyph.Atom.POINT);
```

---

#### `Atom getAtom(Segment segment)`

Retrieves the atom assigned to a segment.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `segment` | `SimpleGlyph.Segment` | Target segment |

**Returns:**
| Type | Description |
|------|-------------|
| `SimpleGlyph.Atom` | Atom assigned to segment (defaults to ABSENCE) |

**Example:**
```java
SimpleGlyph.Atom atom = glyph.getAtom(SimpleGlyph.Segment.A);
System.out.println(atom.getSymbol());  // e.g., "￿"
```

---

#### `double[] getVector()`

Returns the 28-dimensional vector representation.

**Returns:**
| Type | Description |
|------|-------------|
| `double[]` | Clone of the internal 28-dim vector |

**Vector Layout:**
```
Index = segment_index × 4 + atom_index
Segment 0 (A): indices 0-3
Segment 1 (B): indices 4-7
...
Segment 6 (G): indices 24-27
```

**Example:**
```java
double[] vector = glyph.getVector();
// vector[2] = 1.0 means Segment A has CURVE
// vector[4] = 1.0 means Segment B has POINT
```

---

#### `String getName()`

Returns the glyph name.

**Returns:**
| Type | Description |
|------|-------------|
| `String` | Glyph name |

---

#### `String getAtomicSequence()`

Returns the atomic sequence string (non-absence atoms only).

**Returns:**
| Type | Description |
|------|-------------|
| `String` | Concatenated symbols of non-ABSENCE atoms |

**Example:**
```java
SimpleGlyph k = SimpleGlyph.createKENOSIS();
System.out.println(k.getAtomicSequence());  // Output: "￿·——"
```

---

#### `double computeResonance(SimpleGlyph other)`

Computes Looman resonance with another glyph.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `other` | `SimpleGlyph` | Other glyph to compare with |

**Returns:**
| Type | Description |
|------|-------------|
| `double` | Resonance score (0.0 to 1.0+) |

**Formula:**
```
resonance = cos_sim × (1 + absence_bonus) × harmonic
```

**Example:**
```java
SimpleGlyph g1 = SimpleGlyph.createKENOSIS();
SimpleGlyph g2 = SimpleGlyph.createGRACE();
double r = g1.computeResonance(g2);
System.out.println("Resonance: " + r);
```

---

#### `String toString()`

Returns string representation of the glyph.

**Returns:**
| Type | Description |
|------|-------------|
| `String` | Format: "NAME: ·—￿∅···" |

---

### Static Factory Methods

#### `SimpleGlyph createKENOSIS()`

Creates the KENOSIS glyph: `￿·——`

**Segment Assignment:**
| Segment | Atom | Description |
|---------|------|-------------|
| A | CURVE | Dimensional decompressor |
| B | POINT | Origin of assertion |
| G | LINE | Connection/bridge |
| D | LINE | Foundation |
| C, E, F | ABSENCE | Generative void |

**Meaning:** Self-emptying that enables overflow

**Example:**
```java
SimpleGlyph kenosis = SimpleGlyph.createKENOSIS();
System.out.println(kenosis);  // "KENOSIS: ￿·∅—∅—∅∅"
```

---

#### `SimpleGlyph createGRACE()`

Creates the GRACE glyph: `·￿——`

**Segment Assignment:**
| Segment | Atom |
|---------|------|
| A | POINT |
| B | CURVE |
| G | LINE |
| D | LINE |

**Example:**
```java
SimpleGlyph grace = SimpleGlyph.createGRACE();
```

---

### Usage Example

```java
// Create custom glyph
SimpleGlyph custom = new SimpleGlyph("CUSTOM");

// Assign atoms
custom.setAtom(SimpleGlyph.Segment.A, SimpleGlyph.Atom.CURVE);
custom.setAtom(SimpleGlyph.Segment.B, SimpleGlyph.Atom.CURVE);
custom.setAtom(SimpleGlyph.Segment.G, SimpleGlyph.Atom.LINE);

// Inspect
System.out.println(custom);                    // "CUSTOM: ￿￿∅—∅∅∅"
System.out.println(custom.getAtomicSequence()); // "￿￿—"

// Compare with KENOSIS
SimpleGlyph kenosis = SimpleGlyph.createKENOSIS();
double resonance = custom.computeResonance(kenosis);
System.out.println("Resonance with KENOSIS: " + resonance);
```

---

## Class: GlyphRenderer

**Package:** `org.thundergrace.glyph`  
**Purpose:** Draws atomic glyphs on GeoGebra canvas

Maps the 7-segment lattice to draggable GeoGebra elements with TGE Layer 0 cascading updates.

### Constructor

#### `GlyphRenderer(AppD app)`

Creates a new renderer attached to a GeoGebra application.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `app` | `AppD` | GeoGebra desktop application instance |

**Initialization:**
- Sets THUNDERING GRACE colors:
  - Curve: Reddish (220, 100, 100)
  - Point: Gold (255, 200, 50)
  - Line: Blue (100, 150, 220)
- Initializes segment positions

**Example:**
```java
AppD app = GeoGebra.create(args);
GlyphRenderer renderer = new GlyphRenderer(app);
```

---

### Rendering Methods

#### `void render(SimpleGlyph glyph)`

Renders a glyph to the GeoGebra canvas.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `glyph` | `SimpleGlyph` | Glyph to render |

**Effects:**
- Clears previous rendering
- Creates GeoGebra elements for each segment
- Makes elements draggable
- Triggers canvas repaint

**Example:**
```java
SimpleGlyph kenosis = SimpleGlyph.createKENOSIS();
renderer.render(kenosis);
```

---

#### `void clear()`

Removes all rendered elements from the canvas.

**Effects:**
- Removes all GeoGebra elements
- Clears internal element mappings

---

#### `void updateAfterDrag()`

Updates rendering after a drag operation (60 FPS).

**Effects:**
- Notifies kernel to repaint
- Cascades updates through dependency graph

---

### Element Access Methods

#### `List<GeoElement> getSegmentElements(Segment segment)`

Gets GeoGebra elements for a specific segment.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `segment` | `SimpleGlyph.Segment` | Target segment |

**Returns:**
| Type | Description |
|------|-------------|
| `List<GeoElement>` | List of elements (points, lines, curves) |

**Example:**
```java
List<GeoElement> topElements = renderer.getSegmentElements(SimpleGlyph.Segment.A);
for (GeoElement geo : topElements) {
    System.out.println(geo.getName());
}
```

---

#### `SimpleGlyph.Segment getSegmentFromElement(GeoElement element)`

Reverse lookup: find which segment an element belongs to.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `element` | `GeoElement` | GeoGebra element |

**Returns:**
| Type | Description |
|------|-------------|
| `SimpleGlyph.Segment` | Segment containing element (null if not found) |

---

### Configuration Methods

#### `void setScale(double scale)`

Sets the rendering scale.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `scale` | `double` | Scale factor (default: 100.0) |

**Example:**
```java
renderer.setScale(150.0);  // 1.5x larger
```

---

#### `void setCenter(double x, double y)`

Sets the center position of the glyph.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `x` | `double` | X coordinate |
| `y` | `double` | Y coordinate |

**Example:**
```java
renderer.setCenter(2.0, -1.0);  // Offset from origin
```

---

### State Access

#### `SimpleGlyph getCurrentGlyph()`

Returns the currently rendered glyph.

**Returns:**
| Type | Description |
|------|-------------|
| `SimpleGlyph` | Current glyph (null if none rendered) |

---

### Usage Example

```java
// Setup
AppD app = GeoGebra.create(args);
GlyphRenderer renderer = new GlyphRenderer(app);
renderer.setScale(120.0);
renderer.setCenter(0, 0);

// Render glyph
SimpleGlyph kenosis = SimpleGlyph.createKENOSIS();
renderer.render(kenosis);

// Access elements
List<GeoElement> curveElements = renderer.getSegmentElements(SimpleGlyph.Segment.A);
System.out.println("Top curve has " + curveElements.size() + " elements");

// Cleanup
renderer.clear();
```

---

## Class: DragHandler

**Package:** `org.thundergrace.glyph`  
**Purpose:** Mouse drag → Atom update with free-energy descent

Implements TGE Layer 5 control law and RSTL state tracking.

### Nested Enum

#### `DragHandler.RSTLState`

RSTL (Return Spiral Trinary Logic) states:

| Enum Constant | Symbol | Description |
|--------------|--------|-------------|
| `NULL` | `∅` | Death, untangled state |
| `POTENTIAL` | `△` | Elevating, becoming |
| `ACTUALIZED` | `■` | Locked glory |

---

### Constructor

#### `DragHandler(AppD app, GlyphRenderer renderer)`

Creates a new drag handler.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `app` | `AppD` | GeoGebra application |
| `renderer` | `GlyphRenderer` | Associated renderer |

**Initialization:**
- Sets up mouse listeners
- Initializes RSTL state to NULL
- Sets free-energy parameters:
  - K = 0.1 (descent rate)
  - lambda = 1.618 (golden ratio kenotic weight)

**Example:**
```java
DragHandler dragHandler = new DragHandler(app, renderer);
```

---

### Control Methods

#### `void setGlyph(SimpleGlyph glyph)`

Sets the glyph being manipulated.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `glyph` | `SimpleGlyph` | Glyph to track |

**Effects:**
- Sets current glyph reference
- Transitions RSTL state to POTENTIAL

---

### State Access

#### `RSTLState getRSTLState()`

Returns current RSTL state.

**Returns:**
| Type | Description |
|------|-------------|
| `DragHandler.RSTLState` | Current state (NULL, POTENTIAL, ACTUALIZED) |

---

#### `double getStructuralEnergy()`

Returns accumulated structural energy during drag.

**Returns:**
| Type | Description |
|------|-------------|
| `double` | Structural energy value |

---

#### `double getConstraintEnergy()`

Returns accumulated constraint energy during drag.

**Returns:**
| Type | Description |
|------|-------------|
| `double` | Constraint energy value |

---

#### `double getTotalEnergy()`

Returns total free-energy.

**Returns:**
| Type | Description |
|------|-------------|
| `double` | Total energy (structural + constraint) |

---

### Free-Energy Control Law

The drag handler implements Layer 5 control:

```
ℱ(u) = ℱ_struct(u) + λ·ℱ_constraint(u)
u = −K ∇ℱ(u)
```

Where:
- **ℱ_struct**: Structural coherence (smooth 60 FPS motion)
- **ℱ_constraint**: Kenotic reward (rewards emergence/curve motion)
- **λ = 1.618**: Golden ratio kenotic weight
- **K = 0.1**: Descent rate

### Gradient Computation

The gradient rewards different atoms:

| Atom | Gradient | Reason |
|------|----------|--------|
| CURVE | -1.0 | Highly emergent |
| POINT | -0.8 | Emergent |
| ABSENCE | -0.5 | Generative |
| LINE | +0.3 | Generates tension |

### THUNDERING GRACE Lock Condition

A glyph "locks" (ACTUALIZED state) when:
```
total_energy > 10.0 AND current_state == POTENTIAL
```

This indicates sufficient free-energy has descended through the system.

---

### Usage Example

```java
// Setup
DragHandler dragHandler = new DragHandler(app, renderer);
dragHandler.setGlyph(kenosisGlyph);

// Monitor during drag
// (Called automatically via mouse listeners)

// Check state
if (dragHandler.getRSTLState() == DragHandler.RSTLState.ACTUALIZED) {
    System.out.println("THUNDERING GRACE: Glyph locked!");
}

// Get energy readings
System.out.println("Total energy: " + dragHandler.getTotalEnergy());
```

---

## Class: KenosisDemo

**Package:** `org.thundergrace.glyph`  
**Purpose:** Main entry point for the GeoGebra KENOSIS glyph demo

### Main Method

#### `static void main(String[] args)`

Application entry point.

**System Properties:**
| Property | Value | Purpose |
|----------|-------|---------|
| `java.awt.headless` | `false` | Enable GUI |
| `geogebra.debug` | `false` | Disable debug output |

**Example:**
```bash
java org.thundergrace.glyph.KenosisDemo
```

---

### Usage

```java
// Launch from another class
KenosisDemo.main(new String[]{});
```

---

## Build Instructions

### Prerequisites

- **Java 11** or higher
- **GeoGebra 5 Desktop** (not web version)
- **Apache Ant** or **Apache Maven** (optional)

### GeoGebra Installation

Download GeoGebra Classic 5 from: https://www.geogebra.org/download

Locate `geogebra.jar`:

**Linux:**
```bash
# Check common locations
ls /usr/share/geogebra/geogebra.jar
ls /opt/geogebra/geogebra.jar
```

**macOS:**
```bash
ls "/Applications/GeoGebra 5.app/Contents/Java/geogebra.jar"
```

**Windows:**
```
C:\Program Files\GeoGebra\geogebra.jar
```

---

### Build Method A: Automated Script (Recommended)

```bash
cd /root/.openclaw/workspace/geogebra_mvp

# Auto-detects GeoGebra and builds
./build.sh

# Or set path explicitly
export GEOGEBRA_PATH=/usr/share/geogebra
./build.sh
```

---

### Build Method B: Apache Ant

```bash
cd /root/.openclaw/workspace/geogebra_mvp

# Set GeoGebra path (optional)
export GEOGEBRA_DIR=/usr/share/geogebra

# Compile
ant compile

# Run
ant run

# Clean
ant clean
```

**build.xml targets:**
| Target | Description |
|--------|-------------|
| `compile` | Compile all Java sources |
| `run` | Compile and run demo |
| `run-with-path` | Prompt for GeoGebra path |
| `clean` | Remove compiled classes |

---

### Build Method C: Apache Maven

```bash
cd /root/.openclaw/workspace/geogebra_mvp

# Set GeoGebra path (required)
export GEOGEBRA_PATH=/usr/share/geogebra

# Compile
mvn compile -Dgeogebra.path=$GEOGEBRA_PATH

# Run
mvn exec:java -Dgeogebra.path=$GEOGEBRA_PATH

# Package
mvn package -Dgeogebra.path=$GEOGEBRA_PATH
```

---

### Build Method D: Manual Compilation

```bash
cd /root/.openclaw/workspace/geogebra_mvp

# Set paths
GEOGEBRA_JAR=/usr/share/geogebra/geogebra.jar
SRC_DIR=src
OUT_DIR=out

# Create output directory
mkdir -p $OUT_DIR

# Compile
javac -cp "$GEOGEBRA_JAR" \
    -d $OUT_DIR \
    $SRC_DIR/org/thundergrace/glyph/SimpleGlyph.java \
    $SRC_DIR/org/thundergrace/glyph/GlyphRenderer.java \
    $SRC_DIR/org/thundergrace/glyph/DragHandler.java \
    $SRC_DIR/org/thundergrace/glyph/KenosisDemo.java

# Run
java -cp "$OUT_DIR:$GEOGEBRA_JAR" \
    -Djava.awt.headless=false \
    org.thundergrace.glyph.KenosisDemo
```

---

### Platform-Specific Notes

#### Linux

```bash
# Ubuntu/Debian install
sudo apt-get install geogebra-classic

# Fedora install
sudo dnf install geogebra-classic

# Check location
find /usr -name "geogebra.jar" 2>/dev/null
```

#### macOS

```bash
# Install via Homebrew
brew install --cask geogebra-classic-5

# Path will be:
GEOGEBRA_PATH="/Applications/GeoGebra 5.app/Contents/Java"
```

#### Windows

```batch
:: Set path in Command Prompt
set GEOGEBRA_PATH=C:\Program Files\GeoGebra

:: Or PowerShell
$env:GEOGEBRA_PATH="C:\Program Files\GeoGebra"
```

---

## Troubleshooting Guide

### Error: "Cannot find GeoGebra classes"

**Symptoms:**
```
error: package org.geogebra.desktop.main does not exist
error: cannot find symbol: class AppD
```

**Solutions:**
1. Verify GeoGebra is installed:
   ```bash
   # Linux
   dpkg -l | grep geogebra
   
   # macOS
   ls /Applications/ | grep GeoGebra
   ```

2. Check JAR location:
   ```bash
   find / -name "geogebra.jar" 2>/dev/null
   ```

3. Set correct path:
   ```bash
   export GEOGEBRA_PATH=/correct/path/to/geogebra
   ```

---

### Error: "ClassNotFoundException: org.geogebra.desktop.main.AppD"

**Cause:** Using GeoGebra 6 instead of GeoGebra 5

**Solution:** Download GeoGebra Classic 5 specifically:
- GeoGebra 6 uses different package structure
- Only GeoGebra 5 has `org.geogebra.desktop.main.AppD`

---

### Error: "No display / HeadlessException"

**Symptoms:**
```
java.awt.HeadlessException: 
No X11 DISPLAY variable was set
```

**Solutions:**

1. **If running remotely (SSH):**
   ```bash
   # Enable X11 forwarding
   ssh -X user@host
   
   # Or set display
   export DISPLAY=:0
   ```

2. **If on server without GUI:**
   ```bash
   # Install virtual display
   sudo apt-get install xvfb
   
   # Run with virtual framebuffer
   xvfb-run java -cp ... org.thundergrace.glyph.KenosisDemo
   ```

3. **Disable headless mode:**
   ```bash
   java -Djava.awt.headless=false -cp ...
   ```

---

### Error: "UnsatisfiedLinkError: Can't load library"

**Cause:** Native library incompatibility

**Solution:** Use pure Java mode:
```bash
java -Dawt.toolkit=sun.awt.X11.XToolkit -cp ...
```

---

### Error: "Build fails with encoding issues"

**Symptoms:** Special characters (￿, ·, ∅) show as gibberish

**Solution:** Set UTF-8 encoding:
```bash
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF-8"
```

---

### Performance Issues

**Symptoms:** Laggy drag, high CPU usage

**Solutions:**

1. **Reduce frame rate:**
   Edit `DragHandler.java`:
   ```java
   private double K = 0.05;  // Slower descent
   ```

2. **Simplify rendering:**
   Edit `GlyphRenderer.java`:
   ```java
   // Reduce curve complexity
   int numPoints = 3;  // Instead of 5
   ```

3. **Increase heap size:**
   ```bash
   java -Xmx512m -cp ...
   ```

---

### Drag Not Working

**Symptoms:** Cannot drag glyph elements

**Solutions:**

1. **Check element is selectable:**
   ```java
   point.setSelectionAllowed(true);
   point.setFixed(false);
   ```

2. **Verify mouse listeners attached:**
   Check console for `[INIT] Drag handler active`

3. **Check hit radius:**
   ```java
   if (dist < 0.5) {  // Increase if needed
       return geo;
   }
   ```

---

### Glyph Not Displaying

**Symptoms:** Empty canvas, no glyph visible

**Solutions:**

1. **Check view bounds:**
   ```java
   app.getEuclidianView1().setRealWorldCoordSystem(-5, 5, -5, 5);
   ```

2. **Verify elements added to construction:**
   ```java
   cons.addToConstructionList(geo, false);
   ```

3. **Force repaint:**
   ```java
   app.getKernel().notifyRepaint();
   ```

---

### RSTL State Not Changing

**Symptoms:** State stays at POTENTIAL, never ACTUALIZED

**Solutions:**

1. **Lower lock threshold:**
   Edit `DragHandler.java`:
   ```java
   // Lower from 10.0
   return totalEnergy > 5.0 && currentRSTLState == RSTLState.POTENTIAL;
   ```

2. **Drag more vigorously:**
   The lock requires sufficient energy descent

---

### Common Debug Commands

```bash
# Check Java version
java -version  # Should be 11+

# Check GeoGebra classes
jar tf $GEOGEBRA_PATH/geogebra.jar | grep "AppD"

# Verbose class loading
java -verbose:class -cp ... 2>&1 | grep geogebra

# Enable GeoGebra debug
java -Dgeogebra.debug=true -cp ...
```

---

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [TESTS.md](TESTS.md) - Testing procedures
- [mvp_glyph_converter.md](mvp_glyph_converter.md) - Python converter docs
- [vision_processor.md](vision_processor.md) - Vision processing docs
