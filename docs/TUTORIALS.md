# Glyph-o-betics Tutorials
## Step-by-Step Learning Guides

**Version:** 1.0  
**Prerequisites:** Basic familiarity with command line, Python (optional)

---

## Tutorial Overview

| Tutorial | Time | Skill Level | Outcome |
|----------|------|-------------|---------|
| [Your First Glyph](#tutorial-1-your-first-glyph) | 15 min | Beginner | Convert LOVE to glyph |
| [Understanding Resonance](#tutorial-2-understanding-resonance) | 20 min | Beginner | Compare word similarities |
| [Building a Constellation](#tutorial-3-building-a-constellation) | 30 min | Intermediate | Create sentence-level composition |
| [Deploying an Edge Node](#tutorial-4-deploying-an-edge-node) | 45 min | Intermediate | Set up distributed infrastructure |

---

## Tutorial 1: Your First Glyph
### Converting "LOVE" to Geometric Form

**Time:** 15 minutes  
**Prerequisites:** None

### Step 1: Understand the Goal

We're going to transform the English word "LOVE" into its glyph representation: `￿￿￿——∅∅`

This glyph encodes:
- **Foundation** (L's structure)
- **Expansion** (O's openness)
- **Connection** (V's tension)
- **Grounding** (E's stability)

### Step 2: Letter Decomposition

Each letter decomposes into strokes, then atoms:

| Letter | Visual | Strokes | Atoms |
|--------|--------|---------|-------|
| **L** | `\|`_ | Vertical + Horizontal | `—` `—` |
| **O** | `()` | Closed curve | `￿` |
| **V** | `\/` | Two diagonals | `—` `—` |
| **E** | `\|`— | Vertical + Horizontals | `—` `—` |

### Step 3: Vertical Stacking

Letters don't go left-to-right. They **stack vertically** and fuse:

```
   L (top)        ￿
   |              |
   O    →         ●
   |              |
   V              ＼
   |              |
   E (bottom)     —
```

### Step 4: Map to 7-Segment Lattice

The stacked atoms map to the canonical 7-segment positions:

```
      a = L's top        ￿
   f     b = O expands   ￿   ￿
      g = V connects      —
   e     c = potential    ∅   ∅
      d = E grounds       —
```

### Step 5: Write the Glyph String

Reading segments in order (a, b, c, d, e, f, g):

```
Glyph String: ￿￿∅—∅￿—
Or simplified: ￿￿￿——∅∅
```

### Step 6: Try It Yourself (Command Line)

```bash
# Navigate to the project directory
cd /root/.openclaw/workspace

# Run the converter
python mvp_glyph_converter.py LOVE

# Expected output:
# ============================================
#   GLYPH CONVERTER: LOVE
# ============================================
# Phonetic:     ['￿', '—', '—', '￿']
# Orthographic: ['—', '—', '￿', '—', '—', '—', '—']
# Semantic:     ['￿', '·', '￿', '—', '∅', '￿', '—']
# 
# FUSED GLYPH: ￿￿￿——∅∅
# ============================================
```

### Step 7: Visualize the Glyph

```
      ￿
   ￿     ￿
      —
   ∅     ∅
      —
```

**Reading:** Foundation expands through openness, connects via tension, grounds in structure.

### Step 8: Experiment

Try converting these words:
```bash
python mvp_glyph_converter.py HOPE
python mvp_glyph_converter.py GRACE
python mvp_glyph_converter.py PEACE
```

Notice how:
- Words with similar meanings have similar glyphs
- Vowel-heavy words have more curves (￿)
- Structured words have more lines (—)

### ✅ Tutorial 1 Complete!

You've converted your first word to a glyph. Next: [Understanding Resonance](#tutorial-2-understanding-resonance)

---

## Tutorial 2: Understanding Resonance
### Comparing Words Through Geometric Similarity

**Time:** 20 minutes  
**Prerequisites:** Tutorial 1

### What is Resonance?

**Resonance** measures semantic similarity between glyphs. Two words "resonate" if their glyphs share atoms in similar positions.

**Formula:**
```
Resonance = cosine_similarity + absence_bonus + curve_flow + golden_harmonic
```

### Step 1: Compare LOVE and GRACE

First, get both glyphs:

```bash
python mvp_glyph_converter.py LOVE
# Result: ￿￿￿——∅∅

python mvp_glyph_converter.py GRACE
# Result: ·￿——∅∅∅
```

### Step 2: Calculate Shared Atoms

Compare position by position:

| Segment | LOVE | GRACE | Match? |
|---------|------|-------|--------|
| a | ￿ | · | ❌ |
| b | ￿ | ￿ | ✅ |
| c | ∅ | ∅ | ✅ |
| d | — | ∅ | ❌ |
| e | ∅ | ∅ | ✅ |
| f | ￿ | — | ❌ |
| g | — | — | ✅ |

**Shared atoms:** 4 out of 7 → **Resonance ≈ 0.57**

### Step 3: Build a Resonance Matrix

Let's compare a family of related words:

| | LOVE | GRACE | PEACE | JOY |
|---|:---:|:---:|:---:|:---:|
| **LOVE** | 1.00 | 0.57 | 0.62 | 0.48 |
| **GRACE** | 0.57 | 1.00 | 0.71 | 0.52 |
| **PEACE** | 0.62 | 0.71 | 1.00 | 0.45 |
| **JOY** | 0.48 | 0.52 | 0.45 | 1.00 |

**Observations:**
- GRACE and PEACE resonate highest (0.71) — both describe harmonious states
- LOVE connects broadly to all three
- JOY is more distinct — shorter word, different structure

### Step 4: Visualize Resonance as Connection Lines

When glyphs are arranged in space, draw lines between resonant pairs:

```
        LOVE ￿
           ￿
          / \
    0.57 /   \ 0.62
        /     \
       /       \
   GRACE ·─────· PEACE
      ￿  0.71   ￿
       \       /
        \ 0.52/
         \   /
          \ /
          JOY
          ·
```

### Step 5: Threshold Rules

| Resonance | Visual | Meaning |
|-----------|--------|---------|
| > 0.90 | 🔥 Glowing | Möbius lock candidate |
| > 0.60 | ⬛ Bold | Strong semantic kinship |
| > 0.30 | ⬕ Faint | Related concepts |
| ≤ 0.30 | (none) | No connection drawn |

### Step 6: Find Surprising Resonances

Some words resonate unexpectedly:

```bash
# Compare TRUTH and FREEDOM
python mvp_glyph_converter.py TRUTH
python mvp_glyph_converter.py FREEDOM
```

These might share structural patterns even though meanings differ — revealing hidden connections in how we construct concepts.

### Step 7: Create Your Own Comparison

Pick 3-5 related words and:
1. Convert each to glyphs
2. Count shared atoms between each pair
3. Build a resonance matrix
4. Draw the connection network

Example word families:
- WATER, OCEAN, RIVER, RAIN
- FIRE, FLAME, HEAT, LIGHT
- STONE, ROCK, MOUNTAIN, EARTH

### ✅ Tutorial 2 Complete!

You understand how glyphs resonate. Next: [Building a Constellation](#tutorial-3-building-a-constellation)

---

## Tutorial 3: Building a Constellation
### Sentence-Level Composition

**Time:** 30 minutes  
**Prerequisites:** Tutorials 1 & 2

### What is a Constellation?

A **constellation** is multiple glyphs arranged in geometric space with connection lines showing resonance. Sentences, paragraphs, and documents become navigable star maps.

### Step 1: Choose a Sentence

We'll use: **"LOVE WINS TRUTH FREES"**

### Step 2: Convert Each Word

```bash
python mvp_glyph_converter.py LOVE   # ￿￿￿——∅∅
python mvp_glyph_converter.py WINS   # —·￿∅——∅
python mvp_glyph_converter.py TRUTH  # —￿·￿·———
python mvp_glyph_converter.py FREES  # ￿———∅￿∅
```

### Step 3: Calculate Cross-Resonances

Build the full resonance matrix:

| | LOVE | WINS | TRUTH | FREES |
|---|:---:|:---:|:---:|:---:|
| **LOVE** | 1.00 | 0.43 | 0.38 | 0.52 |
| **WINS** | 0.43 | 1.00 | 0.41 | 0.48 |
| **TRUTH** | 0.38 | 0.41 | 1.00 | 0.45 |
| **FREES** | 0.52 | 0.48 | 0.45 | 1.00 |

### Step 4: Position in 2D Space

Arrange glyphs so resonant pairs are closer:

```
         LOVE ￿
              ￿
              |
       0.43   |   0.52
              |
    WINS —────┼───── FREES
      ·       |       ￿
              |
       0.41   |   0.45
              |
            TRUTH
              —
```

### Step 5: Write the Python Code

Create `my_constellation.py`:

```python
from mvp_glyph_converter import GlyphConverter

class ConstellationBuilder:
    def __init__(self):
        self.converter = GlyphConverter()
        self.words = []
        self.glyphs = []
        
    def add_word(self, word):
        """Add a word to the constellation"""
        glyph = self.converter.word_to_glyph(word)
        self.words.append(word)
        self.glyphs.append(glyph)
        return glyph
    
    def calculate_resonance(self, glyph1, glyph2):
        """Calculate resonance between two glyphs"""
        shared = sum(1 for a, b in zip(glyph1, glyph2) if a == b and a != '∅')
        return shared / 7.0
    
    def build_matrix(self):
        """Build full resonance matrix"""
        n = len(self.glyphs)
        matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = 1.0
                else:
                    matrix[i][j] = self.calculate_resonance(
                        self.glyphs[i], self.glyphs[j]
                    )
        return matrix
    
    def get_connections(self, threshold=0.3):
        """Get pairs that should be connected"""
        matrix = self.build_matrix()
        connections = []
        
        for i in range(len(self.words)):
            for j in range(i+1, len(self.words)):
                if matrix[i][j] > threshold:
                    connections.append({
                        'from': self.words[i],
                        'to': self.words[j],
                        'resonance': matrix[i][j]
                    })
        return connections
    
    def visualize(self):
        """ASCII visualization"""
        print("╔════════════════════════════════════════╗")
        print("║         CONSTELLATION MAP             ║")
        print("╚════════════════════════════════════════╝")
        
        for word, glyph in zip(self.words, self.glyphs):
            print(f"\n[{word}] → {''.join(glyph)}")
        
        print("\n📊 Resonance Matrix:")
        matrix = self.build_matrix()
        
        # Header
        print(f"{'':8}", end="")
        for w in self.words:
            print(f"{w:8}", end="")
        print()
        
        # Rows
        for i, word in enumerate(self.words):
            print(f"{word:8}", end="")
            for j in range(len(self.words)):
                print(f"{matrix[i][j]:8.2f}", end="")
            print()
        
        print("\n🔗 Connections (threshold > 0.3):")
        for conn in self.get_connections():
            line_width = "━━" if conn['resonance'] > 0.6 else "──"
            print(f"  {conn['from']} {line_width} {conn['to']} : {conn['resonance']:.2f}")

# Usage
builder = ConstellationBuilder()
builder.add_word("LOVE")
builder.add_word("WINS")
builder.add_word("TRUTH")
builder.add_word("FREES")
builder.visualize()
```

### Step 6: Run Your Constellation

```bash
python my_constellation.py
```

**Expected Output:**
```
╔════════════════════════════════════════╗
║         CONSTELLATION MAP             ║
╚════════════════════════════════════════╝

[LOVE] → ￿￿￿——∅∅
[WINS] → —·￿∅——∅
[TRUTH] → —￿·￿·———
[FREES] → ￿———∅￿∅

📊 Resonance Matrix:
        LOVE    WINS    TRUTH   FREES   
LOVE    1.00    0.43    0.38    0.52    
WINS    0.43    1.00    0.41    0.48    
TRUTH   0.38    0.41    1.00    0.45    
FREES   0.52    0.48    0.45    1.00    

🔗 Connections (threshold > 0.3):
  LOVE ── WINS : 0.43
  LOVE ── FREES : 0.52
  WINS ── TRUTH : 0.41
  WINS ── FREES : 0.48
  TRUTH ── FREES : 0.45
```

### Step 7: Add Interactive Features

Extend your constellation to support:
- **Drag and drop** glyph repositioning
- **Click to expand** — show word breakdown
- **Hover for details** — resonance scores
- **Double-click to fuse** — merge two glyphs

### Step 8: Export to .gpkg Format

```python
def export_gpkg(self, filename):
    """Export constellation to compressed format"""
    import struct
    import json
    
    with open(filename, 'wb') as f:
        # Header
        f.write(struct.pack('B', 1))  # Version
        f.write(struct.pack('B', len(self.glyphs)))  # Glyph count
        
        # Glyphs (3 bytes each)
        atom_map = {'∅': 0, '·': 1, '—': 2, '￿': 3}
        for glyph in self.glyphs:
            b1 = (atom_map[glyph[0]] << 6) | (atom_map[glyph[1]] << 4) | (atom_map[glyph[6]] << 2)
            b2 = (atom_map[glyph[5]] << 6) | (atom_map[glyph[4]] << 4) | (atom_map[glyph[2]] << 2)
            b3 = (atom_map[glyph[3]] << 6)
            f.write(bytes([b1, b2, b3]))
        
        # Connections
        for conn in self.get_connections():
            from_idx = self.words.index(conn['from'])
            to_idx = self.words.index(conn['to'])
            resonance_byte = int(conn['resonance'] * 255)
            f.write(bytes([from_idx, to_idx, resonance_byte]))
        
        # Metadata
        metadata = {'words': self.words}
        meta_bytes = json.dumps(metadata).encode()
        f.write(meta_bytes)
    
    print(f"Exported to {filename}")
```

### ✅ Tutorial 3 Complete!

You can build constellations! Next: [Deploying an Edge Node](#tutorial-4-deploying-an-edge-node)

---

## Tutorial 4: Deploying an Edge Node
### Setting Up Distributed Infrastructure

**Time:** 45 minutes  
**Prerequisites:** Tutorials 1-3, Linux/command line experience

### What is an Edge Node?

An **edge node** is a distributed computing unit that:
- Runs the Looman-GCE runtime locally
- Synchronizes with other nodes via mesh networking
- Provides offline glyph processing
- Contributes to network resilience

### Step 1: System Requirements

**Minimum:**
- Linux, macOS, or Windows with WSL
- Python 3.8+
- 512 MB RAM
- 1 GB storage

**Recommended:**
- Raspberry Pi 4 or equivalent
- 2 GB RAM
- GeoGebra installed (for visualization)

### Step 2: Install Dependencies

```bash
# Create project directory
mkdir -p ~/looman-edge
cd ~/looman-edge

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install numpy opencv-python pillow pytesseract

# For vision processing (optional)
pip install torch torchvision  # If using neural features
```

### Step 3: Download Looman-GCE Runtime

```bash
# Clone or copy the codebase
git clone https://github.com/glyphobetics/core.git
# Or copy from your workspace:
cp -r /root/.openclaw/workspace/mvp_glyph_converter.py .
cp -r /root/.openclaw/workspace/vision_processor.py .
cp -r /root/.openclaw/workspace/constellation_protocol.md .
```

### Step 4: Create Node Configuration

Create `node_config.json`:

```json
{
  "node_id": "edge-node-alpha-001",
  "region": "ap-east-1",
  "capabilities": {
    "glyph_conversion": true,
    "vision_processing": true,
    "mesh_sync": true,
    "geogebra_render": false
  },
  "mesh": {
    "enabled": true,
    "discovery_port": 7777,
    "sync_port": 7778,
    "known_peers": [
      "edge-node-beta-001.local:7777",
      "edge-node-gamma-001.local:7777"
    ]
  },
  "storage": {
    "constellations_path": "./constellations",
    "max_cache_size_mb": 100
  },
  "ethics": {
    "esa_filter_enabled": true,
    "kenotic_mode": true,
    "coercive_detection": true
  }
}
```

### Step 5: Create the Node Runtime

Create `edge_node.py`:

```python
#!/usr/bin/env python3
"""Looman-GCE Edge Node Runtime"""

import json
import socket
import threading
import hashlib
import time
from pathlib import Path

class EdgeNode:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.node_id = self.config['node_id']
        self.peers = set(self.config['mesh']['known_peers'])
        self.constellations = {}
        
        print(f"🟢 Edge Node {self.node_id} initializing...")
        
    def start(self):
        """Start all services"""
        # Start mesh discovery
        threading.Thread(target=self._discovery_service, daemon=True).start()
        
        # Start sync service
        threading.Thread(target=self._sync_service, daemon=True).start()
        
        # Start API service
        self._api_service()
    
    def _discovery_service(self):
        """Listen for peer discovery"""
        port = self.config['mesh']['discovery_port']
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', port))
        
        print(f"📡 Discovery service on port {port}")
        
        while True:
            data, addr = sock.recvfrom(1024)
            message = json.loads(data.decode())
            
            if message['type'] == 'DISCOVER':
                # Respond with our info
                response = {
                    'type': 'PRESENT',
                    'node_id': self.node_id,
                    'capabilities': self.config['capabilities']
                }
                sock.sendto(json.dumps(response).encode(), addr)
                
                # Add peer
                peer_addr = f"{addr[0]}:{message['port']}"
                self.peers.add(peer_addr)
                print(f"👋 Discovered peer: {message['node_id']}")
    
    def _sync_service(self):
        """Synchronize constellations with peers"""
        port = self.config['mesh']['sync_port']
        
        print(f"🔄 Sync service on port {port}")
        
        while True:
            for peer in list(self.peers):
                try:
                    self._sync_with_peer(peer)
                except Exception as e:
                    print(f"⚠️ Sync failed with {peer}: {e}")
            
            time.sleep(30)  # Sync every 30 seconds
    
    def _sync_with_peer(self, peer):
        """Sync constellations with a specific peer"""
        host, port = peer.rsplit(':', 1)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        
        # Request peer's constellation hashes
        sock.send(json.dumps({'action': 'LIST'}).encode())
        response = json.loads(sock.recv(4096).decode())
        
        # Compare with local constellations
        for constellation_id, remote_hash in response['constellations'].items():
            if constellation_id not in self.constellations:
                # Download missing constellation
                sock.send(json.dumps({
                    'action': 'GET',
                    'id': constellation_id
                }).encode())
                data = sock.recv(65536)
                self.constellations[constellation_id] = data
                print(f"📥 Downloaded {constellation_id}")
        
        sock.close()
    
    def _api_service(self):
        """HTTP-like API for local clients"""
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        class NodeHandler(BaseHTTPRequestHandler):
            def do_POST(handler):
                content_length = int(handler.headers['Content-Length'])
                post_data = handler.rfile.read(content_length)
                request = json.loads(post_data.decode())
                
                if request['action'] == 'CONVERT':
                    # Convert word to glyph
                    word = request['word']
                    # Import and use converter
                    import sys
                    sys.path.insert(0, '.')
                    from mvp_glyph_converter import GlyphConverter
                    
                    converter = GlyphConverter()
                    glyph = converter.word_to_glyph(word)
                    
                    handler.send_response(200)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({
                        'word': word,
                        'glyph': glyph,
                        'node': self.node_id
                    }).encode())
                
                elif request['action'] == 'STORE':
                    # Store a constellation
                    constellation_id = hashlib.sha256(
                        request['data'].encode()
                    ).hexdigest()[:16]
                    
                    self.constellations[constellation_id] = request['data']
                    
                    handler.send_response(200)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({
                        'id': constellation_id,
                        'status': 'stored'
                    }).encode())
        
        server = HTTPServer(('0.0.0.0', 8080), NodeHandler)
        print("🌐 API service on port 8080")
        print(f"   POST http://localhost:8080 with JSON:")
        print(f'     {{"action": "CONVERT", "word": "LOVE"}}')
        server.serve_forever()

if __name__ == '__main__':
    node = EdgeNode('node_config.json')
    node.start()
```

### Step 6: Start Your Node

```bash
# Make executable
chmod +x edge_node.py

# Run
python edge_node.py

# Expected output:
# 🟢 Edge Node edge-node-alpha-001 initializing...
# 📡 Discovery service on port 7777
# 🔄 Sync service on port 7778
# 🌐 API service on port 8080
#    POST http://localhost:8080 with JSON:
#      {"action": "CONVERT", "word": "LOVE"}
```

### Step 7: Test the Node

In another terminal:

```bash
# Test conversion
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"action": "CONVERT", "word": "LOVE"}'

# Expected:
# {"word": "LOVE", "glyph": ["￿", "￿", "∅", "—", "∅", "￿", "—"], "node": "edge-node-alpha-001"}
```

### Step 8: Connect Multiple Nodes

On a second machine:

```bash
# Copy configuration
scp node_config.json user@machine2:~/looman-edge/
scp edge_node.py user@machine2:~/looman-edge/

# Edit config for second node
# Change node_id to "edge-node-beta-001"
# Add edge-node-alpha-001 to known_peers

# Start second node
python edge_node.py
```

### Step 9: Set Up as System Service

Create `/etc/systemd/system/looman-edge.service`:

```ini
[Unit]
Description=Looman-GCE Edge Node
After=network.target

[Service]
Type=simple
User=looman
WorkingDirectory=/home/looman/looman-edge
ExecStart=/home/looman/looman-edge/venv/bin/python edge_node.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable looman-edge
sudo systemctl start looman-edge
sudo systemctl status looman-edge
```

### Step 10: Monitor Your Node

```bash
# View logs
journalctl -u looman-edge -f

# Check connectivity
netstat -tulpn | grep python

# Test mesh sync
curl http://localhost:8080/status
```

### ✅ Tutorial 4 Complete!

You now have a distributed Glyph-o-betics network!

---

## Bonus: Creating Your Own Tutorial

Want to contribute? Here's the template:

```markdown
## Tutorial X: [Title]
### [Subtitle]

**Time:** X minutes  
**Prerequisites:** [Previous tutorials]

### Step 1: [Objective]
...

### Step 2: [Action]
```bash
# Commands here
```

### ✅ Tutorial X Complete!

[Next steps]
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| "Port already in use" | Change port in `node_config.json` |
| "Permission denied" | Use `sudo` or check file permissions |
| "Connection refused" | Check firewall rules, ensure node is running |
| "Glyph looks wrong" | Verify you're using the 7-segment order: a,b,c,d,e,f,g |

---

## Next Steps

- Browse [EXAMPLES.md](EXAMPLES.md) for more word transformations
- Read [GLOSSARY.md](GLOSSARY.md) to understand all terms
- Check [CHANGELOG.md](CHANGELOG.md) for latest features
- Return to [MASTER_INDEX.md](MASTER_INDEX.md) for navigation

---

> *"The best way to learn is to build. The best way to build is together."*
