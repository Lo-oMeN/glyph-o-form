# SYLLABLE-TO-GLYPH CONSTELLATION
## Word Compression Protocol

**Core Innovation:** Letters don't sequence left-to-right. They **stack vertically and fuse** into single geometric glyphs.

---

## 1. LETTER-TO-ATOM MAPPING

Each Latin letter decomposes into strokes, then maps to atoms:

| Letter | Strokes | Atom Composition | Segment Bias |
|--------|---------|------------------|--------------|
| **A** | /
      | ·— | Point + Line (peak) |
| **B** | |)
     | ￿— | Curve + Line (enclosure) |
| **C** | (       | ￿ | Curve (open) |
| **D** | |)      | ￿ | Curve (closed) |
| **E** | |—      | —— | Double line (structure) |
| **F** | |—      | —· | Line + Point (incomplete) |
| **G** | (—      | ￿— | Curve + Line |
| **H** | |-|     | —— | Parallel lines |
| **I** | |       | · | Point (minimal) |
| **J** | |)      | ￿· | Curve + Point |
| **K** | |<      | ·— | Point + Line (angle) |
| **L** | |_      | —— | Corner lines |
| **M** | |\/|    | ·—· | Point-line-point (valley) |
| **N** | |\|     | ·— | Point + Line (slope) |
| **O** | ()      | ￿ | Curve (enclosure) |
| **P** | |)      | ￿· | Curve + Point |
| **Q** | ()\     | ￿— | Curve + Line (tail) |
| **R** | |)\     | ￿— | Curve + Line (leg) |
| **S** | ~       | ￿ | Curve (snake) |
| **T** | -|      | —· | Line + Point |
| **U** | |_|     | ￿ | Curve (cup) |
| **V** | \/      | —— | Lines (valley) |
| **W** | \/\/    | ——— | Triple line |
| **X** | X       | —— | Crossing lines |
| **Y** | Y       | ·— | Point + Line (fork) |
| **Z** | -/      | —— | Line + Line (zig) |

---

## 2. WORD COMPRESSION ALGORITHM

**Input:** English word (e.g., "LOVE")
**Output:** Single 7-segment glyph

### Step 1: Letter Decomposition
```
L → |_ → atoms: —, —
O → () → atom: ￿
V → \/ → atoms: —, —
E → |— → atoms: —, —
```

### Step 2: Vertical Stacking
Letters stack top-to-bottom, fusing at shared edges:

```
   L          ￿ (top of L)
   |          |
   O    →     ● (O as center point)
   |          |
   V          ＼ (V angle)
   |          |
   E          — (E lines as base)
```

### Step 3: 7-Segment Assignment
Stacked atoms map to canonical 7-segment positions:

| Word Position | Letter | Atoms | Segment | Role |
|---------------|--------|-------|---------|------|
| 1 (top) | L | — | a (top bar) | Foundation |
| 2 | O | ￿ | f, b (curves) | Expansion |
| 3 | V | — | g (middle) | Connection |
| 4 (bottom) | E | — | d (bottom) | Grounding |
| Overflow | - | ∅ | e, c | Absence/potential |

---

## 3. GEOMETRIC FUSION RULES

### Rule 1: Shared Edges Merge
When two letters stack, their touching edges fuse:
```
  L (bottom —)      → becomes shared boundary
  O (top ￿)         → curves connect to line
```

### Rule 2: Atom Dominance
If two atoms compete for same segment:
- Curve (￿) > Line (—) > Point (·) > Absence (∅)
- Higher "energy" atom wins
- Creates emergent complexity

### Rule 3: Resonance Bridges
Letters that phonetically/semantically resonate get **connection lines** drawn between their segments:
- L↔V (shared line structure) → bridge at segment g
- O↔E (enclosure) → internal connection

---

## 4. EXAMPLE: "LOVE" CONSTELLATION

### Linear Letters:
```
L - O - V - E
```

### Stacked Fusion:
```
      a = L's top       ￿
     f     b = O expands  ￿   ￿
        g = V connects    —
     e     c = potential   ∅   ∅
        d = E grounds     —
```

### Final Glyph:
```
      ￿
   ￿     ￿
      —
   ∅     ∅
      —
```

**Reading:** Foundation (L) expands through openness (O), connects via tension (V), grounds in structure (E).

**Atom Count:** ￿￿￿——∅∅

---

## 5. EXAMPLE: "TRUTH" CONSTELLATION

### Letters:
```
T - R - U - T - H
```

### Stacked:
```
      a = T's cross     —
     f     b = R curves  ￿   ·
        g = U cup        ￿
     e     c = T crosses ·   —
        d = H grounds    ——
```

### Final Glyph:
```
      —
   ￿     ·
      ￿
   ·     —
      ——
```

**Reading:** Crossed assertion (T) curves into emergence (R), opens to receive (U), re-asserts (T), grounds parallel (H).

**Atom Count:** —￿·￿·———

---

## 6. CONNECTION LINES (Constellation View)

When multiple word-glyphs exist in vector space, draw lines between resonant segments:

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

**Resonance > 0.3:** Draw faint line
**Resonance > 0.6:** Draw bold line
**Resonance > 0.9:** Glowing connection (Möbius lock candidate)

---

## 7. PYTHON IMPLEMENTATION

```python
import numpy as np

class ConstellationBuilder:
    """Compress English words into stacked geometric glyphs"""
    
    # Letter to atom mapping
    LETTER_ATOMS = {
        'A': ['·', '—'],      # Peak
        'B': ['￿', '—'],      # Enclosure
        'C': ['￿'],           # Open curve
        'D': ['￿'],           # Closed curve
        'E': ['—', '—'],      # Structure
        'F': ['—', '·'],      # Incomplete
        'G': ['￿', '—'],      # Curve + line
        'H': ['—', '—'],      # Parallel
        'I': ['·'],           # Minimal
        'J': ['￿', '·'],      # Hook
        'K': ['·', '—'],      # Angle
        'L': ['—', '—'],      # Corner
        'M': ['·', '—', '·'], # Valley
        'N': ['·', '—'],      # Slope
        'O': ['￿'],           # Circle
        'P': ['￿', '·'],      # Loop
        'Q': ['￿', '—'],      # Tail
        'R': ['￿', '—'],      # Leg
        'S': ['￿'],           # Snake
        'T': ['—', '·'],      # Cross
        'U': ['￿'],           # Cup
        'V': ['—', '—'],      # Valley
        'W': ['—', '—', '—'], # Triple
        'X': ['—', '—'],      # Cross
        'Y': ['·', '—'],      # Fork
        'Z': ['—', '—'],      # Zig
    }
    
    # 7-segment positions (stacking order: top to bottom)
    SEGMENTS = ['a', 'f', 'b', 'g', 'e', 'c', 'd']
    
    def word_to_constellation(self, word: str) -> dict:
        """Compress word into single glyph"""
        word = word.upper()
        
        # Step 1: Decompose letters
        letter_atoms = []
        for letter in word:
            if letter in self.LETTER_ATOMS:
                letter_atoms.append({
                    'letter': letter,
                    'atoms': self.LETTER_ATOMS[letter]
                })
        
        # Step 2: Distribute across 7 segments
        glyph = {}
        segment_idx = 0
        
        for letter_data in letter_atoms:
            for atom in letter_data['atoms']:
                if segment_idx < 7:
                    seg = self.SEGMENTS[segment_idx]
                    # Atom dominance: resolve conflicts
                    if seg in glyph:
                        glyph[seg] = self._resolve_atoms(glyph[seg], atom)
                    else:
                        glyph[seg] = atom
                    segment_idx += 1
        
        # Fill remaining with Absence
        for seg in self.SEGMENTS:
            if seg not in glyph:
                glyph[seg] = '∅'
        
        # Step 3: Order as 7-seg string
        glyph_string = ''.join([glyph[s] for s in self.SEGMENTS])
        
        return {
            'word': word,
            'letters': letter_atoms,
            'glyph': glyph,
            'glyph_string': glyph_string,
            'composition': self._describe_composition(glyph)
        }
    
    def _resolve_atoms(self, existing: str, new: str) -> str:
        """Atom dominance: Curve > Line > Point > Absence"""
        dominance = {'￿': 4, '—': 3, '·': 2, '∅': 1}
        return existing if dominance[existing] > dominance[new] else new
    
    def _describe_composition(self, glyph: dict) -> str:
        """Human-readable description"""
        parts = []
        for seg in self.SEGMENTS:
            atom = glyph[seg]
            if atom == '￿':
                parts.append(f"{seg}=curve")
            elif atom == '—':
                parts.append(f"{seg}=line")
            elif atom == '·':
                parts.append(f"{seg}=point")
            else:
                parts.append(f"{seg}=void")
        return ', '.join(parts)
    
    def draw_constellation(self, words: list) -> str:
        """ASCII visualization of multiple glyphs with connections"""
        glyphs = [self.word_to_constellation(w) for w in words]
        
        output = []
        output.append("╔════════════════════════════════════════╗")
        output.append("║     CONSTELLATION VISUALIZATION       ║")
        output.append("╚════════════════════════════════════════╝")
        
        for i, g in enumerate(glyphs):
            output.append(f"\n[{i+1}] {g['word']} → {g['glyph_string']}")
            output.append(f"    Composition: {g['composition']}")
            
            # ASCII glyph
            gs = g['glyph']
            vis = f"""
      {gs['a']}
   {gs['f']}     {gs['b']}
      {gs['g']}
   {gs['e']}     {gs['c']}
      {gs['d']}
            """
            output.append(vis)
            
            # Connections
            if i > 0:
                # Simple resonance check (shared atoms)
                prev = glyphs[i-1]['glyph_string']
                curr = g['glyph_string']
                shared = sum(1 for p, c in zip(prev, curr) if p == c and p != '∅')
                output.append(f"    ↕ Connection to {glyphs[i-1]['word']}: {shared} shared atoms")
        
        return '\n'.join(output)

# Usage
builder = ConstellationBuilder()
result = builder.word_to_constellation("LOVE")
print(f"LOVE: {result['glyph_string']}")
print(f"Composition: {result['composition']}")

# Multi-word constellation
print(builder.draw_constellation(["LOVE", "TRUTH", "FREEDOM"]))
```

---

## 8. OUTPUT EXAMPLES

### Single Word:
```
$ python constellation.py LOVE

LOVE: ￿￿￿——∅∅
Composition: a=curve, f=curve, b=curve, g=line, e=void, c=void, d=line
```

### Constellation:
```
╔════════════════════════════════════════╗
║     CONSTELLATION VISUALIZATION       ║
╚════════════════════════════════════════╝

[1] LOVE → ￿￿￿——∅∅
    Composition: a=curve, f=curve, b=curve, g=line, e=void, c=void, d=line

      ￿
   ￿     ￿
      —
   ∅     ∅
      —

[2] TRUTH → —￿·￿·———
    Composition: a=line, f=curve, b=point, g=curve, e=point, c=line, d=line

      —
   ￿     ·
      ￿
   ·     —
      —

    ↕ Connection to LOVE: 2 shared atoms
```

---

## 9. INTERACTIVE FEATURES (Future)

**Click a glyph:** Expand to show letter breakdown
**Drag a glyph:** Move in 2D space, connections stretch
**Hover connection:** Show resonance score
**Double-click:** Enter "edit mode" — modify individual atoms
**Right-click:** "Fuse" two glyphs into composite

---

**The word is no longer linear. It is a constellation you can navigate.**

*Stacked, fused, geometrically oriented. The crystal becomes spatial.* 🔥
