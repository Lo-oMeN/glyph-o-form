# GLYPH-o-BETICS API REFERENCE
## Complete Programming Interface Documentation

**Version:** 2.1.0  
**Date:** 2026-03-06  
**Status:** Publication-Ready  

---

## TABLE OF CONTENTS

1. [Python API](#1-python-api)
   - [GlyphConverter](#glyphconverter)
   - [ConstellationBuilder](#constellationbuilder)
2. [Java API](#2-java-api)
   - [SimpleGlyph](#simpleglyph)
   - [GlyphRenderer](#glyphrenderer)
   - [DragHandler](#draghandler)
   - [KenosisDemo](#kenosisdemo)
3. [Command-Line Interface](#3-command-line-interface)
4. [Data Structures](#4-data-structures)
5. [Error Handling](#5-error-handling)

---

## 1. PYTHON API

### Module: `mvp_glyph_converter.py`

The Python implementation provides a complete command-line tool and importable library for English-to-glyph conversion.

#### GlyphConverter

Main class for transforming English words into 7-segment glyph representations.

```python
class GlyphConverter:
    """English → 7-Segment Glyph converter"""
```

##### Constructor

```python
converter = GlyphConverter()
```

**Parameters:** None

**Returns:** GlyphConverter instance

**Example:**
```python
from mvp_glyph_converter import GlyphConverter

converter = GlyphConverter()
```

---

##### `phonetic_descent(word: str) → List[str]`

Converts a word to atoms based on phonetic (sound) characteristics.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word` | str | English word to analyze |

**Returns:** `List[str]` — List of 7 atom characters

**Mapping Rules:**
| Phoneme Type | Atom | Examples |
|--------------|------|----------|
| Vowels | ￿ | a, e, i, o, u |
| Plosives | · | p, t, k, b, d, g |
| Fricatives | — | f, v, s, z, h |
| Nasals | ∅ | m, n |
| Liquids | ￿ | l, r |

**Example:**
```python
converter = GlyphConverter()
atoms = converter.phonetic_descent("LOVE")
# Returns: ['￿', '·', '￿', '￿', '—', '￿', '—']
```

---

##### `orthographic_descent(word: str) → List[str]`

Converts a word to atoms based on letter shapes (strokes).

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word` | str | English word to analyze |

**Returns:** `List[str]` — List of 7 atom characters

**Stroke Mapping:**
| Letter | Strokes | Atoms |
|--------|---------|-------|
| A | Two diagonals + cross | ['—', '—', '—'] |
| B | Vertical + two curves | ['—', '—', '￿'] |
| C | Single curve | ['￿'] |
| D | Vertical + curve | ['—', '￿'] |
| E | Three horizontals | ['—', '—', '—'] |
| L | Vertical + horizontal | ['—', '—'] |
| O | Closed curve | ['￿'] |
| V | Two diagonals | ['—', '—'] |

**Example:**
```python
converter = GlyphConverter()
atoms = converter.orthographic_descent("LOVE")
# Returns: ['—', '—', '￿', '—', '—', '—', '—']
```

---

##### `semantic_descent(word: str) → List[str]`

Converts a word to atoms based on semantic field and word characteristics.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word` | str | English word to analyze |

**Returns:** `List[str]` — List of 7 atom characters

**Heuristic Rules:**
- High vowel ratio (>40%) → Curve-dominant
- Medium vowel ratio (20-40%) → Mixed
- Low vowel ratio (<20%) → Line/Point-dominant

**Example:**
```python
converter = GlyphConverter()
atoms = converter.semantic_descent("LOVE")
# Returns: ['￿', '￿', '·', '∅', '—', '￿', '—']
```

---

##### `fuse_pathways(phonetic, orthographic, semantic) → str`

Fuses three descent pathways into final glyph using majority voting.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `phonetic` | List[str] | 7 atoms from phonetic analysis |
| `orthographic` | List[str] | 7 atoms from orthographic analysis |
| `semantic` | List[str] | 7 atoms from semantic analysis |

**Returns:** `str` — 7-character glyph string

**Fusion Rules:**
1. Count occurrences of each atom across pathways
2. Absence (∅) counts as 0.5 (kenotic bias)
3. Two ∅ votes → ∅ wins (kenotic amplification)
4. Ties broken by dominance: ￿ > — > · > ∅

**Example:**
```python
converter = GlyphConverter()
p = ['￿', '·', '￿', '￿', '—', '￿', '—']
o = ['—', '—', '￿', '—', '—', '—', '—']
s = ['￿', '￿', '·', '∅', '—', '￿', '—']

glyph = converter.fuse_pathways(p, o, s)
# Returns: "￿·￿∅—￿—"
```

---

##### `english_to_glyph(word: str) → str`

Complete transformation pipeline: English word → 7-segment glyph.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word` | str | English word to transform |

**Returns:** `str` — 7-character glyph string

**Example:**
```python
converter = GlyphConverter()

# Single word
glyph = converter.english_to_glyph("LOVE")
print(glyph)  # Output: "￿·￿∅—￿—"

# Multiple words
words = ["LOVE", "TRUTH", "FREEDOM"]
glyphs = {w: converter.english_to_glyph(w) for w in words}
# {'LOVE': '￿·￿∅—￿—', 'TRUTH': '·—·∅—￿—', ...}
```

---

##### `glyph_to_vector(glyph: str) → List[float]`

Converts glyph string to 28-dimensional one-hot vector.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `glyph` | str | 7-character glyph string |

**Returns:** `List[float]` — 28-dimensional vector

**Vector Structure:**
```
[a_point, a_line, a_curve, a_absence,
 b_point, b_line, b_curve, b_absence,
 ...
 g_point, g_line, g_curve, g_absence]
```

**Example:**
```python
converter = GlyphConverter()
vector = converter.glyph_to_vector("￿·￿∅—￿—")
# Returns: [0,0,1,0, 1,0,0,0, 0,0,1,0, 0,0,0,1, 0,1,0,0, 0,0,1,0, 0,1,0,0]
#             ↑a       ↑b       ↑c       ↑d       ↑e       ↑f       ↑g
```

---

##### `compute_resonance(word1: str, word2: str) → float`

Computes Looman resonance between two English words.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word1` | str | First English word |
| `word2` | str | Second English word |

**Returns:** `float` — Resonance score (0.0 to 1.0+)

**Resonance Components:**
- Vector similarity (cosine)
- Absence bonus (kenosis weighting)
- Curve flow (continuity)
- Golden ratio harmonic

**Example:**
```python
converter = GlyphConverter()

# High resonance (synonyms)
r = converter.compute_resonance("LOVE", "HEART")
print(f"{r:.3f}")  # Output: ~0.85

# Low resonance (antonyms)
r = converter.compute_resonance("LOVE", "HATE")
print(f"{r:.3f}")  # Output: ~0.25
```

---

##### `visualize_glyph(glyph: str, label: str = "") → str`

Creates ASCII art visualization of a glyph.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `glyph` | str | 7-character glyph string |
| `label` | str | Optional label for the glyph |

**Returns:** `str` — Multi-line ASCII art string

**Example:**
```python
converter = GlyphConverter()
art = converter.visualize_glyph("￿·￿∅—￿—", "LOVE")
print(art)
```

**Output:**
```
┌─ LOVE
│       ￿
│    ￿     ·
│       —
│    —     ￿
│       —
└──────────
```

---

##### `get_atom_breakdown(glyph: str) → Dict[str, str]`

Returns atom assignments for each segment.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `glyph` | str | 7-character glyph string |

**Returns:** `Dict[str, str]` — Mapping of segment to atom

**Example:**
```python
converter = GlyphConverter()
breakdown = converter.get_atom_breakdown("￿·￿∅—￿—")
# Returns: {'a': '￿', 'b': '·', 'c': '￿', 'd': '—', 'e': '—', 'f': '￿', 'g': '—'}
```

---

#### ConstellationBuilder

Class for compressing English words into stacked geometric glyphs and building constellations.

```python
class ConstellationBuilder:
    """Compress English words into stacked geometric glyphs"""
```

##### Constructor

```python
builder = ConstellationBuilder()
```

**Parameters:** None

**Returns:** ConstellationBuilder instance

---

##### `word_to_constellation(word: str) → dict`

Compresses a word into a single glyph using vertical stacking.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word` | str | English word to compress |

**Returns:** `dict` with keys:
| Key | Type | Description |
|-----|------|-------------|
| `word` | str | Original word |
| `glyph_string` | str | 7-character glyph |
| `letters` | List[dict] | Letter decompositions |
| `segments` | dict | Segment-to-atom mapping |

**Example:**
```python
builder = ConstellationBuilder()
result = builder.word_to_constellation("LOVE")

print(result['word'])        # "LOVE"
print(result['glyph_string']) # "￿￿￿——∅∅"
print(result['segments'])    # {'a': '￿', 'f': '￿', 'b': '￿', ...}
```

---

##### `draw_constellation(words: list) → str`

Creates ASCII visualization of multiple glyphs with connections.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `words` | List[str] | List of English words |

**Returns:** `str` — Multi-line ASCII constellation visualization

**Example:**
```python
builder = ConstellationBuilder()
print(builder.draw_constellation(["LOVE", "TRUTH", "FREEDOM"]))
```

---

### Constants

```python
# Four Atoms
ATOMS = ['·', '—', '￿', '∅']
ATOM_NAMES = ['Point', 'Line', 'Curve', 'Absence']

# 7-Segment Layout
SEGMENTS = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

# Segment positions for visualization
SEGMENT_POSITIONS = {
    'a': (0, 2, 6),  # row, col_start, col_end
    'b': (1, 6, 8),
    'c': (3, 6, 8),
    'd': (4, 2, 6),
    'e': (3, 0, 2),
    'f': (1, 0, 2),
    'g': (2, 2, 6)
}
```

---

## 2. JAVA API

### Module: `geogebra_mvp`

The Java implementation provides interactive glyph rendering on GeoGebra canvas.

#### SimpleGlyph

Core class representing a 7-segment lattice with atomic assignments.

```java
package org.thundergrace.glyph;

public class SimpleGlyph {
    // 28-dimensional vector: 7 segments × 4 atoms
    private double[] vector;
    private EnumMap<Segment, Atom> assignment;
    private String name;
}
```

##### Enums

**Atom:**
```java
public enum Atom {
    POINT("·", 0),
    LINE("—", 1),
    CURVE("￿", 2),
    ABSENCE("∅", 3);
    
    private final String symbol;
    private final int index;
}
```

**Segment:**
```java
public enum Segment {
    A(0, "top"),
    B(1, "upperRight"),
    C(2, "lowerRight"),
    D(3, "bottom"),
    E(4, "lowerLeft"),
    F(5, "upperLeft"),
    G(6, "middle");
    
    private final int index;
    private final String description;
}
```

##### Constructor

```java
public SimpleGlyph(String name)
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `name` | String | Glyph identifier (e.g., "KENOSIS") |

**Example:**
```java
SimpleGlyph customGlyph = new SimpleGlyph("CUSTOM");
```

---

##### `setAtom(Segment segment, Atom atom) → void`

Assigns an atom to a segment.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `segment` | Segment | Target segment (A-G) |
| `atom` | Atom | Atom to assign |

**Example:**
```java
SimpleGlyph glyph = new SimpleGlyph("CUSTOM");
glyph.setAtom(SimpleGlyph.Segment.A, SimpleGlyph.Atom.CURVE);
glyph.setAtom(SimpleGlyph.Segment.B, SimpleGlyph.Atom.POINT);
glyph.setAtom(SimpleGlyph.Segment.G, SimpleGlyph.Atom.LINE);
glyph.setAtom(SimpleGlyph.Segment.D, SimpleGlyph.Atom.LINE);
```

---

##### `getAtom(Segment segment) → Atom`

Retrieves the atom assigned to a segment.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `segment` | Segment | Target segment |

**Returns:** `Atom` — Assigned atom (defaults to ABSENCE)

**Example:**
```java
Atom atom = glyph.getAtom(SimpleGlyph.Segment.A);
// Returns: Atom.CURVE
```

---

##### `getVector() → double[]`

Returns the 28-dimensional vector representation.

**Returns:** `double[]` — Clone of internal vector

**Example:**
```java
double[] vector = glyph.getVector();
// Length: 28 elements
```

---

##### `computeResonance(SimpleGlyph other) → double`

Computes Looman resonance with another glyph.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `other` | SimpleGlyph | Glyph to compare with |

**Returns:** `double` — Resonance score (0.0 to 1.0+)

**Example:**
```java
SimpleGlyph kenosis = SimpleGlyph.createKENOSIS();
SimpleGlyph grace = SimpleGlyph.createGRACE();
double resonance = kenosis.computeResonance(grace);
// Returns: ~0.75
```

---

##### Static Factory Methods

```java
// Create the KENOSIS glyph: ￿·——
public static SimpleGlyph createKENOSIS()

// Create the GRACE glyph: ·￿——
public static SimpleGlyph createGRACE()
```

**Example:**
```java
SimpleGlyph kenosis = SimpleGlyph.createKENOSIS();
System.out.println(kenosis.getName());        // "KENOSIS"
System.out.println(kenosis.getAtomicSequence()); // "￿·——"
```

---

##### `toString() → String`

Returns string representation of the glyph.

**Returns:** `String` — "Name: atom sequence"

**Example:**
```java
System.out.println(glyph.toString());
// Output: "KENOSIS: ￿·——————"
```

---

#### GlyphRenderer

Renders atomic glyphs on GeoGebra canvas with draggable elements.

```java
package org.thundergrace.glyph;

public class GlyphRenderer {
    private AppD app;
    private Construction cons;
    private SimpleGlyph currentGlyph;
    private Map<SimpleGlyph.Segment, List<GeoElement>> segmentElements;
}
```

##### Constructor

```java
public GlyphRenderer(AppD app)
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `app` | AppD | GeoGebra application instance |

---

##### `render(SimpleGlyph glyph) → void`

Renders a glyph to the GeoGebra canvas.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `glyph` | SimpleGlyph | Glyph to render |

**Example:**
```java
AppD app = GeoGebra.create(args);
GlyphRenderer renderer = new GlyphRenderer(app);

SimpleGlyph kenosis = SimpleGlyph.createKENOSIS();
renderer.render(kenosis);
```

---

##### `clear() → void`

Clears all rendered elements from canvas.

**Example:**
```java
renderer.clear();  // Removes all glyph elements
```

---

##### `setScale(double scale) → void`

Sets the rendering scale.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `scale` | double | Scale factor (default: 100.0) |

**Example:**
```java
renderer.setScale(150.0);  // 1.5x larger
```

---

##### `setCenter(double x, double y) → void`

Sets the center position for rendering.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `x` | double | X coordinate |
| `y` | double | Y coordinate |

**Example:**
```java
renderer.setCenter(0, 0);     // Center at origin
renderer.setCenter(5, -3);    // Offset position
```

---

##### `getSegmentElements(Segment segment) → List<GeoElement>`

Gets rendered GeoGebra elements for a segment.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `segment` | Segment | Target segment |

**Returns:** `List<GeoElement>` — List of GeoGebra geometric objects

---

#### DragHandler

Handles mouse drag operations with free-energy descent control.

```java
package org.thundergrace.glyph;

public class DragHandler {
    public enum RSTLState {
        NULL,       // ∅ - Death, untangled
        POTENTIAL,  // △ - Elevating, becoming
        ACTUALIZED  // ■ - Locked glory
    }
}
```

##### Constructor

```java
public DragHandler(AppD app, GlyphRenderer renderer)
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `app` | AppD | GeoGebra application |
| `renderer` | GlyphRenderer | Associated renderer |

---

##### `setGlyph(SimpleGlyph glyph) → void`

Sets the glyph to handle drag operations for.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `glyph` | SimpleGlyph | Target glyph |

**Example:**
```java
DragHandler handler = new DragHandler(app, renderer);
handler.setGlyph(kenosisGlyph);
```

---

##### `getRSTLState() → RSTLState`

Returns current RSTL (trinary logic) state.

**Returns:** `RSTLState` — Current state (NULL, POTENTIAL, or ACTUALIZED)

**States:**
| State | Meaning |
|-------|---------|
| `NULL` | Initial/reset state |
| `POTENTIAL` | During drag operation |
| `ACTUALIZED` | After lock condition met |

---

##### `getStructuralEnergy() → double`

Returns accumulated structural energy during drag.

**Returns:** `double` — Energy value

---

##### `getConstraintEnergy() → double`

Returns accumulated constraint energy during drag.

**Returns:** `double` — Energy value

---

#### KenosisDemo

Main entry point for the GeoGebra demonstration.

```java
package org.thundergrace.glyph;

public class KenosisDemo {
    public static void main(String[] args)
}
```

**Usage:**
```bash
java -cp ".:geogebra.jar" org.thundergrace.glyph.KenosisDemo
```

**System Properties:**
```bash
java -Djava.awt.headless=false \
     -Dgeogebra.debug=false \
     org.thundergrace.glyph.KenosisDemo
```

---

## 3. COMMAND-LINE INTERFACE

### Python CLI

```bash
python mvp_glyph_converter.py [OPTIONS] <WORD> [WORD2 ...]
```

#### Single Word Mode

Display glyph visualization for one word:

```bash
python mvp_glyph_converter.py LOVE
```

**Output:**
```
============================================================
  GLYPH-o-BETICS CONVERSION
============================================================

  English Input: LOVE
  Glyph Output:  ￿·￿∅—￿—

  Descent Pathways:
    Phonetic:     ￿·￿￿—￿
    Orthographic: ——￿——— —
    Semantic:     ￿￿·∅—￿—
    ─────────────────────────
    Final (fused): ￿·￿∅—￿—

  Segment Mapping:
    a b c d e f g
    ￿ · ￿ — — ￿ —
```

#### Multi-Word Mode

Display glyphs and resonance matrix:

```bash
python mvp_glyph_converter.py LOVE TRUTH FREEDOM
```

**Output:**
```
============================================================
  GLYPH-o-BETICS RESONANCE ANALYSIS
============================================================

  LOVE       → ￿·￿∅—￿—
  TRUTH      → ·—·∅—￿—
  FREEDOM    → ￿—∅∅——

  Resonance Matrix
  ──────────────────────────────────────────────────────────
           LOVE   TRUTH  FREEDOM
  LOVE   │   1.00   0.45   0.62
  TRUTH  │   0.45   1.00   0.58
  FREEDOM│   0.62   0.58   1.00
```

#### Self-Test Mode

Run built-in validation tests:

```bash
python mvp_glyph_converter.py --test
```

---

## 4. DATA STRUCTURES

### Glyph Object (Python)

```python
{
    'word': str,              # Original English word
    'glyph_string': str,      # 7-character atom sequence
    'segments': {
        'a': str,             # Atom at segment a
        'b': str,             # Atom at segment b
        'c': str,             # Atom at segment c
        'd': str,             # Atom at segment d
        'e': str,             # Atom at segment e
        'f': str,             # Atom at segment f
        'g': str,             # Atom at segment g
    },
    'vector': List[float],    # 28-dimensional one-hot vector
}
```

### Compressed Glyph Format

```
Byte 1: [aa][ab][ag]  (atoms for a, b, g segments)
Byte 2: [af][ae][ac]  (atoms for f, e, c segments)
Byte 3: [ad][flags]   (atom for d segment + 4 flag bits)
```

**Atom Encoding:**
- 00 = ∅ (absence)
- 01 = · (point)
- 10 = — (line)
- 11 = ￿ (curve)

### Constellation Format

```python
{
    'version': int,
    'glyphs': List[dict],      # List of glyph objects
    'connections': List[dict], # Resonance connections
    'metadata': {
        'timestamp': str,
        'author': str,
        'mappings': dict,       # Word-to-glyph mappings
    }
}
```

---

## 5. ERROR HANDLING

### Python Exceptions

| Exception | Cause | Resolution |
|-----------|-------|------------|
| `ValueError` | Invalid atom in glyph string | Check input contains only ·—￿∅ |
| `IndexError` | Glyph string not 7 characters | Pad or truncate to exactly 7 |
| `TypeError` | Non-string word input | Convert to string before passing |

### Java Exceptions

| Exception | Cause | Resolution |
|-----------|-------|------------|
| `NullPointerException` | Null glyph passed to renderer | Initialize glyph before rendering |
| `IllegalArgumentException` | Invalid segment/atom enum | Use valid enum values |
| `ClassCastException` | Wrong GeoGebra element type | Check element type before casting |

---

## APPENDIX: IMPORT EXAMPLES

### Python

```python
# Import main converter
from mvp_glyph_converter import GlyphConverter, ConstellationBuilder

# Import constants
from mvp_glyph_converter import ATOMS, SEGMENTS, ATOM_NAMES

# Use in code
converter = GlyphConverter()
glyph = converter.english_to_glyph("LOVE")
```

### Java

```java
// Import all glyph classes
import org.thundergrace.glyph.SimpleGlyph;
import org.thundergrace.glyph.GlyphRenderer;
import org.thundergrace.glyph.DragHandler;
import org.thundergrace.glyph.KenosisDemo;

// Use in code
SimpleGlyph glyph = SimpleGlyph.createKENOSIS();
```

---

*"Code is the loom. The API is the pattern. Weave carefully."*

**End of API Reference**
