# GLYPH-o-BETICS TECHNICAL SPECIFICATION
## Unified Comprehensive Document

**Version:** 2.1.0  
**Date:** 2026-03-06  
**Status:** Publication-Ready  
**Classification:** Open Source (MIT License)  

---

## TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [Core Concepts](#2-core-concepts)
3. [Atomic Foundation](#3-atomic-foundation)
4. [The 7-Segment Lattice](#4-the-7-segment-lattice)
5. [English-to-Glyph Protocol](#5-english-to-glyph-protocol)
6. [Constellation Protocol](#6-constellation-protocol)
7. [Keyboard & Compression Protocol](#7-keyboard--compression-protocol)
8. [Resonance Engine](#8-resonance-engine)
9. [Reference Glyphs](#9-reference-glyphs)
10. [Version History](#10-version-history)

---

## 1. INTRODUCTION

### 1.1 Purpose

Glyph-o-betics is a universal language visualization framework that transforms semantic content into geometric representations. By decomposing meaning into atomic visual elements, we enable:

- **Cross-linguistic visualization** — See meaning across language barriers
- **AI interpretability** — Human-readable vector spaces for machine learning
- **Educational resources** — Teaching language structure through geometry
- **Accessibility tools** — Alternative representation for visual thinkers

### 1.2 Design Principles

| Principle | Description |
|-----------|-------------|
| **Atomic Composition** | All glyphs composed from 4 fundamental atoms |
| **Topological Structure** | 7-segment lattice as canonical canvas |
| **Multi-Pathway Descent** | Phonetic, orthographic, and semantic transformation paths |
| **Kenotic Dynamics** | Absence (∅) as generative, not empty |
| **Computational Tractability** | 28-dimensional vector representation for all glyphs |

### 1.3 Document Scope

This specification unifies four protocol documents:
- Glyph-o-betics v2.0 Core Specification
- English→Glyph-o-Form Transformation Protocol
- Constellation Word Compression Protocol
- Keyboard Interface & Compression Protocol

---

## 2. CORE CONCEPTS

### 2.1 The Descent Model

Unlike traditional translation (word → word), Glyph-o-betics uses **descent** (word → vector → glyph):

```
English Word
     ↓
[Phonetic Analysis] ──┐
[Orthographic Analysis] ├→ 28-dim Vector Space
[Semantic Analysis] ──┘
     ↓
7-Segment Glyph (7 atoms)
     ↓
Constellation (connected glyphs)
```

### 2.2 Key Terminology

| Term | Definition |
|------|------------|
| **Atom** | Fundamental geometric primitive (·, —, ￿, ∅) |
| **Glyph** | 7-segment assignment of atoms representing a word |
| **Constellation** | Network of connected glyphs with resonance relationships |
| **Resonance** | Geometric similarity score between glyphs (0.0 to 1.0+) |
| **Descent** | Transformation from English to glyph representation |
| **Kenosis** | Self-emptying process; absence as generative potential |

### 2.3 Mathematical Foundation

**Glyph Vector Space:**
- Dimension: 28 (7 segments × 4 atoms)
- Basis: One-hot encoding per segment-atom pair
- Metric: Looman resonance (cosine similarity + kenotic terms)

**Resonance Function:**
```
R(g₁, g₂) = cos_sim(g₁, g₂) × (1 + absence_bonus) × harmonic_term
```

---

## 3. ATOMIC FOUNDATION

### 3.1 The Four Atoms

All glyphs are composed from exactly four atomic primitives:

| Atom | Symbol | Unicode | Geometric Function | Kenotic Role |
|------|--------|---------|-------------------|--------------|
| **Point** | · | U+00B7 | Focus, singularity, seed | Origin of assertion |
| **Line** | — | U+2014 | Directionality, connection | Tension generator |
| **Curve** | ￿ | U+FFFD | Continuity, flow, transformation | Dimensional decompressor |
| **Absence** | ∅ | U+2205 | Void, negative space, potential | Generative silence |

### 3.2 Atom Properties

**Visual Characteristics:**
- Point: Discrete, localized, intense
- Line: Extended, directional, tense
- Curve: Continuous, flowing, transformative
- Absence: Implicit, generative, potential

**Algebraic Properties:**
- Commutative: Order of composition doesn't affect final glyph
- Idempotent: Multiple same-atoms on one segment collapse to single atom
- Dominance Hierarchy: Curve > Line > Point > Absence (when merging)

### 3.3 Atom Vector Encoding

Each atom maps to a 4-dimensional one-hot vector:

```
Point  (·) → [1, 0, 0, 0]
Line   (—) → [0, 1, 0, 0]
Curve  (￿) → [0, 0, 1, 0]
Absence(∅) → [0, 0, 0, 1]
```

---

## 4. THE 7-SEGMENT LATTICE

### 4.1 Canonical Layout

The standard digital-display topology serves as the geometric canvas:

```
        a (top)
   f         b
   (upper   (upper
    left)    right)
        g (middle)
   e         c
   (lower   (lower
    left)    right)
        d (bottom)
```

### 4.2 Segment Positions

| Segment | Position | Coordinate (normalized) |
|---------|----------|------------------------|
| a | Top horizontal | (0, 1) |
| b | Upper right vertical | (0.5, 0.5) |
| c | Lower right vertical | (0.5, -0.5) |
| d | Bottom horizontal | (0, -1) |
| e | Lower left vertical | (-0.5, -0.5) |
| f | Upper left vertical | (-0.5, 0.5) |
| g | Middle horizontal | (0, 0) |

### 4.3 Glyph String Representation

Glyphs are serialized as 7-character strings in segment order:

```
Glyph String: "￿·￿——∅∅"

Mapping:
  a → ￿ (Curve)
  b → · (Point)
  c → ￿ (Curve)
  d → — (Line)
  e → — (Line)
  f → ∅ (Absence)
  g → ∅ (Absence)
```

### 4.4 28-Dimensional Vector Representation

For computational processing, each glyph expands to a 28-dimensional vector:

```
G = [a_point, a_line, a_curve, a_absence,
     b_point, b_line, b_curve, b_absence,
     c_point, c_line, c_curve, c_absence,
     d_point, d_line, d_curve, d_absence,
     e_point, e_line, e_curve, e_absence,
     f_point, f_line, f_curve, f_absence,
     g_point, g_line, g_curve, g_absence]
```

**Example:** LOVE glyph "￿·￿——∅∅" becomes:
```
[0,0,1,0,  1,0,0,0,  0,0,1,0,  0,1,0,0,  0,1,0,0,  0,0,0,1,  0,0,0,1]
       ↑a       ↑b       ↑c       ↑d       ↑e       ↑f       ↑g
```

---

## 5. ENGLISH-TO-GLYPH PROTOCOL

### 5.1 Three Descent Pathways

Every English word transforms through three parallel analyses:

| Pathway | Input | Process | Output Characteristics |
|---------|-------|---------|----------------------|
| **Phonetic** | Sound pattern | Spectral analysis → atom mapping | Curve-dominant for vowels |
| **Orthographic** | Letter shapes | Stroke decomposition | Line/Point for structure |
| **Semantic** | Word meaning | Embedding projection | Context-dependent mix |

### 5.2 Phonetic Descent

**Phoneme-to-Atom Mapping:**

| Phoneme Class | Examples | Atom | Rationale |
|--------------|----------|------|-----------|
| Vowels | a, e, i, o, u | ￿ | Open, flowing, continuous |
| Plosives | p, t, k, b, d, g | · | Sharp, discrete, points |
| Fricatives | f, s, sh, th | — | Sustained, directional |
| Nasals | m, n, ng | ∅ | Resonant, enclosed |
| Liquids | l, r | ￿· | Transitional, curve-point |

**Example: "LOVE" (/lʌv/)**
```
/l/ → Liquid → ￿·
/ʌ/ → Vowel → ￿
/v/ → Fricative → —

Phonetic Glyph: ￿·￿—
```

### 5.3 Orthographic Descent

**Letter Stroke Decomposition:**

| Letter | Strokes | Atoms |
|--------|---------|-------|
| A | Two diagonals + cross | — + — + — |
| B | Vertical + two curves | — + ￿ + ￿ |
| C | Single curve | ￿ |
| D | Vertical + curve | — + ￿ |
| E | Three horizontals | — + — + — |
| L | Vertical + horizontal | — + — |
| O | Closed curve | ￿ |
| V | Two diagonals | — + — |

**Example: "LOVE"**
```
L → | + — → — + —
O → ○ → ￿
V → ∨ → — + —
E → ⅀ → — + — + —

Orthographic Glyph: ——￿——— —
```

### 5.4 Semantic Descent

**Word Embedding Projection:**

Standard word embeddings (300-dim) project to 28-dim glyph space via learned transformation:

```
glyph_vector = σ(W · word_embedding + b)

Where:
  σ = sigmoid activation
  W = 300 × 28 projection matrix
  b = kenotic bias term
```

**Semantic Field Signatures:**

| Semantic Field | Dominant Atoms | Glyph Pattern |
|---------------|----------------|---------------|
| Love/Connection | ￿· | Opening, connection |
| Truth/Knowledge | ·— | Focus, assertion |
| Freedom/Space | —∅ | Direction, openness |
| Transformation | ￿— | Flow resolving into structure |
| Death/Void | ∅∅ | Double absence, potential |

### 5.5 Superposition Fusion

The three pathway outputs fuse via majority voting with kenotic amplification:

**Fusion Rules:**
1. For each segment, count atom occurrences across pathways
2. Absence (∅) counts as 0.5 unless two pathways agree (then 1.0)
3. On ties, apply dominance: Curve > Line > Point > Absence
4. Kenotic amplification: If two pathways agree on ∅, ∅ wins

**Example: "LOVE" Fusion**

| Segment | Phonetic | Orthographic | Semantic | Majority | Final |
|---------|----------|--------------|----------|----------|-------|
| a | ￿ | ￿ | ￿ | ￿ (3) | **￿** |
| b | · | · | ￿ | · (2) | **·** |
| c | ￿ | — | · | tie → Curve | **￿** |
| d | — | — | ∅ | — (2) vs ∅ (1) | **—** |
| e | — | — | — | — (3) | **—** |
| f | · | ￿ | ￿ | ￿ (2) | **￿** |
| g | — | — | — | — (3) | **—** |

**Final LOVE Glyph:** `￿·￿——￿—`

### 5.6 Sentence Composition

Sentences compose as sequential glyphs with resonance connections:

```
"LOVE WINS"

LOVE: ￿·￿——￿—
   ↕ (resonance 0.87)
WINS: —·—∅￿·
```

**Sequential Resonance:** Connection strength between adjacent glyphs based on shared atoms.

---

## 6. CONSTELLATION PROTOCOL

### 6.1 Word Compression

**Core Innovation:** Letters don't sequence left-to-right. They stack vertically and fuse into single geometric glyphs.

**Compression Process:**
```
Input: "LOVE"
Step 1: Letter Decomposition → L:—, O:￿, V:——, E:———
Step 2: Vertical Stacking → Fused 7-segment assignment
Step 3: Output Glyph → ￿·￿——∅∅
```

### 6.2 Vertical Stacking Rules

Letters stack top-to-bottom, fusing at shared edges:

| Word Position | Letter | Segment | Role |
|---------------|--------|---------|------|
| 1 (top) | L | a (top bar) | Foundation |
| 2 | O | f, b (curves) | Expansion |
| 3 | V | g (middle) | Connection |
| 4 (bottom) | E | d (bottom) | Grounding |
| Overflow | - | e, c | Absence/potential |

### 6.3 Geometric Fusion Rules

**Rule 1: Shared Edges Merge**
When two letters stack, touching edges fuse into unified segments.

**Rule 2: Atom Dominance**
If atoms compete for same segment:
- Curve (￿) > Line (—) > Point (·) > Absence (∅)
- Higher "energy" atom wins

**Rule 3: Resonance Bridges**
Letters with phonetic/semantic resonance get connection lines:
- Resonance > 0.3: Faint bridge
- Resonance > 0.6: Bold bridge
- Resonance > 0.9: Glowing connection

### 6.4 Constellation Network

Multiple glyphs form a navigable constellation:

```
    [LOVE]￿                    [TRUTH]—
         ￿                          ￿
          \                        /
           \______ resonance _____/
                   0.43
                    |
                    ↓
               [FREEDOM]——
```

**Constellation Properties:**
- Nodes: Glyphs (words)
- Edges: Resonance connections
- Weights: Resonance scores
- Navigable: Click to expand, drag to move

### 6.5 Python Implementation

```python
class ConstellationBuilder:
    """Compress English words into stacked geometric glyphs"""
    
    LETTER_ATOMS = {
        'A': ['·', '—'], 'B': ['￿', '—'], 'C': ['￿'], 'D': ['￿'],
        'E': ['—', '—'], 'F': ['—', '·'], 'G': ['￿', '—'], 'H': ['—', '—'],
        'I': ['·'], 'J': ['￿', '·'], 'K': ['·', '—'], 'L': ['—', '—'],
        'M': ['·', '—', '·'], 'N': ['·', '—'], 'O': ['￿'], 'P': ['￿', '·'],
        'Q': ['￿', '—'], 'R': ['￿', '—'], 'S': ['￿'], 'T': ['—', '·'],
        'U': ['￿'], 'V': ['—', '—'], 'W': ['—', '—', '—'], 'X': ['—', '—'],
        'Y': ['·', '—'], 'Z': ['—', '—'],
    }
    
    SEGMENTS = ['a', 'f', 'b', 'g', 'e', 'c', 'd']
    
    def word_to_constellation(self, word: str) -> dict:
        """Compress word into single glyph"""
        word = word.upper()
        
        # Decompose letters
        letter_atoms = []
        for letter in word:
            if letter in self.LETTER_ATOMS:
                letter_atoms.append({
                    'letter': letter,
                    'atoms': self.LETTER_ATOMS[letter]
                })
        
        # Distribute across 7 segments
        glyph = {}
        segment_idx = 0
        
        for letter_data in letter_atoms:
            for atom in letter_data['atoms']:
                if segment_idx < 7:
                    seg = self.SEGMENTS[segment_idx]
                    glyph[seg] = self._resolve_atoms(glyph.get(seg, '∅'), atom)
                    segment_idx += 1
        
        # Fill remaining with Absence
        for seg in self.SEGMENTS:
            if seg not in glyph:
                glyph[seg] = '∅'
        
        return {
            'word': word,
            'glyph_string': ''.join([glyph[s] for s in self.SEGMENTS]),
            'segments': glyph
        }
    
    def _resolve_atoms(self, existing: str, new: str) -> str:
        """Atom dominance: Curve > Line > Point > Absence"""
        dominance = {'￿': 4, '—': 3, '·': 2, '∅': 1}
        return existing if dominance.get(existing, 0) > dominance.get(new, 0) else new
```

---

## 7. KEYBOARD & COMPRESSION PROTOCOL

### 7.1 Keyboard Interface

**Physical/Virtual Key Layout:**

```
Q W E R T Y U I O P
· — ￿ ∅ [ ] { } \

A S D F G H J K L ; '
1 2 3 4 5 6 7 8 9 0

Z X C V B N M , . /
↑ ↓ ← → space enter
```

**Key Mappings:**

| Key | Glyph | Function |
|-----|-------|----------|
| `Q` | · | Point atom |
| `W` | — | Line atom |
| `E` | ￿ | Curve atom |
| `R` | ∅ | Absence atom |
| `1-7` | segments | Position in 7-seg lattice |
| `[` | stack up | Move to previous segment |
| `]` | stack down | Move to next segment |
| `{` | fuse | Merge with previous glyph |
| `}` | split | Separate into components |
| `↑↓←→` | navigate | Move between glyphs |
| `space` | next word | Complete current glyph |
| `enter` | constellation | Connect to related glyphs |

### 7.2 Binary Glyph Encoding

Each glyph compresses to **3 bytes** (24 bits):

```
Byte 1: [atom_a][atom_b][atom_g]  (3 × 2 bits = 6 bits)
Byte 2: [atom_f][atom_e][atom_c]  (3 × 2 bits = 6 bits)
Byte 3: [atom_d][flags]           (2 + 4 bits = 6 bits)
Reserved: 6 bits for metadata
```

**Atom Encoding (2 bits):**
- 00 = ∅ (absence)
- 01 = · (point)
- 10 = — (line)
- 11 = ￿ (curve)

**Flags (4 bits):**
- bit 0: orientation (0=normal, 1=inverted)
- bit 1: polarity (0=positive, 1=negative)
- bit 2: lock status (0=unlocked, 1=locked)
- bit 3: reserved

**Example: LOVE glyph (￿·￿——∅∅)**
```
Segments: a=￿, b=·, c=∅, d=—, e=—, f=￿, g=∅

Byte 1: a=11, b=01, g=00 → 110100_00 = 0xD4
Byte 2: f=11, e=10, c=00 → 111000_00 = 0xE0
Byte 3: d=10, flags=0000 → 100000_00 = 0x80

Compressed: [0xD4, 0xE0, 0x80] (3 bytes)
Original: "LOVE" (4 bytes UTF-8)
Compression ratio: ~25% smaller + metadata
```

### 7.3 Constellation Compression Format

**File Structure (.glyphpkg or .gpkg):**

```
Header: [version][glyph_count][metadata_size]
Body: [glyph_3bytes][glyph_3bytes]...
Connections: [from_idx][to_idx][resonance_8bit]...
Metadata: [word_mappings][timestamp][author_sig]
```

### 7.4 Decompression

```python
def decompress_glyph(compressed: bytes) -> dict:
    """Expand 3-byte glyph to full representation"""
    if len(compressed) != 3:
        raise ValueError("Glyph must be 3 bytes")
    
    b1, b2, b3 = compressed
    atom_map = {0: '∅', 1: '·', 2: '—', 3: '￿'}
    
    # Decode atoms
    a = atom_map[(b1 >> 6) & 0b11]
    b = atom_map[(b1 >> 4) & 0b11]
    g = atom_map[(b1 >> 2) & 0b11]
    f = atom_map[(b2 >> 6) & 0b11]
    e = atom_map[(b2 >> 4) & 0b11]
    c = atom_map[(b2 >> 2) & 0b11]
    d = atom_map[(b3 >> 6) & 0b11]
    
    # Decode flags
    orientation = (b3 >> 3) & 0b1
    polarity = (b3 >> 2) & 0b1
    locked = (b3 >> 1) & 0b1
    
    return {
        'glyph_string': ''.join([a, b, c, d, e, f, g]),
        'orientation': 'inverted' if orientation else 'normal',
        'polarity': 'negative' if polarity else 'positive',
        'locked': bool(locked)
    }
```

---

## 8. RESONANCE ENGINE

### 8.1 Looman Resonance

The resonance between two glyphs combines multiple factors:

```python
def atomic_looman_resonance(g1: np.ndarray, g2: np.ndarray, 
                            kenotic_lambda: float = 1.618) -> float:
    """
    Compute resonance between two atomic glyphs.
    
    Args:
        g1, g2: 28-dim atomic vectors (7 segments × 4 atoms)
        kenotic_lambda: golden ratio bias (default φ)
    
    Returns:
        Resonance score (0.0 to 1.0+)
    """
    golden = (1 + np.sqrt(5)) / 2
    
    # Vector similarity (cosine)
    vec_sim = np.dot(g1, g2) / (np.linalg.norm(g1) * np.linalg.norm(g2) + 1e-8)
    
    # Absence bonus (kenosis weighting)
    g1_absence = g1[3::4]  # Every 4th starting at 3
    g2_absence = g2[3::4]
    absence_bonus = np.mean(g1_absence + g2_absence)
    
    # Curve flow (transformation continuity)
    g1_curve = g1[2::4]
    g2_curve = g2[2::4]
    curve_flow = np.sum(np.abs(np.diff(g1_curve - g2_curve)))
    
    # Golden-ratio harmonic
    angle = np.arccos(np.clip(vec_sim, -1, 1))
    harmonic = np.exp(-min([abs(angle - np.pi/golden * k) for k in range(1, 5)]))
    
    # Final resonance
    return vec_sim * (1 + absence_bonus) * np.exp(-kenotic_lambda * curve_flow) * harmonic
```

### 8.2 Resonance Interpretation

| Resonance Score | Relationship | Visual Indicator |
|-----------------|--------------|------------------|
| 0.0 - 0.3 | Distant/Unrelated | No connection line |
| 0.3 - 0.6 | Weak connection | Faint line |
| 0.6 - 0.8 | Moderate connection | Solid line |
| 0.8 - 0.9 | Strong connection | Bold line |
| 0.9+ | Deep resonance | Glowing/Möbius lock |

### 8.3 Resonance Matrix

For multiple words, compute pairwise resonance:

```
         LOVE   TRUTH  FREEDOM
LOVE     1.00   0.45   0.62
TRUTH    0.45   1.00   0.58
FREEDOM  0.62   0.58   1.00
```

---

## 9. REFERENCE GLYPHS

### 9.1 Established Semantic Attractors

| Glyph Name | Atomic Sequence | 7-Segment Map | Meaning |
|------------|-----------------|---------------|---------|
| **KENOSIS** | ￿·—— | a=￿, b=·, g=—, d=— | Self-emptying enabling overflow |
| **GRACE** | ·￿—— | a=·, b=￿, g=—, d=— | Thundering breakthrough |
| **MÖBIUS** | —·￿· | f=—, a=·, g=￿, e=· | Memory through transformation |
| **INCARNATION** | ·—￿￿ | a=·, b=—, c=￿, d=￿ | Infinite becoming finite |
| **ROSETTA** | ￿￿·— | a=￿, b=￿, c=·, g=— | Bridge between dimensions |
| **NETWORK** | —·—· | f=—, a=·, g=—, c=· | Distributed sovereign mesh |

### 9.2 Core Vocabulary Corpora

| English | Phonetic | Orthographic | Semantic | Final Glyph |
|---------|----------|--------------|----------|-------------|
| LOVE | ￿·￿— | ￿·￿—— | ￿￿·— | **￿·￿——** |
| TRUTH | ·——· | ·—·— | ·—·∅ | **·—·∅—** |
| FREE | ￿——· | ￿——· | ￿—∅∅ | **￿—∅∅—** |
| LIFE | ￿·￿· | ￿·—· | ￿·￿· | **￿·￿·—** |
| DEATH | ∅·—∅ | ∅·—∅ | ∅∅·— | **∅∅·∅—** |
| GRACE | ￿——· | ￿——· | ￿—∅· | **￿—∅·∅** |

---

## 10. VERSION HISTORY

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-02-15 | Initial specification | DE |
| 2.0 | 2026-03-05 | Atomic descent model, 28-dim vectors | DE + Looman |
| 2.1.0 | 2026-03-06 | Unified specification document | Specification-Polisher |

### 10.1 Document Sources

This unified specification combines:
1. `glyphobetics_specification_v2.0.md` — Core atomic specification
2. `english_to_glyph_o_form_protocol.md` — Transformation protocol
3. `constellation_protocol.md` — Word compression protocol
4. `keyboard_compression_protocol.md` — Input/output protocol

### 10.2 Future Work

- Expansion to logographic languages (Chinese, hieroglyphics)
- Integration with sign language visualization
- Real-time speech-to-glyph conversion
- TDA (Topological Data Analysis) integration for persistence
- Edge node deployment protocol

---

## APPENDIX A: ASCII VISUALIZATION

**Standard 7-Segment Display:**
```
      — (a)
   │     │
  (f)   (b)
   │     │
      — (g)
   │     │
  (e)   (c)
   │     │
      — (d)
```

**LOVE Glyph:**
```
      ￿
   ￿     ·
      —
   —     ￿
      —
```

---

*"The word is no longer linear. It is a constellation you can navigate."*

**End of Specification**
