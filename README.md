# Glyph-o-betics MVP

**English → 7-Segment Glyph Converter**

A minimal functional demo of the Glyph-o-betics system, implementing the 4-atom (Point ·, Line —, Curve ￿, Absence ∅) composition on a 7-segment lattice.

## Features

- **Three Descent Pathways**: Phonetic, Orthographic, and Semantic transformation
- **Atomic Resonance Engine**: Computes similarity between glyphs using 28-dimensional vectors
- **7-Segment Visualization**: ASCII art display of glyphs
- **Resonance Matrix**: Compare multiple words for glyph harmony

## Installation

No installation required. Just Python 3.6+.

```bash
# Verify Python version
python3 --version
```

## Usage

### Single Word Conversion

```bash
python3 mvp_glyph_converter.py LOVE
```

Output shows:
- The 7-segment glyph representation
- All three descent pathways
- Segment mapping
- ASCII visualization
- Atom composition breakdown

### Multiple Word Resonance Analysis

```bash
python3 mvp_glyph_converter.py LOVE TRUTH FREEDOM
```

Output shows:
- Individual glyphs for each word
- ASCII visualizations
- Resonance matrix
- Pair analysis with relationship classification

### Self-Test

```bash
python3 mvp_glyph_converter.py --test
```

## Test Examples

### LOVE
```
English Input: LOVE
Glyph Output:  ￿￿￿￿———

Segment Mapping:
  a b c d e f g
  ￿ ￿ ￿ ￿ — — —

[Visualization]
```

### TRUTH
```
English Input: TRUTH
Glyph Output:  ·—￿·—￿∅

Segment Mapping:
  a b c d e f g
  · — ￿ · — ￿ ∅
```

### FREEDOM
```
English Input: FREEDOM
Glyph Output:  ——￿￿·￿—

Segment Mapping:
  a b c d e f g
  — — ￿ ￿ · ￿ —
```

## Resonance Scoring

The Looman Resonance Engine computes similarity (0.0 to 1.0) between words:

| Score | Classification |
|-------|----------------|
| > 0.7 | ☯ Strong Harmony |
| 0.4-0.7 | ◐ Moderate Connection |
| < 0.4 | ○ Distant |

## Technical Details

### 4 Atoms
- **· Point** (U+00B7): Position, singularity, focus
- **— Line** (U+2014): Directionality, connection, assertion
- **￿ Curve** (U+FFFF): Continuity, flow, transformation
- **∅ Absence** (U+2205): Void, negative space, generative silence

### 7-Segment Lattice
```
   a
f     b
   g
e     c
   d
```

### Resonance Formula
Based on vector similarity, kenotic absence weighting, and golden-ratio harmonics.

## File Structure

```
mvp_glyph_converter.py    # Main executable script
README.md                  # This file
```

## License

Part of the Glyph-o-betics research initiative.

---

*"The atom speaks. The lattice breathes. The crystal is executable."*
