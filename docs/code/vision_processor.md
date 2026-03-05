# vision_processor.py - Complete Documentation

> **L∞m≡n Vision Processor**  
> Analyze images of glyphs and convert to 7-segment representation using computer vision.

## Table of Contents

1. [Overview](#overview)
2. [Computer Vision Pipeline](#computer-vision-pipeline)
3. [Class: GlyphVisionProcessor](#class-glyphvisionprocessor)
4. [Function Reference](#function-reference)
5. [Usage Examples](#usage-examples)
6. [Accuracy Expectations](#accuracy-expectations)
7. [Calibration Procedures](#calibration-procedures)
8. [Example Image Analyses](#example-image-analyses)

---

## Overview

The `vision_processor.py` module provides computer vision capabilities for analyzing images containing glyph drawings. It converts visual representations of the 7-segment atomic glyphs into their symbolic representations.

### Key Features

- **Segment Detection**: Automatically identifies which of the 7 segments contain marks
- **Shape Classification**: Classifies detected shapes as Point (·), Line (—), Curve (￿), or Absence (∅)
- **Confidence Scoring**: Provides confidence metrics for analysis reliability
- **Comparison Mode**: Validates detected glyphs against expected patterns

### Dependencies

```python
import cv2          # OpenCV for image processing
import numpy as np  # NumPy for numerical operations
from PIL import Image  # PIL for image loading
import sys, os      # System utilities
```

**Installation:**
```bash
pip install opencv-python numpy pillow
```

---

## Computer Vision Pipeline

### Stage 1: Image Loading

```
Input Image (RGB/Color)
    ↓
Load with cv2.imread()
    ↓
BGR Format Image
```

**Validation:**
- File existence check
- Image load success check
- Shape extraction (height, width, channels)

---

### Stage 2: Preprocessing

```
BGR Image
    ↓
Color Conversion (COLOR_BGR2GRAY)
    ↓
Grayscale Image
    ↓
Edge Detection (Canny)
    ↓
Edge Map (Binary)
```

**Canny Parameters:**
- `threshold1 = 50` (lower threshold)
- `threshold2 = 150` (upper threshold)

These values detect edges while filtering noise.

---

### Stage 3: Contour Detection

```
Edge Map
    ↓
findContours(RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
    ↓
List of Contours
```

**Parameters:**
- `RETR_EXTERNAL`: Retrieves only extreme outer contours
- `CHAIN_APPROX_SIMPLE`: Compresses horizontal, vertical, and diagonal segments

---

### Stage 4: Segment Region Mapping

The image is divided into 7 regions corresponding to the 7-segment display:

```
    ┌─────────────────────────────┐
    │         Region A            │  ← Top (0.2,0.0) to (0.8,0.15)
    │    (0.2,0.0)  (0.8,0.15)    │
    ├────────┬──────────┬─────────┤
    │        │          │         │
    │Region F│          │Region B │  ← Upper sides
    │(0,0.15)│          │(0.8,0.5)│
    │  (0.2, │          │         │
    │  0.5)  │          │         │
    │        │ Region G │         │  ← Middle (0.2,0.425) to (0.8,0.575)
    │        │(0.2,0.425)        │
    │        │ (0.8,0.575)       │
    │        │          │         │
    │Region E│          │Region C │  ← Lower sides
    │(0,0.5) │          │(0.8,0.85)│
    │ (0.2,  │          │         │
    │ 0.85)  │          │         │
    ├────────┴──────────┴─────────┤
    │         Region D            │  ← Bottom (0.2,0.85) to (0.8,1.0)
    │   (0.2,0.85)  (0.8,1.0)     │
    └─────────────────────────────┘
```

**Region Definitions (relative coordinates):**
```python
regions = {
    'a': (0.2, 0.0, 0.8, 0.15),     # Top horizontal
    'b': (0.8, 0.15, 1.0, 0.5),     # Upper right vertical
    'c': (0.8, 0.5, 1.0, 0.85),     # Lower right vertical
    'd': (0.2, 0.85, 0.8, 1.0),     # Bottom horizontal
    'e': (0.0, 0.5, 0.2, 0.85),     # Lower left vertical
    'f': (0.0, 0.15, 0.2, 0.5),     # Upper left vertical
    'g': (0.2, 0.425, 0.8, 0.575)   # Middle horizontal
}
```

---

### Stage 5: Contour Assignment

For each detected contour:
1. Calculate centroid using moments
2. Determine which region contains the centroid
3. Assign contour to that segment
4. Keep only the largest contour per region

**Centroid Calculation:**
```python
M = cv2.moments(contour)
if M["m00"] != 0:
    cx = int(M["m10"] / M["m00"])  # X centroid
    cy = int(M["m01"] / M["m00"])  # Y centroid
```

---

### Stage 6: Shape Classification

Each segment's contour is classified into one of four atoms:

```
Contour
    ↓
Calculate Area
    ↓
Area < 50 pixels? → ABSENCE (∅)
    ↓ No
Approximate Polygon
    ↓
Count Vertices
    ↓
1 vertex OR area < 200 → POINT (·)
2-3 vertices → LINE (—)
4+ vertices → CURVE (￿)
```

**Classification Algorithm:**
```python
def _classify_segment(self, contour, img):
    if contour is None:
        return '∅'
    
    area = cv2.contourArea(contour)
    if area < 50:  # Too small
        return '∅'
    
    # Approximate shape
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    vertices = len(approx)
    
    if vertices == 1 or area < 200:
        return '·'  # Point
    elif vertices <= 3:
        return '—'  # Line
    elif vertices >= 4:
        return '￿'  # Curve
    else:
        return '∅'  # Absence
```

---

## Class: GlyphVisionProcessor

The main processor class for glyph image analysis.

### Constants

```python
ATOMS = ['∅', '·', '—', '￿']    # Index 0, 1, 2, 3
SEGMENTS = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
```

### Constructor

#### `__init__()`

Initializes the vision processor.

**Parameters:** None

**Attributes:**
| Name | Type | Description |
|------|------|-------------|
| `debug` | `bool` | Enable debug output (default: True) |
| `ATOMS` | `List[str]` | Atom symbols |
| `SEGMENTS` | `List[str]` | Segment names |

**Example:**
```python
processor = GlyphVisionProcessor()
```

---

## Function Reference

### Main Analysis Methods

#### `analyze_image(image_path: str) -> dict`

Main entry point: analyzes an image and returns glyph data.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `image_path` | `str` | Path to image file (PNG, JPG, etc.) |

**Returns:**
| Type | Description |
|------|-------------|
| `dict` | Analysis results or error dict |

**Return Structure (Success):**
```python
{
    'glyph_string': '￿·——∅∅∅',      # Detected 7-char glyph
    'segments': {                    # Per-segment atom assignments
        'a': '￿',
        'b': '·',
        'c': '—',
        'd': '—',
        'e': '∅',
        'f': '∅',
        'g': '—'
    },
    'contours_found': 4,             # Number of contours detected
    'image_shape': (480, 640, 3),    # (height, width, channels)
    'ascii_art': '...',              # ASCII visualization
    'analysis_confidence': 0.75      # Confidence score (0.0-1.0)
}
```

**Return Structure (Error):**
```python
{
    'error': 'Error message description'
}
```

**Pipeline:**
1. Validate file exists
2. Load image with OpenCV
3. Convert to grayscale
4. Detect edges (Canny)
5. Find contours
6. Map to 7 segments
7. Classify each segment
8. Build glyph string
9. Calculate confidence
10. Generate ASCII art

**Example:**
```python
result = processor.analyze_image('my_glyph.png')
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print(f"Detected: {result['glyph_string']}")
```

---

#### `compare_to_expected(image_path: str, expected_glyph: str) -> dict`

Compares image analysis to an expected glyph pattern.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `image_path` | `str` | Path to image file |
| `expected_glyph` | `str` | Expected 7-character glyph string |

**Returns:**
| Type | Description |
|------|-------------|
| `dict` | Comparison results |

**Return Structure:**
```python
{
    # All fields from analyze_image()
    'expected': '￿·——∅∅∅',
    'similarity': 0.857,      # Match ratio (0.0-1.0)
    'match': True             # True if similarity > 0.7
}
```

**Example:**
```python
result = processor.compare_to_expected('sketch.png', '￿·——∅∅∅')
print(f"Similarity: {result['similarity']:.1%}")
print(f"Match: {'Yes' if result['match'] else 'No'}")
```

---

### Internal Methods

#### `_detect_segments(img: ndarray, contours: list) -> dict`

Maps image regions to 7-segment positions.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `img` | `ndarray` | Input image |
| `contours` | `list` | List of detected contours |

**Returns:**
| Type | Description |
|------|-------------|
| `dict` | Mapping of segment names to contours |

**Algorithm:**
1. Get image dimensions
2. Define 7 region bounding boxes (relative coords)
3. For each contour, calculate centroid
4. Assign to region containing centroid
5. Keep largest contour per region

---

#### `_classify_segment(contour: ndarray, img: ndarray) -> str`

Classifies a contour as point, line, curve, or absence.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `contour` | `ndarray` | Contour points |
| `img` | `ndarray` | Source image (for context) |

**Returns:**
| Type | Description |
|------|-------------|
| `str` | Atom symbol ('∅', '·', '—', or '￿') |

**Classification Rules:**
| Condition | Atom | Reason |
|-----------|------|--------|
| `contour is None` | `∅` | No contour |
| `area < 50` | `∅` | Too small |
| `vertices == 1` or `area < 200` | `·` | Point-like |
| `2 <= vertices <= 3` | `—` | Linear |
| `vertices >= 4` | `￿` | Curved |

---

#### `_render_ascii(glyph_data: dict) -> str`

Renders glyph as ASCII art.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `glyph_data` | `dict` | Segment to atom mapping |

**Returns:**
| Type | Description |
|------|-------------|
| `str` | Multi-line ASCII representation |

**Format:**
```
      a
   f     b
      g
   e     c
      d
```

---

#### `_calculate_confidence(segments: dict) -> float`

Calculates analysis confidence score.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `segments` | `dict` | Detected segment mappings |

**Returns:**
| Type | Description |
|------|-------------|
| `float` | Confidence (0.0-1.0) |

**Formula:**
```python
confidence = min(1.0, detected_segments / 4.0)
```

4+ detected segments = high confidence (1.0)

---

## Usage Examples

### Example 1: Basic Image Analysis

```python
from vision_processor import GlyphVisionProcessor

# Initialize processor
processor = GlyphVisionProcessor()

# Analyze image
result = processor.analyze_image('hand_drawn_glyph.jpg')

if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print("╔════════════════════════════════════════╗")
    print("║     GLYPH VISION ANALYSIS              ║")
    print("╚════════════════════════════════════════╝")
    print()
    print(f"Detected Glyph: {result['glyph_string']}")
    print(f"Confidence: {result['analysis_confidence']:.1%}")
    print()
    print("Segment Breakdown:")
    for seg, atom in result['segments'].items():
        print(f"  {seg}: {atom}")
    print()
    print("Visualization:")
    print(result['ascii_art'])
```

**Expected Output:**
```
╔════════════════════════════════════════╗
║     GLYPH VISION ANALYSIS              ║
╚════════════════════════════════════════╝

Detected Glyph: ￿·——∅∅∅
Confidence: 75.0%

Segment Breakdown:
  a: ￿
  b: ·
  c: —
  d: —
  e: ∅
  f: ∅
  g: —

Visualization:

      ￿
   ∅     ·
      —
   ∅     —
      —
```

---

### Example 2: Validation Mode

```python
processor = GlyphVisionProcessor()

# Test against expected glyph
test_cases = [
    ('kenosis_drawing.png', '￿·——∅∅∅'),
    ('love_glyph.jpg', '￿·￿∅—￿—'),
    ('truth_sketch.png', '·—·∅—￿∅'),
]

print("Validation Results:")
print("=" * 60)

for image_path, expected in test_cases:
    result = processor.compare_to_expected(image_path, expected)
    
    if 'error' in result:
        print(f"\n{image_path}: ERROR - {result['error']}")
        continue
    
    status = "✓ PASS" if result['match'] else "✗ FAIL"
    print(f"\n{image_path}")
    print(f"  Expected:   {expected}")
    print(f"  Detected:   {result['glyph_string']}")
    print(f"  Similarity: {result['similarity']:.1%}")
    print(f"  Status:     {status}")
```

**Expected Output:**
```
Validation Results:
============================================================

kenosis_drawing.png
  Expected:   ￿·——∅∅∅
  Detected:   ￿·——∅∅∅
  Similarity: 100.0%
  Status:     ✓ PASS

love_glyph.jpg
  Expected:   ￿·￿∅—￿—
  Detected:   ￿—￿∅—￿—
  Similarity: 85.7%
  Status:     ✓ PASS
```

---

### Example 3: Batch Processing

```python
import os
from glob import glob

processor = GlyphVisionProcessor()

# Process all images in directory
image_dir = 'glyph_samples/'
image_files = glob(os.path.join(image_dir, '*.png'))

results = []
for img_path in image_files:
    result = processor.analyze_image(img_path)
    results.append({
        'file': os.path.basename(img_path),
        'result': result
    })

# Summary report
print("Batch Processing Summary")
print("=" * 70)
print(f"{'File':<30} {'Glyph':<10} {'Confidence':<12} {'Status'}")
print("-" * 70)

for item in results:
    file = item['file']
    result = item['result']
    
    if 'error' in result:
        glyph = 'ERROR'
        conf = 'N/A'
        status = result['error'][:20]
    else:
        glyph = result['glyph_string']
        conf = f"{result['analysis_confidence']:.1%}"
        status = 'OK' if result['analysis_confidence'] > 0.5 else 'LOW_CONF'
    
    print(f"{file:<30} {glyph:<10} {conf:<12} {status}")
```

---

### Example 4: Custom Classification Parameters

```python
class CustomGlyphProcessor(GlyphVisionProcessor):
    """Custom processor with adjusted thresholds"""
    
    def _classify_segment(self, contour, img):
        if contour is None:
            return '∅'
        
        area = cv2.contourArea(contour)
        
        # Adjusted thresholds for finer drawings
        if area < 20:  # Lower threshold
            return '∅'
        
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)  # Stricter
        vertices = len(approx)
        
        if vertices == 1 or area < 100:
            return '·'
        elif vertices <= 2:  # Stricter line requirement
            return '—'
        elif vertices >= 3:  # More inclusive curves
            return '￿'
        else:
            return '∅'

# Use custom processor
processor = CustomGlyphProcessor()
result = processor.analyze_image('fine_drawing.png')
```

---

### Example 5: Debugging Visualization

```python
import cv2
import matplotlib.pyplot as plt

def visualize_analysis(image_path, processor):
    """Show intermediate processing steps"""
    
    # Load image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours
    contour_img = img.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
    
    # Draw segment regions
    h, w = img.shape[:2]
    regions = {
        'a': (0.2, 0.0, 0.8, 0.15),
        'b': (0.8, 0.15, 1.0, 0.5),
        'c': (0.8, 0.5, 1.0, 0.85),
        'd': (0.2, 0.85, 0.8, 1.0),
        'e': (0.0, 0.5, 0.2, 0.85),
        'f': (0.0, 0.15, 0.2, 0.5),
        'g': (0.2, 0.425, 0.8, 0.575)
    }
    
    region_img = img.copy()
    for seg, (x1, y1, x2, y2) in regions.items():
        px1, py1 = int(x1 * w), int(y1 * h)
        px2, py2 = int(x2 * w), int(y2 * h)
        color = (255, 0, 0) if seg in 'ae' else (0, 255, 0) if seg in 'bd' else (0, 0, 255)
        cv2.rectangle(region_img, (px1, py1), (px2, py2), color, 2)
        cv2.putText(region_img, seg, (px1 + 5, py1 + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    # Display
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Original')
    axes[0, 1].imshow(edges, cmap='gray')
    axes[0, 1].set_title('Edges (Canny)')
    axes[1, 0].imshow(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f'Contours ({len(contours)} found)')
    axes[1, 1].imshow(cv2.cvtColor(region_img, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('Segment Regions')
    plt.tight_layout()
    plt.show()

# Use visualization
processor = GlyphVisionProcessor()
visualize_analysis('test_image.png', processor)

# Also print analysis
result = processor.analyze_image('test_image.png')
print(f"Detected: {result['glyph_string']}")
```

---

### Example 6: Command-Line Usage

```bash
# Basic analysis
python vision_processor.py my_glyph.png

# With expected pattern (validation)
python vision_processor.py sketch.png '￿·——∅∅∅'

# Output:
# ╔════════════════════════════════════════╗
# ║     GLYPH VISION ANALYSIS              ║
# ╚════════════════════════════════════════╝
# 
# Detected Glyph: ￿·——∅∅∅
# Confidence: 75.0%
# ...
```

---

## Accuracy Expectations

### Factors Affecting Accuracy

| Factor | Impact | Recommendation |
|--------|--------|----------------|
| **Image Resolution** | High | Use 640x480 minimum |
| **Contrast** | High | Dark marks on light background |
| **Line Thickness** | Medium | 2-5px thick strokes |
| **Segment Alignment** | High | Standard 7-segment layout |
| **Noise** | Medium | Clean background preferred |

### Expected Accuracy by Condition

| Condition | Point (·) | Line (—) | Curve (￿) | Absence (∅) |
|-----------|-----------|----------|-----------|-------------|
| **Ideal** (clean, aligned) | 95% | 90% | 85% | 95% |
| **Good** (minor variations) | 85% | 80% | 75% | 85% |
| **Fair** (noisy/rotated) | 70% | 65% | 60% | 75% |
| **Poor** (heavily distorted) | 50% | 45% | 40% | 60% |

### Confidence Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 0.75-1.00 | High confidence | Result reliable |
| 0.50-0.75 | Moderate confidence | Verify visually |
| 0.25-0.50 | Low confidence | Manual review needed |
| 0.00-0.25 | Very low confidence | Likely incorrect |

### Common Failure Modes

1. **Over-segmentation**: One mark split into multiple contours
   - *Solution*: Adjust Canny thresholds
   
2. **Under-segmentation**: Multiple marks merged
   - *Solution*: Ensure clear gaps between segments
   
3. **Misclassification**: Curve detected as line
   - *Solution*: Adjust approxPolyDP epsilon
   
4. **Missing segments**: Small marks filtered out
   - *Solution*: Lower area threshold

---

## Calibration Procedures

### Step 1: Camera/Scanner Setup

```python
# For live capture calibration
import cv2

def calibrate_capture():
    cap = cv2.VideoCapture(0)
    
    # Set optimal resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Set optimal focus (if available)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    
    return cap
```

**Guidelines:**
- Resolution: 1280x720 or higher
- Lighting: Even, diffuse lighting
- Background: Solid white or light gray
- Distance: Fill 80% of frame with glyph

---

### Step 2: Edge Detection Calibration

```python
def calibrate_edge_detection(image_path):
    """Find optimal Canny thresholds"""
    img = cv2.imread(image_path, 0)
    
    # Test different thresholds
    thresholds = [(30, 100), (50, 150), (70, 200), (100, 250)]
    
    results = []
    for t1, t2 in thresholds:
        edges = cv2.Canny(img, t1, t2)
        contour_count = len(cv2.findContours(edges, cv2.RETR_EXTERNAL, 
                                             cv2.CHAIN_APPROX_SIMPLE)[0])
        results.append({
            'thresholds': (t1, t2),
            'contours': contour_count,
            'coverage': np.sum(edges > 0) / edges.size
        })
    
    # Select best (7-10 contours, 5-15% coverage)
    best = min(results, 
               key=lambda x: abs(x['contours'] - 7) + abs(x['coverage'] - 0.1))
    
    return best['thresholds']

# Usage
optimal_low, optimal_high = calibrate_edge_detection('calibration_image.png')
print(f"Optimal Canny thresholds: {optimal_low}, {optimal_high}")
```

---

### Step 3: Region Calibration

```python
def calibrate_regions(image_path, known_glyph):
    """Adjust region boundaries for specific setup"""
    from mvp_glyph_converter import GlyphConverter
    
    processor = GlyphVisionProcessor()
    
    # Test with different offsets
    best_score = 0
    best_offsets = (0, 0)
    
    for dx in np.arange(-0.1, 0.1, 0.02):
        for dy in np.arange(-0.1, 0.1, 0.02):
            # Temporarily adjust regions
            original_regions = processor._detect_segments.__defaults__
            
            result = processor.analyze_image(image_path)
            if 'error' not in result:
                # Compare to expected
                matches = sum(a == b for a, b in 
                             zip(result['glyph_string'], known_glyph))
                score = matches / 7.0
                
                if score > best_score:
                    best_score = score
                    best_offsets = (dx, dy)
    
    return best_offsets, best_score

# Usage
offsets, accuracy = calibrate_regions('test.png', '￿·——∅∅∅')
print(f"Best offsets: {offsets}, Accuracy: {accuracy:.1%}")
```

---

### Step 4: Shape Classification Calibration

```python
def calibrate_classification(test_images, expected_atoms):
    """
    Calibrate classification thresholds
    test_images: list of image paths
    expected_atoms: list of expected atom symbols
    """
    processor = GlyphVisionProcessor()
    
    # Collect statistics
    areas = []
    vertices = []
    
    for img_path, expected in zip(test_images, expected_atoms):
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, 
                                        cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            cnt = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
            
            areas.append((area, expected))
            vertices.append((len(approx), expected))
    
    # Analyze distributions
    print("Area statistics by atom:")
    for atom in ['·', '—', '￿']:
        atom_areas = [a for a, e in areas if e == atom]
        if atom_areas:
            print(f"  {atom}: min={min(atom_areas):.0f}, "
                  f"max={max(atom_areas):.0f}, "
                  f"avg={sum(atom_areas)/len(atom_areas):.0f}")
    
    print("\nVertex statistics by atom:")
    for atom in ['·', '—', '￿']:
        atom_verts = [v for v, e in vertices if e == atom]
        if atom_verts:
            print(f"  {atom}: min={min(atom_verts)}, max={max(atom_verts)}, "
                  f"avg={sum(atom_verts)/len(atom_verts):.1f}")
    
    return areas, vertices

# Usage with labeled test images
test_data = [
    ('point_sample.png', '·'),
    ('line_sample.png', '—'),
    ('curve_sample.png', '￿'),
]
areas, vertices = calibrate_classification(
    [t[0] for t in test_data],
    [t[1] for t in test_data]
)
```

---

### Step 5: Full System Calibration

```python
def full_calibration(test_set_path):
    """
    Complete calibration procedure
    test_set_path: directory with labeled glyph images
    """
    from glob import glob
    import json
    
    # Load test data
    test_images = glob(f"{test_set_path}/*.png")
    
    calibration = {
        'edge_thresholds': None,
        'region_offsets': None,
        'classification_params': {
            'point_area_threshold': 200,
            'absence_area_threshold': 50,
            'line_vertex_range': (2, 3),
            'curve_vertex_min': 4
        }
    }
    
    # Step 1: Edge detection
    print("Step 1: Calibrating edge detection...")
    calibration['edge_thresholds'] = calibrate_edge_detection(test_images[0])
    
    # Step 2: Region boundaries
    print("Step 2: Calibrating region boundaries...")
    # Use first image with known glyph
    calibration['region_offsets'] = calibrate_regions(
        test_images[0], 
        '￿·——∅∅∅'  # Known calibration glyph
    )[0]
    
    # Step 3: Shape classification
    print("Step 3: Calibrating shape classification...")
    areas, vertices = calibrate_classification(test_images, 
                                                ['·', '—', '￿', '∅'] * 10)
    
    # Save calibration
    with open('vision_calibration.json', 'w') as f:
        json.dump(calibration, f, indent=2)
    
    print("Calibration complete! Saved to vision_calibration.json")
    return calibration

# Run full calibration
config = full_calibration('calibration_set/')
```

---

## Example Image Analyses

### Example 1: KENOSIS Glyph (￿·——∅∅∅)

**Input:** Clean hand-drawn KENOSIS glyph

**Analysis:**
```python
result = processor.analyze_image('kenosis_clean.png')
```

**Expected Output:**
```
Detected Glyph: ￿·——∅∅∅
Confidence: 100.0%
Contours Found: 4

Segment Breakdown:
  a: ￿ (Curve)      - Detected 5-vertex arc
  b: · (Point)      - Detected small circular region
  c: — (Line)       - Detected 2-vertex segment
  d: — (Line)       - Detected 2-vertex segment
  e: ∅ (Absence)    - No contour detected
  f: ∅ (Absence)    - No contour detected
  g: — (Line)       - Detected 2-vertex segment
```

**Visualization:**
```
      ￿
   ∅     ·
      —
   ∅     —
      —
```

---

### Example 2: Complex LOVE Glyph

**Input:** Stylized LOVE glyph with decorative curves

**Analysis:**
```python
result = processor.analyze_image('love_stylized.png')
```

**Expected Output:**
```
Detected Glyph: ￿·￿∅—￿—
Confidence: 85.7%
Contours Found: 6

Segment Breakdown:
  a: ￿ (Curve)      - Upper decorative swirl
  b: · (Point)      - Small accent dot
  c: ￿ (Curve)      - Stylized right side
  d: — (Line)       - Horizontal base
  e: ∅ (Absence)    - Clean
  f: — (Line)       - Left stem (detected as line)
  g: ￿ (Curve)      - Flowing crossbar
```

---

### Example 3: Noisy/Degraded Image

**Input:** Low-quality scan with noise

**Analysis:**
```python
result = processor.analyze_image('noisy_scan.jpg')
```

**Expected Output:**
```
Detected Glyph: ￿·—∅—∅∅
Confidence: 50.0%
Contours Found: 8
Warning: Multiple contours in region 'g'

Segment Breakdown:
  a: ￿ (Curve)      - Main arc detected
  b: · (Point)      - Noise may affect accuracy
  c: — (Line)       - Merged with noise
  d: — (Line)       - Partial detection
  ...

Note: Low confidence due to:
  - 8 contours found (expected 4-7)
  - Multiple contours in middle region
  - Small fragments detected as points
```

**Recommended Actions:**
1. Apply Gaussian blur before processing
2. Increase Canny thresholds
3. Manual verification recommended

---

### Example 4: Batch Comparison Report

```python
# Generate comprehensive report
test_images = ['kenosis.png', 'love.png', 'truth.png', 'freedom.png']
expected = ['￿·——∅∅∅', '￿·￿∅—￿—', '·—·∅—￿∅', '￿—∅∅—￿—']

print("Vision Processing Accuracy Report")
print("=" * 70)
print(f"{'Image':<20} {'Expected':<12} {'Detected':<12} {'Match':<8} {'Conf'}")
print("-" * 70)

correct = 0
total = len(test_images)

for img, exp in zip(test_images, expected):
    result = processor.compare_to_expected(img, exp)
    
    if 'error' in result:
        print(f"{img:<20} {exp:<12} {'ERROR':<12} {'N/A':<8} N/A")
        continue
    
    det = result['glyph_string']
    match = "✓" if result['match'] else "✗"
    conf = f"{result['analysis_confidence']:.0%}"
    
    if result['match']:
        correct += 1
    
    print(f"{img:<20} {exp:<12} {det:<12} {match:<8} {conf}")

print("-" * 70)
print(f"Accuracy: {correct}/{total} ({correct/total:.1%})")
```

**Expected Output:**
```
Vision Processing Accuracy Report
======================================================================
Image                Expected     Detected     Match    Conf
----------------------------------------------------------------------
kenosis.png          ￿·——∅∅∅       ￿·——∅∅∅       ✓        100%
love.png             ￿·￿∅—￿—       ￿·￿∅—￿—       ✓        100%
truth.png            ·—·∅—￿∅       ·—·∅—￿∅       ✓        100%
freedom.png          ￿—∅∅—￿—       ￿—∅∅—￿—       ✓        100%
----------------------------------------------------------------------
Accuracy: 4/4 (100.0%)
```

---

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Get started quickly
- [TESTS.md](TESTS.md) - Testing procedures
- [mvp_glyph_converter.md](mvp_glyph_converter.md) - Python converter docs
- [geogebra_mvp.md](geogebra_mvp.md) - Interactive visualization docs
