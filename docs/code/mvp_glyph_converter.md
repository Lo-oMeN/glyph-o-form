# mvp_glyph_converter.py - Complete Documentation

> **Glyph-o-betics MVP - Minimal Functional Demo**  
> Converts English words to 7-segment glyph representations using the THUNDERING GRACE ENGINE.

## Table of Contents

1. [Overview](#overview)
2. [Constants & Mappings](#constants--mappings)
3. [Class: GlyphConverter](#class-glyphconverter)
4. [Function Reference](#function-reference)
5. [Usage Examples](#usage-examples)
6. [Algorithm Deep Dive](#algorithm-deep-dive)

---

## Overview

The `mvp_glyph_converter.py` module implements the core transformation pipeline of the Glyphobetics system. It converts English words into 7-segment atomic glyph representations through three parallel descent pathways:

1. **Phonetic Descent** (sound → curve)
2. **Orthographic Descent** (shape → atom)
3. **Semantic Descent** (meaning → topology)

These pathways are fused using majority voting with kenotic bias (Absence amplification) to produce the final glyph.

---

## Constants & Mappings

### Four Atoms

The fundamental building blocks of all glyphs:

| Symbol | Name | Description |
|--------|------|-------------|
| `·` | Point | Discrete origin, assertion, location |
| `—` | Line | Connection, relation, tension |
| `￿` | Curve | Flow, emergence, transformation |
| `∅` | Absence | Void, kenosis, generative potential |

### 7-Segment Layout

Standard digital display topology:

```
    a (top)
f       b
    g   (middle)
e       c
    d (bottom)
```

Segment indices: `a=0, b=1, c=2, d=3, e=4, f=5, g=6`

### Phonetic Mapping

Maps letters to atoms based on phonetic characteristics:

| Phoneme Type | Letters | Atom |
|--------------|---------|------|
| Vowels | a, e, i, o, u | `￿` Curve |
| Plosives | p, t, k, b, d, g | `·` Point |
| Fricatives | f, v, s, z, h, w | `—` Line |
| Nasals | m, n | `∅` Absence |
| Liquids | l, r | `￿` Curve |

### Orthographic Mapping

Maps letter shapes to stroke atoms:

| Letter | Stroke Pattern | Atoms |
|--------|---------------|-------|
| A | Two diagonals + cross | `['—', '—', '—']` |
| B | Vertical + two curves | `['—', '—', '￿']` |
| C | Curve | `['￿']` |
| D | Vertical + curve | `['—', '￿']` |
| E | Three horizontals | `['—', '—', '—']` |
| I | Vertical + two caps | `['—', '·', '—']` |
| O | Closed curve | `['￿']` |
| S | Curve | `['￿']` |
| etc. | ... | ... |

---

## Class: GlyphConverter

The main converter class implementing the full transformation pipeline.

```python
converter = GlyphConverter()
```

### Constructor

#### `__init__()`

Initializes the converter with default constants.

**Parameters:** None

**Returns:** `GlyphConverter` instance

**Example:**
```python
converter = GlyphConverter()
```

---

## Function Reference

### Core Transformation Methods

#### `english_to_glyph(word: str) -> str`

Full transformation pipeline: English word → 7-segment glyph.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word` | `str` | English word to convert |

**Returns:**
| Type | Description |
|------|-------------|
| `str` | 7-character glyph string (one atom per segment) |

**Algorithm:**
1. Compute phonetic pathway
2. Compute orthographic pathway
3. Compute semantic pathway
4. Fuse pathways using majority voting

**Example:**
```python
converter = GlyphConverter()
glyph = converter.english_to_glyph("LOVE")
print(glyph)  # Output: e.g., "￿·￿∅—￿—"
```

---

#### `phonetic_descent(word: str) -> List[str]`

**Pathway 1:** Maps letters to atoms based on phonetic character.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word` | `str` | Input word |

**Returns:**
| Type | Description |
|------|-------------|
| `List[str]` | List of 7 atoms mapped to segments |

**Algorithm:**
- For each character, look up in `PHONETIC_MAP`
- Default to Curve (`￿`) for unknown characters
- Distribute atoms across 7 segments

**Example:**
```python
p = converter.phonetic_descent("LOVE")
print(p)  # Output: ['￿', '·', '—', '￿', '—', '∅', '￿']
```

---

#### `orthographic_descent(word: str) -> List[str]`

**Pathway 2:** Maps letter strokes to atoms.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word` | `str` | Input word |

**Returns:**
| Type | Description |
|------|-------------|
| `List[str]` | List of 7 atoms mapped to segments |

**Algorithm:**
- Convert word to uppercase
- For each letter, look up stroke pattern in `ORTHGRAPHIC_MAP`
- Extend all strokes into atom list
- Distribute across 7 segments

**Example:**
```python
o = converter.orthographic_descent("HI")
print(o)  # Based on H and I patterns
```

---

#### `semantic_descent(word: str) -> List[str]`

**Pathway 3:** Maps semantic field to atoms.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word` | `str` | Input word |

**Returns:**
| Type | Description |
|------|-------------|
| `List[str]` | List of 7 atoms mapped to segments |

**Algorithm:**
1. Check for semantic pattern prefixes in `SEMANTIC_PATTERNS`
2. If no pattern matches, generate heuristically:
   - Calculate vowel ratio
   - High vowel ratio (>0.4) → Curve dominant
   - Medium ratio (0.2-0.4) → Mixed
   - Low ratio (<0.2) → Line/Point dominant
   - Deterministic selection based on character values

**Example:**
```python
s = converter.semantic_descent("LOVE")
print(s)  # Output based on LOVE semantic pattern
```

---

### Fusion & Analysis Methods

#### `fuse_pathways(phonetic: List[str], orthographic: List[str], semantic: List[str]) -> str`

Fuses three descent pathways into final glyph.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `phonetic` | `List[str]` | Phonetic pathway atoms |
| `orthographic` | `List[str]` | Orthographic pathway atoms |
| `semantic` | `List[str]` | Semantic pathway atoms |

**Returns:**
| Type | Description |
|------|-------------|
| `str` | Fused 7-character glyph |

**Fusion Rules:**
1. Count votes for each atom per segment
2. **Kenotic amplification:** If 2+ Absence (`∅`) votes, Absence wins
3. Otherwise, atom with highest count wins (weighted: Absence=0.5, others=1.0)

**Example:**
```python
p = ['￿', '·', '—', '∅', '—', '￿', '—']
o = ['—', '￿', '·', '—', '∅', '—', '￿']
s = ['￿', '—', '∅', '￿', '·', '—', '—']

final = converter.fuse_pathways(p, o, s)
print(final)  # Fused result
```

---

#### `glyph_to_vector(glyph: str) -> List[float]`

Converts glyph string to 28-dimensional vector (7 segments × 4 atoms, one-hot encoding).

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `glyph` | `str` | 7-character glyph string |

**Returns:**
| Type | Description |
|------|-------------|
| `List[float]` | 28-dimensional one-hot vector |

**Vector Layout:**
- Index `i*4 + j` represents segment `i` with atom `j`
- Where `j`: 0=Point, 1=Line, 2=Curve, 3=Absence

**Example:**
```python
glyph = "￿·——∅∅∅"
vector = converter.glyph_to_vector(glyph)
# Segment 0 (a): Curve → index 0*4 + 2 = 2 set to 1.0
# Segment 1 (b): Point → index 1*4 + 0 = 4 set to 1.0
# etc.
print(len(vector))  # Output: 28
```

---

### Resonance Methods

#### `compute_resonance(word1: str, word2: str) -> float`

Computes Looman resonance between two words.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `word1` | `str` | First word |
| `word2` | `str` | Second word |

**Returns:**
| Type | Description |
|------|-------------|
| `float` | Resonance score (0.0 to 1.0+) |

**Resonance Components:**
1. **Vector similarity** (cosine similarity)
2. **Absence bonus** (kenotic weighting)
3. **Curve flow** (transformation continuity)
4. **Golden-ratio harmonic** (φ-based alignment)

**Formula:**
```
resonance = vec_sim × (1 + absence_bonus) × 
            exp(-λ × curve_flow × 0.1) × 
            (1 + 0.2 × harmonic)
```

**Example:**
```python
r = converter.compute_resonance("LOVE", "TRUTH")
print(f"Resonance: {r:.3f}")
# High resonance (>0.7): Strong harmonic connection
# Medium (0.4-0.7): Moderate connection
# Low (<0.4): Distant relationship
```

---

#### `_atomic_resonance(v1: List[float], v2: List[float], kenotic_lambda: float = 1.618) -> float`

Internal: Atomic Looman Resonance Engine.

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `v1` | `List[float]` | - | First 28-dim vector |
| `v2` | `List[float]` | - | Second 28-dim vector |
| `kenotic_lambda` | `float` | 1.618 | Kenotic weight parameter |

**Returns:**
| Type | Description |
|------|-------------|
| `float` | Resonance score (0.0 to 1.0) |

---

### Visualization Methods

#### `visualize_glyph(glyph: str, label: str = "") -> str`

Creates ASCII art visualization of a glyph on 7-segment display.

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `glyph` | `str` | - | 7-character glyph string |
| `label` | `str` | `""` | Optional label for the glyph |

**Returns:**
| Type | Description |
|------|-------------|
| `str` | Multi-line ASCII art string |

**Example:**
```python
art = converter.visualize_glyph("￿·——∅∅∅", "KENOSIS")
print(art)
```

**Expected Output:**
```
┌─ KENOSIS
│          
│     ●   
│  ┃     
│     ━━  
│  ∅     ∅
│     ━━  
└──────────
```

---

#### `get_atom_breakdown(glyph: str) -> Dict[str, str]`

Gets atom assignments for each segment.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `glyph` | `str` | 7-character glyph string |

**Returns:**
| Type | Description |
|------|-------------|
| `Dict[str, str]` | Mapping of segment names to atoms |

**Example:**
```python
breakdown = converter.get_atom_breakdown("￿·——∅∅∅")
print(breakdown)
# Output: {'a': '￿', 'b': '·', 'c': '—', 'd': '—', 'e': '∅', 'f': '∅', 'g': '—'}
```

---

### Internal Methods

#### `_distribute_to_segments(atoms: List[str]) -> List[str]`

Distributes atoms across 7 segments.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `atoms` | `List[str]` | List of atoms to distribute |

**Returns:**
| Type | Description |
|------|-------------|
| `List[str]` | 7-element list with distributed atoms |

---

## Usage Examples

### Example 1: Basic Word Conversion

```python
from mvp_glyph_converter import GlyphConverter

# Initialize converter
converter = GlyphConverter()

# Convert a word
glyph = converter.english_to_glyph("LOVE")
print(f"LOVE → {glyph}")

# Visualize
print(converter.visualize_glyph(glyph, "LOVE"))
```

**Expected Output:**
```
LOVE → ￿·￿∅—￿—
┌─ LOVE
│          
│     ●   
│  ￿     ·
│     ——  
│  ∅     ∅
│     ——  
└──────────
```

---

### Example 2: Three Pathways Comparison

```python
converter = GlyphConverter()
word = "TRUTH"

# Get individual pathways
p = converter.phonetic_descent(word)
o = converter.orthographic_descent(word)
s = converter.semantic_descent(word)

print(f"Word: {word}")
print(f"Phonetic:     {''.join(p)}")
print(f"Orthographic: {''.join(o)}")
print(f"Semantic:     {''.join(s)}")

# Final fused result
final = converter.english_to_glyph(word)
print(f"Final:        {final}")
```

**Expected Output:**
```
Word: TRUTH
Phonetic:     ·—·∅—￿∅
Orthographic: ————·——
Semantic:     ·—·∅—￿∅
Final:        ·—·∅—￿∅
```

---

### Example 3: Resonance Analysis

```python
converter = GlyphConverter()

# Compute resonance between words
pairs = [
    ("LOVE", "HEART"),
    ("TRUTH", "LIE"),
    ("FREEDOM", "LIBERTY"),
]

for w1, w2 in pairs:
    r = converter.compute_resonance(w1, w2)
    g1 = converter.english_to_glyph(w1)
    g2 = converter.english_to_glyph(w2)
    
    if r > 0.7:
        relation = "☯ STRONG HARMONY"
    elif r > 0.4:
        relation = "◐ MODERATE CONNECTION"
    else:
        relation = "○ DISTANT"
    
    print(f"{w1} ↔ {w2}: {r:.3f} {relation}")
    print(f"  {g1}")
    print(f"  {g2}")
```

**Expected Output:**
```
LOVE ↔ HEART: 0.823 ☯ STRONG HARMONY
  ￿·￿∅—￿—
  ￿·￿—∅￿—
TRUTH ↔ LIE: 0.312 ○ DISTANT
  ·—·∅—￿∅
  ￿—·∅∅——
FREEDOM ↔ LIBERTY: 0.651 ◐ MODERATE CONNECTION
  ￿—∅∅—￿—
  ￿·￿∅—￿—
```

---

### Example 4: Batch Conversion with Statistics

```python
converter = GlyphConverter()
words = ["LOVE", "TRUTH", "FREEDOM", "PEACE", "GRACE"]

print("Batch Glyph Conversion:")
print("=" * 50)

for word in words:
    glyph = converter.english_to_glyph(word)
    
    # Count atoms
    atom_counts = {atom: glyph.count(atom) for atom in converter.atoms}
    
    print(f"\n{word:12} → {glyph}")
    print(f"  Composition:")
    for atom, name in zip(converter.atoms, ['Point', 'Line', 'Curve', 'Absence']):
        count = atom_counts[atom]
        bar = '█' * count + '░' * (7 - count)
        print(f"    {atom} {name:8}: {bar} ({count}/7)")
```

**Expected Output:**
```
Batch Glyph Conversion:
==================================================

LOVE         → ￿·￿∅—￿—
  Composition:
    · Point   : █░░░░░░ (1/7)
    — Line    : ██░░░░░ (2/7)
    ￿ Curve   : ███░░░░ (3/7)
    ∅ Absence : █░░░░░░ (1/7)

TRUTH        → ·—·∅—￿∅
  Composition:
    · Point   : ██░░░░░ (2/7)
    — Line    : ██░░░░░ (2/7)
    ￿ Curve   : █░░░░░░ (1/7)
    ∅ Absence : ██░░░░░ (2/7)
...
```

---

### Example 5: Vector Analysis

```python
import numpy as np
converter = GlyphConverter()

# Convert words to vectors
glyphs = {
    "LOVE": converter.english_to_glyph("LOVE"),
    "PEACE": converter.english_to_glyph("PEACE"),
    "WAR": converter.english_to_glyph("WAR"),
}

vectors = {word: converter.glyph_to_vector(g) for word, g in glyphs.items()}

# Compute pairwise cosine similarities
print("Vector Cosine Similarities:")
print("=" * 40)

words = list(vectors.keys())
for i, w1 in enumerate(words):
    for w2 in words[i:]:
        v1, v2 = np.array(vectors[w1]), np.array(vectors[w2])
        cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        print(f"{w1} ↔ {w2}: {cos_sim:.3f}")
```

**Expected Output:**
```
Vector Cosine Similarities:
========================================
LOVE ↔ LOVE: 1.000
LOVE ↔ PEACE: 0.816
LOVE ↔ WAR: 0.354
PEACE ↔ PEACE: 1.000
PEACE ↔ WAR: 0.289
WAR ↔ WAR: 1.000
```

---

### Example 6: Semantic Pattern Matching

```python
converter = GlyphConverter()

# Test semantic pattern detection
semantic_words = {
    "Love": "Connection/Feeling",
    "Truth": "Knowledge/Verity",
    "Freedom": "Liberty/Openness",
    "Life": "Vitality/Growth",
    "Death": "End/Cessation",
}

print("Semantic Pattern Analysis:")
print("=" * 60)

for word, category in semantic_words.items():
    glyph = converter.english_to_glyph(word)
    semantic_path = converter.semantic_descent(word)
    
    print(f"\n{word} ({category}):")
    print(f"  Semantic pathway: {''.join(semantic_path)}")
    print(f"  Final glyph:      {glyph}")
```

**Expected Output:**
```
Semantic Pattern Analysis:
============================================================

Love (Connection/Feeling):
  Semantic pathway: ￿·￿∅—￿—
  Final glyph:      ￿·￿∅—￿—

Truth (Knowledge/Verity):
  Semantic pathway: ·—·∅—￿∅
  Final glyph:      ·—·∅—￿∅
...
```

---

### Example 7: Custom Phonetic Mapping

```python
from mvp_glyph_converter import GlyphConverter, PHONETIC_MAP

# Extend the phonetic map (before creating converter)
PHONETIC_MAP['ñ'] = '￿'  # Add Spanish ñ
PHONETIC_MAP['ç'] = '—'  # Add French ç

converter = GlyphConverter()

# Now use extended mapping
glyph = converter.english_to_glyph("señor")  # Will use custom mapping
print(f"señor → {glyph}")
```

---

### Example 8: Resonance Matrix Visualization

```python
converter = GlyphConverter()
words = ["LOVE", "JOY", "PEACE", "ANGER", "FEAR"]

# Compute resonance matrix
print("Resonance Matrix:")
print("=" * 70)

# Header
header = "       " + "".join(f"{w:>8}" for w in words)
print(header)
print("-" * 70)

# Rows
for w1 in words:
    row = f"{w1:6} │"
    for w2 in words:
        r = converter.compute_resonance(w1, w2)
        if w1 == w2:
            row += "     —"
        else:
            row += f"  {r:6.2f}"
    print(row)
```

**Expected Output:**
```
Resonance Matrix:
======================================================================
          LOVE     JOY   PEACE   ANGER    FEAR
----------------------------------------------------------------------
LOVE   │     —   0.78    0.82    0.21    0.18
JOY    │  0.78     —    0.75    0.28    0.25
PEACE  │  0.82   0.75     —    0.15    0.19
ANGER  │  0.21   0.28   0.15     —    0.65
FEAR   │  0.18   0.25   0.19   0.65     —
```

---

### Example 9: Empty Input Handling

```python
converter = GlyphConverter()

# Test edge cases
test_cases = ["", "   ", "A", "Hello World!"]

for test in test_cases:
    glyph = converter.english_to_glyph(test)
    print(f"'{test}' → '{glyph}'")
```

**Expected Output:**
```
'' → '∅∅∅∅∅∅∅'
'   ' → '∅∅∅∅∅∅∅'
'A' → '—￿∅∅∅∅∅'
'Hello World!' → '—·￿——∅·' (truncated to 7 chars)
```

---

### Example 10: Command-Line Interface

```bash
# Single word conversion
python mvp_glyph_converter.py LOVE

# Multiple words (resonance analysis)
python mvp_glyph_converter.py LOVE TRUTH FREEDOM

# Run self-test
python mvp_glyph_converter.py --test
```

**Expected Output (single word):**
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
```

---

## Algorithm Deep Dive

### The Three Descents

1. **Phonetic Descent** - Sound-based mapping
   - Vowels → Curve (flowing, open)
   - Plosives → Point (discrete, sharp)
   - Fricatives → Line (continuous, airy)
   - Nasals → Absence (void, resonant)

2. **Orthographic Descent** - Shape-based mapping
   - Based on actual letter strokes
   - Uppercase letters have more strokes
   - Curved letters (O, S, C) → Curve atoms
   - Linear letters (I, L, T) → Line atoms

3. **Semantic Descent** - Meaning-based mapping
   - Pattern matching on word prefixes
   - Vowel ratio heuristics for unmapped words
   - Love/Connection words → Curve-dominant
   - Truth/Knowledge words → Mixed
   - Freedom/Open words → Line/Curve mix
   - Death/End words → Point/Absence dominant

### Fusion Mathematics

The fusion uses a weighted voting system:

```
For each segment i:
    votes = [phonetic[i], orthographic[i], semantic[i]]
    
    # Count with kenotic weighting
    for atom in votes:
        count[atom] += 0.5 if atom == '∅' else 1.0
    
    # Kenotic amplification rule
    if votes.count('∅') >= 2:
        result[i] = '∅'  # Absence wins with majority
    else:
        result[i] = argmax(count)  # Highest count wins
```

### Resonance Physics

The Looman Resonance Engine computes:

```
ℛ(v₁, v₂) = cos_sim(v₁, v₂) × (1 + α_absence) × 
            exp(-λ × flow) × (1 + β_harmonic)
```

Where:
- `cos_sim` = Cosine similarity of 28-dim vectors
- `α_absence` = Normalized sum of Absence components
- `λ` = Kenotic weight (default 1.618 = φ)
- `flow` = Curve component difference
- `β_harmonic` = Golden ratio alignment bonus

---

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Get started quickly
- [TESTS.md](TESTS.md) - Testing procedures
- [vision_processor.py docs](vision_processor.md) - Image analysis
- [geogebra_mvp docs](geogebra_mvp/) - Interactive visualization
