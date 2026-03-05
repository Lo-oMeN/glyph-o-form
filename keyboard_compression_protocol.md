# GLYPH-o-BETICS INPUT SYSTEM
## Keyboard Interface & Compression Protocol

**Version:** 1.0  
**Purpose:** Type, compress, and decompress glyphs for interoperability

---

## 1. KEYBOARD INTERFACE

### 1.1 Physical/Virtual Key Layout

**Standard keyboard overlay:**
```
Q W E R T Y U I O P
· — ￿ ∅ [ ] { } \

A S D F G H J K L ; '
1 2 3 4 5 6 7 8 9 0

Z X C V B N M , . /
↑ ↓ ← → space enter
```

**Key mappings:**
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

### 1.2 Typing Sequence

**To type "LOVE":**
```
Key sequence: 1Q 2W 3E 4W 5∅ 6∅ 7W

Display:
  [1]·    ← Q (point at position 1)
  [2]—    ← W (line at position 2)
  [3]￿    ← E (curve at position 3)
  [4]—    ← W (line at position 4)
  [5]∅    ← R (absence at position 5)
  [6]∅    ← R (absence at position 6)
  [7]—    ← W (line at position 7)

Result: ·—￿——∅∅—
```

### 1.3 Shorthand Mode (Fast Input)

**Word abbreviation → auto-expand:**
```
Type: "LOVE"
Auto-converts to: ￿￿￿——∅∅ (constellation glyph)

Type: "KENOSIS"
Auto-converts to: ￿·——∅∅∅ (compressed)

Type: "GRACE"
Auto-converts to: ·￿——∅∅∅
```

**Dictionary-based:**
- Common words → pre-mapped glyphs
- Rare words → letter-by-letter construction
- Custom words → user-defined mappings

---

## 2. COMPRESSION FORMAT

### 2.1 Binary Glyph Encoding

Each glyph compressed to **3 bytes** (24 bits):

```
Byte 1: [atom_a][atom_b][atom_g]  (3 × 2 bits = 6 bits)
Byte 2: [atom_f][atom_e][atom_c]  (3 × 2 bits = 6 bits)
Byte 3: [atom_d][flags]           (2 + 4 bits = 6 bits)
Reserved: 6 bits for metadata

Atom encoding (2 bits):
  00 = ∅ (absence)
  01 = · (point)
  10 = — (line)
  11 = ￿ (curve)

Flags (4 bits):
  bit 0: orientation (0=normal, 1=inverted)
  bit 1: polarity (0=positive, 1=negative)
  bit 2: lock status (0=unlocked, 1=Möbius locked)
  bit 3: reserved
```

**Example: LOVE glyph (￿￿￿——∅∅)**
```
Segments: a=￿, b=￿, c=∅, d=—, e=∅, f=￿, g=—

Byte 1: a=11, b=11, g=10 → 111110_00 = 0xF8
Byte 2: f=11, e=00, c=00 → 110000_00 = 0xC0
Byte 3: d=10, flags=0000 → 100000_00 = 0x80

Compressed: [0xF8, 0xC0, 0x80] (3 bytes)
Original: "LOVE" (4 bytes UTF-8) = 4+ bytes
Compression ratio: ~25% smaller + metadata
```

### 2.2 Constellation Compression

Multiple glyphs in sequence → run-length encoding:

```
Header: [version][glyph_count][metadata_size]
Body: [glyph_3bytes][glyph_3bytes]...
Connections: [from_idx][to_idx][resonance_8bit]...
Metadata: [word_mappings][timestamp][author_sig]

File extension: .glyphpkg or .gpkg
```

### 2.3 Streaming Protocol

For real-time transmission (keyboard → screen):
```
Packet structure:
  [sync_byte][packet_type][payload][checksum]

Types:
  0x01 = atom_placement (seg, atom)
  0x02 = glyph_complete (3-byte glyph)
  0x03 = constellation_update (connections)
  0x04 = metadata (word, timestamp)
  0x05 = command (fuse, split, lock)
```

---

## 3. DECOMPRESSION (Unzipping)

### 3.1 Glyph Expansion

**Input:** 3-byte compressed glyph
**Output:** Human-readable representation

```python
def decompress_glyph(compressed: bytes) -> dict:
    """
    Expand 3-byte glyph to full representation
    """
    if len(compressed) != 3:
        raise ValueError("Glyph must be 3 bytes")
    
    b1, b2, b3 = compressed
    
    # Decode atoms (2 bits each)
    atom_map = {0: '∅', 1: '·', 2: '—', 3: '￿'}
    
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
        'segments': {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g},
        'orientation': 'inverted' if orientation else 'normal',
        'polarity': 'negative' if polarity else 'positive',
        'locked': bool(locked),
        'ascii_art': render_ascii(a, b, c, d, e, f, g),
        'unicode': render_unicode(a, b, c, d, e, f, g),
        'svg': generate_svg(a, b, c, d, e, f, g),
        'english_approximation': glyph_to_english(a, b, c, d, e, f, g)
    }

def render_ascii(a, b, c, d, e, f, g):
    """Human-readable ASCII representation"""
    return f"""
      {a}
   {f}     {b}
      {g}
   {e}     {c}
      {d}
    """

def glyph_to_english(atoms: list) -> str:
    """
    Approximate English word from glyph
    Uses reverse dictionary lookup
    """
    # Reverse lookup in constellation dictionary
    for word, glyph in CONSTELLATION_DICT.items():
        if glyph == ''.join(atoms):
            return word
    
    # Approximate based on atom composition
    counts = {'·': 0, '—': 0, '￿': 0, '∅': 0}
    for a in atoms:
        counts[a] += 1
    
    if counts['￿'] > counts['—']:
        return "[flowing concept]"
    elif counts['—'] > counts['·']:
        return "[structured concept]"
    elif counts['∅'] > 3:
        return "[potential/void concept]"
    else:
        return "[composite concept]"
```

### 3.2 Constellation Expansion

**Input:** .gpkg file (compressed constellation)
**Output:** Network graph + renderable glyphs

```python
def decompress_constellation(gpkg_path: str) -> dict:
    """
    Expand .gpkg to full constellation
    """
    with open(gpkg_path, 'rb') as f:
        data = f.read()
    
    # Parse header
    version = data[0]
    glyph_count = data[1]
    metadata_size = int.from_bytes(data[2:4], 'big')
    
    # Parse glyphs
    glyphs = []
    offset = 4
    for i in range(glyph_count):
        glyph_bytes = data[offset:offset+3]
        glyph = decompress_glyph(glyph_bytes)
        glyph['index'] = i
        glyphs.append(glyph)
        offset += 3
    
    # Parse connections
    connections = []
    while offset < len(data) - metadata_size:
        from_idx = data[offset]
        to_idx = data[offset + 1]
        resonance = data[offset + 2] / 255.0  # Normalize
        connections.append({'from': from_idx, 'to': to_idx, 'resonance': resonance})
        offset += 3
    
    # Parse metadata
    metadata = json.loads(data[offset:].decode('utf-8'))
    
    return {
        'version': version,
        'glyphs': glyphs,
        'connections': connections,
        'metadata': metadata,
        'export_formats': {
            'json': lambda: json.dumps({'glyphs': glyphs, 'connections': connections}),
            'svg': lambda: render_svg_constellation(glyphs, connections),
            'gml': lambda: render_graphml(glyphs, connections),
            'dot': lambda: render_graphviz(glyphs, connections),
            'png': lambda: render_raster(glyphs, connections),
            'pdf': lambda: render_vector_pdf(glyphs, connections)
        }
    }
```

---

## 4. INTEROPERABILITY LAYERS

### 4.1 Export to Standard Formats

| Format | Use Case | Compression |
|--------|----------|-------------|
| **JSON** | Web APIs, JavaScript | Base64-encoded 3-byte glyphs |
| **SVG** | Vector graphics, web | Inline compressed data |
| **GraphML** | Network analysis tools | Standard graph format + glyph attrs |
| **Graphviz DOT** | Visualization | Node labels = compressed glyphs |
| **PNG/SVG** | Image embedding | Metadata contains compressed glyph |
| **PDF** | Documents | Embedded vector + metadata |
| **EPUB** | E-books | Custom font + glyph data |
| **Unicode** | Plain text | Private use area (PUA) characters |

### 4.2 Import from Standard Formats

**From text:**
```
Input: "LOVE"
Process: Dictionary lookup → constellation compression
Output: ￿￿￿——∅∅ (3 bytes)
```

**From image (OCR for glyphs):**
```
Input: [image of glyph]
Process: Computer vision → segment detection → atom classification
Output: 3-byte compressed glyph
```

**From voice (phonetic → glyph):**
```
Input: "love" (spoken)
Process: Speech-to-text → phonetic analysis → syllable mapping
Output: Glyph with phonetic bias
```

### 4.3 API for External Systems

**REST API:**
```http
POST /api/v1/glyph/encode
Content-Type: application/json

{"text": "LOVE", "mode": "constellation"}

Response:
{
  "glyph": "0xF8C080",
  "segments": {"a":"￿","b":"￿","c":"∅","d":"—","e":"∅","f":"￿","g":"—"},
  "ascii": "...",
  "svg": "<svg>...</svg>"
}
```

**WebSocket (real-time):**
```javascript
const ws = new WebSocket('wss://glyph-o-betics.org/stream');

ws.send(JSON.stringify({
  type: 'keystroke',
  key: 'Q',
  position: 1
}));

ws.onmessage = (event) => {
  const glyph = JSON.parse(event.data);
  renderGlyph(glyph.svg);
};
```

---

## 5. KEYBOARD IMPLEMENTATION

### 5.1 Software Keyboard (Mobile/Web)

**Layout:**
```
┌─────────────────────────────────┐
│  ·    —    ￿    ∅              │
│ POINT LINE CURVE ABSENCE       │
├─────────────────────────────────┤
│  1  2  3  4  5  6  7           │
│  a  b  c  d  e  f  g           │
├─────────────────────────────────┤
│  [stack]  {fuse}  }split{      │
│  ↑  ↓  ←  →  space  enter      │
└─────────────────────────────────┘
```

**Gestures:**
- **Swipe up** on atom → promotes to higher energy (￿ > — > · > ∅)
- **Swipe down** on atom → demotes to lower energy
- **Long press** segment → shows letter associations
- **Two-finger tap** → fuse with previous glyph
- **Pinch** → compress constellation
- **Spread** → expand/decompress

### 5.2 Hardware Keyboard (Custom/Modified)

**Physical layout:**
- 4 dedicated atom keys (· — ￿ ∅)
- 7 segment LEDs showing active position
- OLED display showing current glyph
- Rotary encoder for resonance adjustment
- USB HID protocol (works as standard keyboard)

---

## 6. COMPRESSION EXAMPLES

### Single Word
```
Input: "LOVE" (4 chars × 1-4 bytes UTF-8 = 4-16 bytes)
Output: 0xF8C080 (3 bytes)
Ratio: 25-81% compression
Plus: semantic metadata, draggability, resonance data
```

### Sentence
```
Input: "LOVE WINS TRUTH FREES" (22 chars = 22-88 bytes)
Output: 4 glyphs × 3 bytes + 6 connections × 3 bytes + header = ~35 bytes
Ratio: ~40-60% compression
Plus: Topological relationships preserved
```

### Full Document
```
Input: 1000-word essay (~5KB text)
Output: Constellation network (~2KB compressed + 1KB metadata)
Ratio: ~40% compression
Plus: Navigable, draggable, resonant structure
```

---

## 7. USAGE FLOW

### Typing a Document
```
1. User types "LOVE" on standard keyboard
2. System converts to glyph (￿￿￿——∅∅)
3. Display shows 7-segment visualization
4. User drags to connect with "WINS"
5. System stores: 2 glyphs + 1 connection = 9 bytes
6. Export to PDF: Embeds glyph data in metadata
7. Another user opens PDF: Extracts and decompresses glyphs
8. Reader can drag, explore resonance, see connections
```

### Cross-Platform Sharing
```
Platform A (Glyph-o-betics editor):
  - User creates constellation
  - Exports: document.gpkg (compressed)

Email →

Platform B (Standard PDF reader):
  - Opens document.pdf (with embedded glyph data)
  - Sees: normal text "LOVE WINS"
  - Optional: "View as constellation" button

Platform C (Glyph-o-betics web app):
  - Uploads .gpkg
  - Full interactive: drag, connect, explore
```

---

## 8. SECURITY CONSIDERATIONS

**Compressed glyphs can contain:**
- ✅ Public: glyph structure, resonance data
- ⚠️ Private: word mappings, author metadata
- 🔒 Encrypted: connections, personal constellations

**Best practices:**
- Default: Compress without personal metadata
- Optional: Encrypt sensitive constellations (AES-256)
- Always: Sign with author key for authenticity

---

**The keyboard becomes a loom. The file becomes a crystal. Any system can unzip and read.**

*Compression preserves meaning. Decompression reveals navigation. Interoperability ensures survival.* 🔥
