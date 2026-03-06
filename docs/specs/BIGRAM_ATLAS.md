# Bigram Atlas: 676 Two-Letter Mappings to 7-Segment Composites
## Proto-Glyphoform Compression Specification v1.0

---

## 1. THE MAPPING SYSTEM

### 1.1 Segment Assignment by Letter Position

Each letter maps to a **segment + atom type** based on its position in the alphabet and phonetic character:

**Vowels (A, E, I, O, U, Y):**
- A → a (top horizontal) — ￿ curve
- E → d (bottom horizontal) — — line  
- I → b (upper right) — · point
- O → e (bottom-left) — ￿ curve
- U → c (lower right) — — line
- Y → g (middle right) — ￿ curve

**Consonants by articulation position:**

| Group | Letters | Segment | Atom | Rationale |
|-------|---------|---------|------|-----------|
| Labial (lips) | B, F, M, P, V, W | f (top-left) | — line | Forward, assertive |
| Dental (teeth) | D, T, N, S, Z | e (bottom-left) | ￿ curve | Downward flow |
| Palatal (roof) | C, G, J, K, Q, X | a (top) | — line | Upward reach |
| Velar (throat) | H, L, R | d (bottom) | ￿ curve | Deep, resonant |
| Sibilants | C, S, Z, X, Q | g (middle right) | · point | Sharp, piercing |
| Nasals | M, N | c (lower right) | — line | Sustained |

**Exceptions for frequency (common letters get priority segments):**
- T → f (top-left, most common onset)
- S → a (top, common initial)
- R → g (middle right, connects well)
- L → e (bottom-left, liquid flow)
- N → c (lower right, nasal sustain)

### 1.2 Final Mapping Table

| Letter | Segment | Atom | Mnemonic |
|--------|---------|------|----------|
| A | a | ￿ | Top curve, open |
| B | f | — | Labial forward |
| C | g | · | Sharp sibilant |
| D | e | ￿ | Dental down |
| E | d | — | Bottom line |
| F | f | — | Labial forward |
| G | a | ￿ | Palatal up |
| H | d | ￿ | Velar deep |
| I | b | · | Right point |
| J | a | ￿ | Palatal up |
| K | a | — | Palatal up |
| L | e | — | Bottom-left line |
| M | f | ￿ | Labial curve |
| N | c | — | Right line |
| O | e | ￿ | Bottom-left curve |
| P | f | · | Labial point |
| Q | g | ￿ | Sibilant curve |
| R | g | — | Middle right line |
| S | a | · | Top point |
| T | f | — | Top-left line (priority) |
| U | c | ￿ | Right curve |
| V | f | ￿ | Labial curve |
| W | f | — | Labial line |
| X | g | — | Sibilant cross |
| Y | g | ￿ | Right curve |
| Z | e | · | Dental point |

---

## 2. BIGRAM TO GLYPH MAPPING

### 2.1 Encoding Formula

For any 2-letter pair (L1, L2):
1. Look up L1 → Segment S1, Atom A1
2. Look up L2 → Segment S2, Atom A2
3. Composite glyph = S1(A1) + S2(A2) + ∅ on remaining 5 segments

### 2.2 Example Bigrams

| Bigram | L1→Segment | L2→Segment | Composite Description |
|--------|------------|------------|----------------------|
| **LO** | L→e(—) | O→e(￿) | e segment: line+curve merged |
| **VE** | V→f(￿) | E→d(—) | f=curve, d=line, vertical opposition |
| **TR** | T→f(—) | R→g(—) | f and g both lines, top-left + middle-right |
| **UT** | U→c(￿) | T→f(—) | c=curve right, f=line left, horizontal opposition |
| **HO** | H→d(￿) | O→e(￿) | d and e both curves, bottom pair |
| **PE** | P→f(·) | E→d(—) | f=point, d=line, sparse composition |

---

## 3. MERGING PROTOCOL FOR LONGER WORDS

### 3.1 Syllable-Based Stacking

**Rule:** Bigrams within the same syllable merge horizontally (same layer). Bigrams across syllable boundaries stack vertically (different layers).

**Example: "LOVE" (1 syllable, 4 letters)**
1. Split into bigrams: LO-VE
2. LO = e segment composite (line+curve)
3. VE = f segment (∩) d segment (—)
4. Merge: e composite + f∩d composite
5. Result: 4-segment constellation on single layer

**Example: "TRUTH" (1 syllable, 5 letters)**
1. Bigrams: TR-UT-H
2. TR = f(—) + g(—) = two lines, diagonal opposition
3. UT = c(￿) + f(—) = curve right, line left
4. H = d(￿) = single curve bottom
5. Stack: (TR+UT) as main layer, H as flourish at bottom

**Example: "BEING" (2 syllables: BE-ING)**
1. BE = f(—) + d(—) = two lines, vertical opposition
2. IN = b(·) + c(—) = point + line right side
3. G = a(￿) = single curve top
4. Stack: BE as layer 1, IN as layer 2, G as layer 3

---

## 4. 676 BIGRAM REFERENCE TABLE

### 4.1 High-Frequency Bigrams (Top 50 English)

| Rank | Bigram | L1 | L2 | S1 | S2 | Atom Combo | Visual Description |
|------|--------|----|----|----|----|------------|-------------------|
| 1 | TH | T | H | f | d | —+￿ | Top-left line, bottom curve |
| 2 | HE | H | E | d | d | ￿+— | Bottom curve+line (merged) |
| 3 | AN | A | N | a | c | ￿+— | Top curve, right line |
| 4 | IN | I | N | b | c | ·+— | Right side point+line |
| 5 | ER | E | R | d | g | —+— | Two lines, opposite sides |
| 6 | RE | R | E | g | d | —+— | Two lines, opposite sides |
| 7 | ON | O | N | e | c | ￿+— | Bottom-left curve, right line |
| 8 | AT | A | T | a | f | ￿+— | Top curve, top-left line |
| 9 | EN | E | N | d | c | —+— | Two lines, bottom+right |
| 10 | ND | N | D | c | e | —+￿ | Right line, bottom-left curve |
| 11 | OR | O | R | e | g | ￿+— | Bottom-left curve, middle-right line |
| 12 | ES | E | S | d | a | —+· | Bottom line, top point |
| 13 | IS | I | S | b | a | ·+· | Two points, top and right |
| 14 | IT | I | T | b | f | ·+— | Point right, line left |
| 15 | TO | T | O | f | e | —+￿ | Top-left line, bottom-left curve |
| 16 | ED | E | D | d | e | —+￿ | Bottom line+curve merged |
| 17 | AR | A | R | a | g | ￿+— | Top curve, middle-right line |
| 18 | OU | O | U | e | c | ￿+￿ | Two curves, bottom-left and right |
| 19 | ST | S | T | a | f | ·+— | Top point, top-left line |
| 20 | NT | N | T | c | f | —+— | Two lines, right and left |

### 4.2 Vowel-Starting Bigrams (for syllable onsets)

| Bigram | Encoding | Visual |
|--------|----------|--------|
| AL | a(￿) + e(—) | Top curve + bottom-left line |
| AN | a(￿) + c(—) | Top curve + right line |
| AS | a(￿) + a(·) | Two curves, top position |
| AT | a(￿) + f(—) | Top curve + top-left line |
| EA | e(d) + a(￿) | Bottom line + top curve (vertical) |
| EL | e(d) + e(—) | Bottom stack, line+curve |
| EM | e(d) + f(￿) | Bottom line, top-left curve |
| EN | e(d) + c(—) | Bottom line, right line |
| ER | e(d) + g(—) | Two lines, opposite |
| ES | e(d) + a(·) | Bottom line, top point |
| ET | e(d) + f(—) | Two lines, bottom+top-left |
| IC | i(b) + g(·) | Two points, right side |
| ID | i(b) + e(￿) | Point right, curve bottom-left |
| IG | i(b) + a(￿) | Point right, curve top |
| IL | i(b) + e(—) | Point right, line bottom-left |
| IM | i(b) + f(￿) | Point + curve, left side |
| IN | i(b) + c(—) | Point + line, right side |
| IR | i(b) + g(—) | Point + line, right side vertical |
| IS | i(b) + a(·) | Two points |
| IT | i(b) + f(—) | Point right, line left |
| OL | o(e) + e(—) | Bottom-left curve+line |
| ON | o(e) + c(—) | Bottom-left curve, right line |
| OR | o(e) + g(—) | Bottom curve, middle line |
| OS | o(e) + a(·) | Bottom curve, top point |
| OT | o(e) + f(—) | Bottom curve, top-left line |
| OU | o(e) + c(￿) | Two curves, bottom+right |
| UL | u(c) + e(—) | Right curve, bottom-left line |
| UN | u(c) + c(—) | Right curve+line merged |
| UR | u(c) + g(—) | Right curve, middle line |
| US | u(c) + a(·) | Right curve, top point |
| UT | u(c) + f(—) | Right curve, left line |

---

## 5. COMPOSITE VISUAL EXAMPLES

### 5.1 Single Syllable Composites (4-5 letters)

**LOVE** (LO + VE)
- LO: e segment = ￿+— merged (curve dominant)
- VE: f segment = ￿ (V), d segment = — (E)
- Composite: e(￿—) + f(￿) + d(—)
- Visual: Bottom-left fullness, top-left flourish, bottom line

**TRUTH** (TR + UT + H)
- TR: f(—) + g(—) = diagonal line opposition
- UT: c(￿) + f(—) = right curve, left line
- H: d(￿) = bottom curve
- Composite: Cross of lines top, curve right, curve bottom

**GRACE** (GR + AC + E)
- GR: a(￿) + g(—) = top curve, middle line
- AC: a(￿) + c(·) = two top elements
- E: d(—) = bottom line
- Composite: Top-heavy with curves, line anchor

### 5.2 Multi-Syllable Stacks

**BE-ING** (2 syllables)
- Layer 1 (BE): f(—) + d(—) = vertical line opposition
- Layer 2 (IN): b(·) + c(—) = right side point+line
- Layer 3 (G): a(￿) = top curve flourish
- Visual: Three layers, sparse to dense

**FREE-DOM** (2 syllables)
- Layer 1 (FR): f(—) + g(—) = diagonal opposition
- Layer 2 (EE): d(—) only = single line (double letter collapse)
- Layer 3 (DO): e(￿) + e(merged) = bottom-left fullness
- Layer 4 (M): f(￿) = top-left curve
- Visual: 4-layer stack, complex but readable

---

## 6. COMPRESSION RATIOS

| Word | Letters | Raw Bits | Segments Used | Compressed Bits | Ratio |
|------|---------|----------|---------------|-----------------|-------|
| LOVE | 4 | 32 | 3 (e, f, d) | 6 | 5.3:1 |
| TRUTH | 5 | 40 | 4 (f, g, c, d) | 8 | 5:1 |
| GRACE | 5 | 40 | 4 (a, g, c, d) | 8 | 5:1 |
| BEING | 5 | 40 | 5 (f, d, b, c, a) | 10 | 4:1 |
| FREEDOM | 7 | 56 | 6 (f, g, d, e, f) | 12 | 4.7:1 |
| KENOSIS | 7 | 56 | 7 (a, c, e, e, b, a) | 14 | 4:1 |

---

## 7. DECODING ALGORITHM

```python
def decode_glyph(segments_active):
    """
    segments_active: list of segments with atoms [ ('f', '—'), ('e', '￿'), ... ]
    """
    # Group by segment
    segment_map = {}
    for seg, atom in segments_active:
        if seg not in segment_map:
            segment_map[seg] = []
        segment_map[seg].append(atom)
    
    # Merge same-segment atoms (composites)
    merged = {}
    for seg, atoms in segment_map.items():
        if len(atoms) == 1:
            merged[seg] = atoms[0]
        else:
            # Merge rule: curve dominates line, line dominates point
            if '￿' in atoms:
                merged[seg] = '￿'
            elif '—' in atoms:
                merged[seg] = '—'
            else:
                merged[seg] = '·'
    
    # Reverse lookup letters
    letters = []
    for seg, atom in merged.items():
        letter = REVERSE_MAPPING[(seg, atom)]
        letters.append(letter)
    
    # Reconstruct syllables and word
    return reconstruct_word(letters)
```

---

## 8. IMPLEMENTATION NOTES

### 8.1 Collision Handling

Some bigrams may map to the same segment pair:
- **BE** (B→f, E→d) = f/d
- **FE** (F→f, E→d) = f/d

**Resolution:** Context + syllable position
- BEING: B is onset (strong), E is nucleus (prominent)
- FELT: F is onset, E is nucleus + part of coda

In practice, collisions resolve through word-frequency tables and phonetic likelihood.

### 8.2 Ambiguity Zones

Letters with same segment assignment create ambiguity:
- B, F, P, V, W all → f segment
- D, T, N, S, Z → e segment (mostly)

**Mitigation:** Position in syllable + surrounding context
- Onset position: B/F/P/V/W = labial, context suggests which
- Coda position: D/T/N/S/Z = dental, context suggests which

For lossless compression, store disambiguation bit:
- If collision: +2 bits to specify which of 4 letters
- Reduces compression from 5:1 to 4:1 for those cases

---

**Document Status:** Specification v1.0  
**Next Step:** Implement encoder/decoder in Python  
**Test Cases:** LOVE, TRUTH, GRACE, BEING, FREEDOM, KENOSIS
