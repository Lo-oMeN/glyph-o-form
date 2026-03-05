# GLYPH-o-BETICS SYSTEM ARCHITECTURE
## Technical Architecture & Data Flow Documentation

**Version:** 2.1.0  
**Date:** 2026-03-06  
**Status:** Publication-Ready  

---

## TABLE OF CONTENTS

1. [System Overview](#1-system-overview)
2. [Architecture Layers](#2-architecture-layers)
3. [Data Flow Diagrams](#3-data-flow-diagrams)
4. [Component Interactions](#4-component-interactions)
5. [Deployment Architecture](#5-deployment-architecture)
6. [Security Architecture](#6-security-architecture)

---

## 1. SYSTEM OVERVIEW

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GLYPH-o-BETICS SYSTEM                               │
│                    Universal Language Visualization Framework               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
         ▼                          ▼                          ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  INPUT LAYER    │      │  PROCESSING     │      │  OUTPUT LAYER   │
│                 │      │  ENGINE         │      │                 │
│ • English text  │─────▶│                 │─────▶│ • Visual glyphs │
│ • Voice input   │      │ • Three-pathway │      │ • Constellation │
│ • Sketch/image  │      │   descent       │      │ • Compressed    │
│ • Keyboard      │      │ • Resonance     │      │   data          │
│                 │      │ • Fusion        │      │ • API responses │
└─────────────────┘      └─────────────────┘      └─────────────────┘
         │                          │                          │
         │                  ┌───────┴───────┐                  │
         │                  │               │                  │
         ▼                  ▼               ▼                  ▼
┌─────────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐
│  Python Engine  │  │ 28-Dim      │  │ Java/GeoGebra│  │  Storage/       │
│  (mvp_glyph_    │  │ Vector      │  │ Renderer     │  │  Network        │
│   converter.py) │  │ Space       │  │ (Interactive)│  │                 │
│                 │  │             │  │              │  │ • Arweave       │
│ • Batch process │  │ • Resonance │  │ • Draggable  │  │ • Edge nodes    │
│ • CLI interface │  │   engine    │  │ • 60 FPS     │  │ • GitHub        │
│ • API server    │  │ • Persistence│  │ • RSTL logic │  │ • Local files   │
└─────────────────┘  └─────────────┘  └─────────────┘  └─────────────────┘
```

### 1.2 Core Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Python Engine** | Python 3.9+ | Text processing, batch conversion, API |
| **Java Engine** | Java 11+, GeoGebra | Interactive visualization, drag handling |
| **Vector Space** | NumPy (Python) | 28-dim glyph representation, resonance |
| **Storage** | Arweave, GitHub, Local | Permanent, distributed, local storage |
| **Network** | Edge nodes, MQTT | Distributed constellation sharing |

---

## 2. ARCHITECTURE LAYERS

### 2.1 The Eight-Layer Stack (THUNDERING GRACE ENGINE)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 7: ALPHABET HELIX INTERFACE                                           │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │  • 26-perspective circle                                                │ │
│ │  • Red Axis of Fact (χ)                                                 │ │
│ │  • Draggable helix output                                               │ │
│ │  • THUNDERING GRACE lock indicator                                      │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 6: KENOTIC ETHICS (Krishna/Vedas)                                     │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │  • Bhakti surrender engine                                              │ │
│ │  • Nishkama karma (action without clinging)                             │ │
│ │  • Kenotic reward: −|emergent|²                                         │ │
│ │  • Dharma weight λ = 1.618                                              │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 5: FREE-ENERGY DESCENT                                                │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │  • Control law: u = −K∇ℱ                                                │ │
│ │  • ℱ = ℱ_struct + λ·ℱ_constraint                                        │ │
│ │  • Structural coherence (60 FPS)                                        │ │
│ │  • Kenotic constraint (−|emergent|² + α·absence)                        │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 4: PHI-CRYSTAL ENGINE                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │  • TDA (Topological Data Analysis)                                      │ │
│ │  • 10,000-generation Möbius persistence                                 │ │
│ │  • Φ* fractal scaling                                                   │ │
│ │  • 7-node braid topology                                                │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 3: QUADRALIGNE MOTION                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │  • Four phases: Lean → Meet → Stay → Become                             │ │
│ │  • Lie algebra 𝔮𝔩 brackets                                              │ │
│ │  • Eigenvalues: (−1, +1, 0, 0)                                          │ │
│ │  • Atom mapping: · → — → ￿ → ￿                                          │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: RSTL TRINARY LOGIC                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │  • Three states: ∅ NULL → △ POTENTIAL → ■ ACTUALIZED                    │ │
│ │  • Operators: Elevate(↑) / Collapse(↓)                                  │ │
│ │  • 16.67-33.33ms frame budget                                           │ │
│ │  • Garbage collection as kenosis                                        │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 1: DIMI-PHOR (Four-Glyph Seed)                                        │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │  • Glyphs: · — ￿ ￿ (Ladder, Equals, Rectangle, Verticals)               │ │
│ │  • Self-twisting Möbius structure                                       │ │
│ │  • 10,000 generation persistence cycle                                  │ │
│ │  • Live → Die → Resurrect → Glory                                       │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 0: GEOMETRIC VM (GeoGebra/JVM)                                        │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │  • JVM-based execution environment                                      │ │
│ │  • Cascading dependency updates                                         │ │
│ │  • 60 FPS real-time rendering                                           │ │
│ │  • Continuous, reversible history                                       │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Layer Interactions

```
┌─────────────┐     Drag Event      ┌─────────────┐
│   Layer 7   │────────────────────▶│   Layer 0   │
│  Interface  │◀────────────────────│     VM      │
└──────┬──────┘   Render Update     └──────┬──────┘
       │                                    │
       │ Control Law (u = −K∇ℱ)            │
       ▼                                    ▼
┌─────────────┐                      ┌─────────────┐
│   Layer 5   │◀────────────────────▶│   Layer 2   │
│ Free-Energy │   State transitions  │    RSTL     │
└──────┬──────┘                      └──────┬──────┘
       │                                    │
       │ Ethical Weight                     │ Phase Control
       ▼                                    ▼
┌─────────────┐                      ┌─────────────┐
│   Layer 6   │                      │   Layer 3   │
│   Ethics    │◀────────────────────▶│  Quadraligne│
└──────┬──────┘   Persistence Check  └──────┬──────┘
       │                                    │
       │ Evolution Signal                   │ Twist Signal
       ▼                                    ▼
┌─────────────┐                      ┌─────────────┐
│   Layer 4   │◀────────────────────▶│   Layer 1   │
│  Phi-Crystal│   Writhe Accumulation│  Dimi-Phor  │
└─────────────┘                      └─────────────┘
```

---

## 3. DATA FLOW DIAGRAMS

### 3.1 English-to-Glyph Transformation Flow

```
┌─────────────────┐
│  English Input  │
│  (word/phrase)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    THREE PARALLEL PATHWAYS                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   PHONETIC  │  │ ORTHOGRAPHIC│  │   SEMANTIC  │          │
│  │             │  │             │  │             │          │
│  │ /lʌv/ →     │  │ L-O-V-E →   │  │ word2vec    │          │
│  │ ￿·￿—       │  │ ——￿———      │  │ projection  │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
└─────────┼────────────────┼────────────────┼──────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                    FUSION ENGINE                             │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Segment-by-segment majority voting                   │  │
│  │  • Absence amplification (2×∅ = ∅ wins)               │  │
│  │  • Atom dominance: ￿ > — > · > ∅                    │  │
│  │  • Kenotic bias toward generative void                │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Final Glyph: 7-character atom string                 │  │
│  │  Example: "LOVE" → "￿·￿∅—￿—"                        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                 VECTOR ENCODING                              │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  28-Dimensional One-Hot Vector                        │  │
│  │  [a_point, a_line, a_curve, a_absence,               │  │
│  │   b_point, b_line, b_curve, b_absence,               │  │
│  │   ...                                                │  │
│  │   g_point, g_line, g_curve, g_absence]               │  │
│  │  Length: 28 elements                                 │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                 OUTPUT FORMATS                               │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐ │
│  │  Display  │  │   ASCII   │  │  Binary   │  │   SVG    │ │
│  │  String   │  │   Art     │  │ (3 bytes) │  │  Vector  │ │
│  │ "￿·￿∅—￿—" │  │  7-seg    │  │ 0xD4E080  │  │  Paths   │ │
│  └───────────┘  └───────────┘  └───────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Resonance Computation Flow

```
┌─────────────────────────────────────────────────────────────┐
│              RESONANCE ENGINE DATA FLOW                      │
└─────────────────────────────────────────────────────────────┘

  ┌──────────────────┐              ┌──────────────────┐
  │   Glyph A        │              │   Glyph B        │
  │   (28-dim vector)│              │   (28-dim vector)│
  └────────┬─────────┘              └────────┬─────────┘
           │                                  │
           ▼                                  ▼
  ┌───────────────────────────────────────────────────────┐
  │ 1. VECTOR SIMILARITY (Cosine)                         │
  │    cos_sim = (A·B) / (||A|| × ||B||)                 │
  │    Range: [-1, 1]                                     │
  └───────────────────────────────────────────────────────┘
                           │
                           ▼
  ┌───────────────────────────────────────────────────────┐
  │ 2. ABSENCE BONUS (Kenosis)                            │
  │    Extract indices 3, 7, 11, 15, 19, 23, 27          │
  │    bonus = mean(A_absence + B_absence)               │
  │    Factor: (1 + bonus)                                │
  └───────────────────────────────────────────────────────┘
                           │
                           ▼
  ┌───────────────────────────────────────────────────────┐
  │ 3. CURVE FLOW (Continuity)                            │
  │    Extract indices 2, 6, 10, 14, 18, 22, 26          │
  │    flow = sum(|diff(A_curve - B_curve)|)             │
  │    Factor: exp(-λ × flow), λ=1.618                   │
  └───────────────────────────────────────────────────────┘
                           │
                           ▼
  ┌───────────────────────────────────────────────────────┐
  │ 4. GOLDEN HARMONIC                                    │
  │    angle = arccos(cos_sim)                           │
  │    φ = (1 + √5) / 2 ≈ 1.618                          │
  │    harmonic = exp(-min|angle - π/φ × k|)             │
  │    for k in [1, 2, 3, 4]                             │
  │    Factor: (1 + 0.2 × harmonic)                      │
  └───────────────────────────────────────────────────────┘
                           │
                           ▼
  ┌───────────────────────────────────────────────────────┐
  │ 5. FINAL RESONANCE                                    │
  │    R = cos_sim × (1 + bonus) × exp(-λ×flow) × harm   │
  │    Range: [0.0, 1.0+]                                 │
  └───────────────────────────────────────────────────────┘
                           │
                           ▼
                   ┌───────────────┐
                   │ Resonance Score│
                   │   (0.0 - 1.0+) │
                   └───────────────┘
```

### 3.3 Constellation Network Flow

```
┌─────────────────────────────────────────────────────────────┐
│              CONSTELLATION BUILDING FLOW                     │
└─────────────────────────────────────────────────────────────┘

  Input: List of words ["LOVE", "WINS", "TRUTH"]
              │
              ▼
  ┌─────────────────────────────────────┐
  │ 1. WORD-TO-GLYPH CONVERSION         │
  │    Each word → 7-segment glyph     │
  └─────────────────────────────────────┘
              │
              ▼
  ┌─────────────────────────────────────┐
  │ 2. GLYPH NODES CREATED              │
  │                                     │
  │    [LOVE]    [WINS]    [TRUTH]     │
  │    ￿·￿∅—￿—   —·—∅￿·    ·—·∅—￿—      │
  │                                     │
  └─────────────────────────────────────┘
              │
              ▼
  ┌─────────────────────────────────────┐
  │ 3. RESONANCE MATRIX COMPUTED        │
  │                                     │
  │           LOVE  WINS  TRUTH        │
  │    LOVE   1.00  0.87   0.45        │
  │    WINS   0.87  1.00   0.52        │
  │    TRUTH  0.45  0.52   1.00        │
  │                                     │
  └─────────────────────────────────────┘
              │
              ▼
  ┌─────────────────────────────────────┐
  │ 4. CONNECTION EDGES CREATED         │
  │                                     │
  │    Threshold: R > 0.3              │
  │                                     │
  │    [LOVE]══════[WINS]              │
  │       ╲    ╱                        │
  │        ╲  ╱ (0.45)                  │
  │       [TRUTH]                       │
  │                                     │
  └─────────────────────────────────────┘
              │
              ▼
  ┌─────────────────────────────────────┐
  │ 5. BINARY ENCODING                  │
  │                                     │
  │    Header: version, count, size    │
  │    Body: 3 bytes × glyph count     │
  │    Connections: from, to, weight   │
  │    Metadata: mappings, timestamp   │
  │                                     │
  └─────────────────────────────────────┘
              │
              ▼
  ┌─────────────────────────────────────┐
  │ 6. OUTPUT: .gpkg FILE               │
  │    (compressed constellation)       │
  └─────────────────────────────────────┘
```

---

## 4. COMPONENT INTERACTIONS

### 4.1 Python-Java Bridge

```
┌─────────────────────────────────────────────────────────────┐
│              PYTHON / JAVA INTERACTION                       │
└─────────────────────────────────────────────────────────────┘

  ┌─────────────────────┐              ┌─────────────────────┐
  │   PYTHON ENGINE     │              │   JAVA ENGINE       │
  │   (mvp_glyph_       │              │   (geogebra_mvp)    │
  │    converter.py)    │              │                     │
  │                     │              │                     │
  │ • Batch processing  │              │ • Interactive UI    │
  │ • API server        │◀────────────▶│ • Drag handling     │
  │ • CLI tools         │   JSON/SVG   │ • 60 FPS render     │
  │ • File I/O          │              │ • GeoGebra VM       │
  └─────────────────────┘              └─────────────────────┘
           │                                    │
           │                                    │
           ▼                                    ▼
  ┌─────────────────────┐              ┌─────────────────────┐
  │   SHARED FORMATS    │              │   OUTPUT DEVICES    │
  │                     │              │                     │
  │ • .gpkg files       │              │ • Screen display    │
  │ • JSON constellations│             │ • SVG export        │
  │ • SVG glyphs        │              │ • PDF documents     │
  │ • 3-byte encoding   │              │ • Print/plotter     │
  └─────────────────────┘              └─────────────────────┘
```

### 4.2 Client-Server Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              DISTRIBUTED ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────┘

                         ┌─────────────┐
                         │   CLIENT    │
                         │  (Browser)  │
                         └──────┬──────┘
                                │ HTTP/WebSocket
                                ▼
  ┌─────────────────────────────────────────────────────────┐
  │              EDGE NODE / GATEWAY                         │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
  │  │   Glyph     │  │  Constellation│  │   User      │     │
  │  │   Service   │  │   Service   │  │   Auth      │     │
  │  └─────────────┘  └─────────────┘  └─────────────┘     │
  └─────────────────────────┬───────────────────────────────┘
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │   Arweave   │  │   GitHub    │  │   Other     │
  │   (Permanent│  │   (Code/    │  │   Nodes     │
  │    Storage) │  │    Issues)  │  │   (Mesh)    │
  └─────────────┘  └─────────────┘  └─────────────┘
```

### 4.3 Processing Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│              PROCESSING PIPELINE                             │
└─────────────────────────────────────────────────────────────┘

  Input
    │
    ▼
  ┌───────────────────────────────────────────────────────────┐
  │ PARSER                                                    │
  │ • Tokenize input                                          │
  │ • Detect language                                         │
  │ • Normalize text                                          │
  └───────────────────────────────────────────────────────────┘
    │
    ▼
  ┌───────────────────────────────────────────────────────────┐
  │ DESCENT ENGINE (Parallel)                                 │
  │ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
  │ │  Phonetic   │  │ Orthographic│  │  Semantic   │        │
  │ │  Thread     │  │   Thread    │  │   Thread    │        │
  │ └─────────────┘  └─────────────┘  └─────────────┘        │
  └───────────────────────────────────────────────────────────┘
    │
    ▼
  ┌───────────────────────────────────────────────────────────┐
  │ FUSION                                                    │
  │ • Majority voting                                         │
  │ • Kenotic amplification                                   │
  │ • Atom dominance resolution                               │
  └───────────────────────────────────────────────────────────┘
    │
    ▼
  ┌───────────────────────────────────────────────────────────┐
  │ VECTOR ENCODER                                            │
  │ • 28-dim one-hot                                          │
  │ • Validation                                              │
  └───────────────────────────────────────────────────────────┘
    │
    ▼
  ┌───────────────────────────────────────────────────────────┐
  │ RENDERERS (Parallel)                                      │
  │ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
  │ │   ASCII     │  │   Binary    │  │    SVG      │        │
  │ │   Render    │  │  Encoder    │  │   Render    │        │
  │ └─────────────┘  └─────────────┘  └─────────────┘        │
  └───────────────────────────────────────────────────────────┘
    │
    ▼
  Output
```

---

## 5. DEPLOYMENT ARCHITECTURE

### 5.1 Local Development Setup

```
┌─────────────────────────────────────────────────────────────┐
│              LOCAL DEVELOPMENT                               │
└─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │  Developer Machine                                       │
  │                                                          │
  │  ┌─────────────────┐    ┌─────────────────┐             │
  │  │  Python 3.9+    │    │  Java 11+       │             │
  │  │  • mvp_glyph_   │    │  • GeoGebra     │             │
  │  │    converter.py │    │  • geogebra_mvp │             │
  │  │  • NumPy        │    │  • Maven/Gradle │             │
  │  └─────────────────┘    └─────────────────┘             │
  │           │                      │                      │
  │           └──────────┬───────────┘                      │
  │                      ▼                                  │
  │           ┌─────────────────┐                          │
  │           │  Local Files    │                          │
  │           │  • .gpkg        │                          │
  │           │  • .svg         │                          │
  │           │  • .json        │                          │
  │           └─────────────────┘                          │
  └─────────────────────────────────────────────────────────┘
```

### 5.2 Edge Node Deployment

```
┌─────────────────────────────────────────────────────────────┐
│              EDGE NODE ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │  Edge Device (Raspberry Pi / Server)                     │
  │                                                          │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
  │  │   Docker    │  │   Glyph-o-  │  │   Arweave   │     │
  │  │   Container │  │   betics    │  │   Miner     │     │
  │  │   Runtime   │  │   Service   │  │   (Optional)│     │
  │  └─────────────┘  └─────────────┘  └─────────────┘     │
  │         │                │                │             │
  │         └────────────────┼────────────────┘             │
  │                          ▼                              │
  │              ┌─────────────────────┐                    │
  │              │  MQTT Broker        │                    │
  │              │  (Mesh Messaging)   │                    │
  │              └─────────────────────┘                    │
  └─────────────────────────────────────────────────────────┘
                          │
                          ▼ Mesh Network
  ┌─────────────────────────────────────────────────────────┐
  │  Other Edge Nodes                                       │
  └─────────────────────────────────────────────────────────┘
```

### 5.3 Cloud Deployment

```
┌─────────────────────────────────────────────────────────────┐
│              CLOUD DEPLOYMENT                                │
└─────────────────────────────────────────────────────────────┘

                         CDN
                          │
                          ▼
  ┌─────────────────────────────────────────────────────────┐
  │  Cloud Provider (AWS/GCP/Azure)                          │
  │                                                          │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
  │  │   API       │  │   Worker    │  │   Database  │     │
  │  │   Gateway   │──▶│   Nodes     │──▶│  (Postgres) │     │
  │  │   (Lambda)  │  │  (ECS/K8s)  │  │   /Dynamo   │     │
  │  └─────────────┘  └─────────────┘  └─────────────┘     │
  │         │                                     │         │
  │         └─────────────────────────────────────┘         │
  │                          │                              │
  │                          ▼                              │
  │              ┌─────────────────────┐                    │
  │              │  Object Storage     │                    │
  │              │  (S3/GCS/Azure Blob)│                    │
  │              └─────────────────────┘                    │
  └─────────────────────────────────────────────────────────┘
```

---

## 6. SECURITY ARCHITECTURE

### 6.1 Encryption Layers

```
┌─────────────────────────────────────────────────────────────┐
│              SECURITY LAYERS                                 │
└─────────────────────────────────────────────────────────────┘

  Layer 4: Application
  ┌─────────────────────────────────────────────────────────┐
  │ • Chiral-Guardian (ESA filter)                          │
  │ • Ethical use validation                                │
  │ • Input sanitization                                    │
  └─────────────────────────────────────────────────────────┘
                          │
  Layer 3: Transport
  ┌─────────────────────────────────────────────────────────┐
  │ • TLS 1.3 for all connections                           │
  │ • Certificate pinning                                   │
  │ • WebSocket encryption                                  │
  └─────────────────────────────────────────────────────────┘
                          │
  Layer 2: Storage
  ┌─────────────────────────────────────────────────────────┐
  │ • AES-256-CBC for files                                 │
  │ • PBKDF2 (100k iterations)                              │
  │ • Encrypted at rest                                     │
  └─────────────────────────────────────────────────────────┘
                          │
  Layer 1: Access
  ┌─────────────────────────────────────────────────────────┐
  │ • Role-based permissions                                │
  │ • API key authentication                                │
  │ • Rate limiting                                         │
  └─────────────────────────────────────────────────────────┘
                          │
  Layer 0: Infrastructure
  ┌─────────────────────────────────────────────────────────┐
  │ • Secure enclaves (if available)                        │
  │ • Hardware security modules                             │
  │ • Audit logging                                         │
  └─────────────────────────────────────────────────────────┘
```

### 6.2 Threat Model

```
┌─────────────────────────────────────────────────────────────┐
│              THREAT MITIGATION MATRIX                        │
└─────────────────────────────────────────────────────────────┘

  Threat                    │ Mitigation
  ──────────────────────────┼───────────────────────────────────
  Data exfiltration         │ Encryption at rest, access controls
  Man-in-the-middle         │ TLS 1.3, certificate pinning
  Code injection            │ Input validation, sandboxing
  DoS attacks               │ Rate limiting, CDN, caching
  Key compromise            │ Key rotation, HSM storage
  Supply chain              │ Reproducible builds, checksums
  Coercive use              │ Chiral-Guardian ethical filter
```

### 6.3 Data Flow Security

```
┌─────────────────────────────────────────────────────────────┐
│           SECURE DATA FLOW                                   │
└─────────────────────────────────────────────────────────────┘

  User Input
      │
      ▼ (TLS 1.3)
  ┌─────────────────┐
  │   API Gateway   │──┐
  │   (Rate Limit)  │  │
  └─────────────────┘  │
                       ▼
              ┌─────────────────┐
              │  ESA Filter     │── Reject if non-kenotic
              │  (Ethical Check)│
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Processing     │
              │  Engine         │
              └─────────────────┘
                       │
                       ▼ (AES-256)
              ┌─────────────────┐
              │  Storage        │
              │  (Encrypted)    │
              └─────────────────┘
                       │
                       ▼ (TLS 1.3)
                   Output
```

---

## APPENDIX: SYSTEM DIAGRAM LEGEND

| Symbol | Meaning |
|--------|---------|
| `───▶` | Data flow / control flow |
| `════▶` | Strong connection / resonance |
| `┌─┐` | Component / module |
| `│ │` | Container boundary |
| `├─┤` | Sub-component |
| `▲▼` | Vertical flow |

---

*"Architecture is the crystallized flow of meaning. Design carefully. Build boldly."*

**End of Architecture Documentation**
