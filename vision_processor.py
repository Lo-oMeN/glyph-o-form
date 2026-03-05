#!/usr/bin/env python3
"""
L∞m≡n Vision Processor - Glyph Image Analysis

Analyzes images of glyphs and converts them to 7-segment atomic representations
using computer vision techniques from OpenCV.

This module implements the computer vision pipeline that bridges the gap between
visual glyph representations (hand-drawn or digital) and their symbolic form.
It uses edge detection, contour analysis, and shape classification to identify
atomic elements within a 7-segment display layout.

Usage:
    python3 vision_processor.py <image_path> [expected_glyph]
    
Examples:
    python3 vision_processor.py sketch.png
    python3 vision_processor.py sketch.png '￿·——∅∅∅'

Dependencies:
    - OpenCV (cv2): Image processing and computer vision
    - NumPy: Numerical operations
    - PIL: Image loading utilities

Author: THUNDERING GRACE ENGINE Project
Version: 1.0
"""

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
import cv2          # OpenCV for image processing, edge detection, contours
import numpy as np  # NumPy for array operations and numerical computing
from PIL import Image  # PIL for image loading and format handling
import sys          # System utilities for CLI argument handling
import os           # OS utilities for file path validation


# =============================================================================
# GLYPH VISION PROCESSOR CLASS
# =============================================================================

class GlyphVisionProcessor:
    """
    Convert images of glyphs to 7-segment atom representation.
    
    This class implements a complete computer vision pipeline for analyzing
    images containing glyph drawings. It detects the 7-segment layout in the
    image, identifies which segments contain marks, and classifies each mark
    as Point (·), Line (—), Curve (￿), or Absence (∅).
    
    The processing pipeline:
        1. Load and validate image
        2. Convert to grayscale
        3. Detect edges using Canny algorithm
        4. Find contours
        5. Map contours to 7-segment regions
        6. Classify each segment's shape
        7. Build glyph representation
    
    Attributes:
        ATOMS (List[str]): Atomic symbols in order of classification
            ['∅', '·', '—', '￿'] = [Absence, Point, Line, Curve]
        SEGMENTS (List[str]): Segment names ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        debug (bool): Enable debug output (default: True)
    
    Example:
        >>> processor = GlyphVisionProcessor()
        >>> result = processor.analyze_image('my_glyph.png')
        >>> print(result['glyph_string'])
        '￿·——∅∅∅'
    """
    
    # Class constants: atomic symbols in classification order
    # Order matters for index-based classification
    ATOMS = ['∅', '·', '—', '￿']  # 0=absence, 1=point, 2=line, 3=curve
    
    # 7-segment display segment names (standard digital display nomenclature)
    SEGMENTS = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    
    def __init__(self):
        """
        Initialize the GlyphVisionProcessor.
        
        Sets default attributes:
            - debug: True (enables diagnostic output)
        
        No parameters required.
        """
        self.debug = True  # Enable debug output for troubleshooting
    
    # -------------------------------------------------------------------------
    # MAIN ANALYSIS METHODS
    # -------------------------------------------------------------------------
    
    def analyze_image(self, image_path):
        """
        Main entry point: analyze an image and return glyph data.
        
        This is the primary API method for vision processing. It runs the
        complete pipeline from image loading through glyph construction.
        
        Processing Pipeline:
            1. Validate file exists
            2. Load image with OpenCV
            3. Convert to grayscale
            4. Detect edges (Canny algorithm)
            5. Find contours
            6. Map contours to 7-segment regions
            7. Classify each segment's shape
            8. Build glyph string
            9. Calculate confidence score
            10. Generate ASCII visualization
        
        Args:
            image_path (str): Path to the image file (PNG, JPG, etc.)
            
        Returns:
            dict: Analysis results containing:
                - 'glyph_string' (str): Detected 7-character glyph
                - 'segments' (dict): Per-segment atom assignments
                - 'contours_found' (int): Number of contours detected
                - 'image_shape' (tuple): (height, width, channels)
                - 'ascii_art' (str): ASCII visualization
                - 'analysis_confidence' (float): Confidence score 0.0-1.0
                
            If error occurs:
                - 'error' (str): Error message
        
        Example:
            >>> processor = GlyphVisionProcessor()
            >>> result = processor.analyze_image('glyph.png')
            >>> if 'error' not in result:
            ...     print(f"Detected: {result['glyph_string']}")
            ...     print(f"Confidence: {result['analysis_confidence']:.1%}")
        """
        # Step 1: Validate file exists
        if not os.path.exists(image_path):
            return {'error': f'Image not found: {image_path}'}
        
        # Step 2: Load image with OpenCV
        # OpenCV loads images in BGR format by default
        img = cv2.imread(image_path)
        if img is None:
            return {'error': 'Could not load image'}
        
        # Step 3: Preprocess - convert to grayscale
        # Grayscale simplifies edge detection and reduces noise
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Step 4: Edge detection using Canny algorithm
        # Canny parameters: threshold1=50 (lower), threshold2=150 (upper)
        # These values detect edges while filtering out noise
        edges = cv2.Canny(gray, 50, 150)
        
        # Step 5: Find contours in the edge map
        # RETR_EXTERNAL: get only outer contours (ignores holes)
        # CHAIN_APPROX_SIMPLE: compress horizontal/vertical segments
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Step 6: Map contours to 7-segment regions
        segments = self._detect_segments(img, contours)
        
        # Step 7: Classify each detected segment
        glyph_data = {}  # Build segment -> atom mapping
        for seg_name, contour in segments.items():
            atom = self._classify_segment(contour, img)
            glyph_data[seg_name] = atom
        
        # Step 8: Build glyph string in segment order (a-g)
        glyph_string = ''.join([glyph_data.get(s, '∅') for s in self.SEGMENTS])
        
        # Step 9: Return complete analysis
        return {
            'glyph_string': glyph_string,              # The detected glyph
            'segments': glyph_data,                    # Per-segment details
            'contours_found': len(contours),           # Raw detection count
            'image_shape': img.shape,                  # Original dimensions
            'ascii_art': self._render_ascii(glyph_data),  # Visualization
            'analysis_confidence': self._calculate_confidence(segments)  # Reliability
        }
    
    def compare_to_expected(self, image_path, expected_glyph):
        """
        Compare image analysis to expected glyph string.
        
        This method extends analyze_image() by comparing the detected glyph
        against an expected pattern and calculating similarity.
        
        Args:
            image_path (str): Path to the image file
            expected_glyph (str): Expected 7-character glyph string
            
        Returns:
            dict: All fields from analyze_image() plus:
                - 'expected' (str): The expected glyph string
                - 'similarity' (float): Match ratio (0.0-1.0)
                - 'match' (bool): True if similarity > 0.7
                
        Example:
            >>> processor = GlyphVisionProcessor()
            >>> result = processor.compare_to_expected('sketch.png', '￿·——∅∅∅')
            >>> print(f"Similarity: {result['similarity']:.1%}")
            >>> print(f"Match: {'Yes' if result['match'] else 'No'}")
        """
        # Get base analysis
        result = self.analyze_image(image_path)
        
        # Return error if analysis failed
        if 'error' in result:
            return result
        
        # Get detected glyph
        detected = result['glyph_string']
        
        # Calculate similarity: ratio of matching segments
        matches = sum(1 for d, e in zip(detected, expected_glyph) if d == e)
        similarity = matches / 7.0
        
        # Return extended result
        return {
            **result,                    # Include all base analysis fields
            'expected': expected_glyph,  # The expected pattern
            'similarity': similarity,    # Match ratio
            'match': similarity > 0.7    # Pass/fail threshold
        }
    
    # -------------------------------------------------------------------------
    # INTERNAL PROCESSING METHODS
    # -------------------------------------------------------------------------
    
    def _detect_segments(self, img, contours):
        """
        Map image regions to 7-segment positions.
        
        Divides the image into 7 regions corresponding to the 7-segment
        display layout. Each contour is assigned to a region based on its
        centroid location.
        
        Region Layout (relative coordinates 0.0-1.0):
        
            ┌─────────────────────────────┐
            │         Region A            │  y: 0.0 to 0.15
            │    (0.2,0.0)  (0.8,0.15)    │
            ├────────┬──────────┬─────────┤
            │        │          │         │
            │Region F│          │Region B │  y: 0.15 to 0.5
            │(0,0.15)│          │(0.8,0.5)│
            │        │ Region G │         │  y: 0.425 to 0.575
            │        │(0.2,0.425)        │
            │        │ (0.8,0.575)       │
            │Region E│          │Region C │  y: 0.5 to 0.85
            │(0,0.5) │          │(0.8,0.85)│
            │        │          │         │
            ├────────┴──────────┴─────────┤
            │         Region D            │  y: 0.85 to 1.0
            │   (0.2,0.85)  (0.8,1.0)     │
            └─────────────────────────────┘
            x: 0.0-0.2   0.2-0.8   0.8-1.0
        
        Args:
            img (ndarray): Input image (used for dimensions)
            contours (list): List of contours from cv2.findContours
            
        Returns:
            dict: Mapping of segment names ('a'-'g') to their largest contour
        """
        # Get image dimensions
        h, w = img.shape[:2]
        
        # Define segment regions as relative coordinates (x1, y1, x2, y2)
        # These map to the standard 7-segment display topology
        regions = {
            'a': (0.2, 0.0, 0.8, 0.15),    # Top horizontal
            'b': (0.8, 0.15, 1.0, 0.5),    # Upper right vertical
            'c': (0.8, 0.5, 1.0, 0.85),    # Lower right vertical
            'd': (0.2, 0.85, 0.8, 1.0),    # Bottom horizontal
            'e': (0.0, 0.5, 0.2, 0.85),    # Lower left vertical
            'f': (0.0, 0.15, 0.2, 0.5),    # Upper left vertical
            'g': (0.2, 0.425, 0.8, 0.575)  # Middle horizontal
        }
        
        segment_contours = {}  # Build segment -> contour mapping
        
        # For each segment region
        for seg_name, (x1, y1, x2, y2) in regions.items():
            # Convert relative coordinates to pixel coordinates
            px1, py1 = int(x1 * w), int(y1 * h)
            px2, py2 = int(x2 * w), int(y2 * h)
            
            # Find contours whose centroid falls within this region
            region_contours = []
            for cnt in contours:
                # Calculate centroid using moments
                M = cv2.moments(cnt)
                if M["m00"] != 0:  # Avoid division by zero
                    cx = int(M["m10"] / M["m00"])  # X centroid
                    cy = int(M["m01"] / M["m00"])  # Y centroid
                    
                    # Check if centroid is within region bounds
                    if px1 <= cx <= px2 and py1 <= cy <= py2:
                        region_contours.append(cnt)
            
            # If contours found in this region, keep the largest one
            if region_contours:
                segment_contours[seg_name] = max(region_contours, key=cv2.contourArea)
        
        return segment_contours
    
    def _classify_segment(self, contour, img):
        """
        Classify a contour as point, line, curve, or absence.
        
        Uses geometric analysis of the contour to determine its atomic type:
        - ABSENCE (∅): No contour or too small to be significant
        - POINT (·): Small area or single vertex
        - LINE (—): 2-3 vertices (straight-ish)
        - CURVE (￿): 4+ vertices (curved/complex)
        
        Classification Algorithm:
            1. If contour is None → ABSENCE
            2. Calculate contour area
            3. If area < 50 pixels → ABSENCE (too small)
            4. Approximate polygon from contour
            5. Count vertices
            6. If vertices == 1 or area < 200 → POINT
            7. If vertices 2-3 → LINE
            8. If vertices >= 4 → CURVE
        
        Args:
            contour (ndarray): Contour points from cv2.findContours
            img (ndarray): Source image (for context, currently unused)
            
        Returns:
            str: Atom symbol ('∅', '·', '—', or '￿')
        """
        # No contour = absence
        if contour is None:
            return '∅'
        
        # Calculate contour area
        area = cv2.contourArea(contour)
        
        # Too small to be significant = absence
        if area < 50:
            return '∅'
        
        # Approximate the contour shape with a polygon
        # arcLength calculates perimeter, approxPolyDP simplifies the contour
        peri = cv2.arcLength(contour, True)  # True = closed contour
        # epsilon = 0.04 * peri controls approximation accuracy
        # Smaller epsilon = more vertices = more detailed approximation
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        
        # Count vertices of approximated polygon
        vertices = len(approx)
        
        # Classify based on vertex count and area
        if vertices == 1 or area < 200:
            # Single vertex or small area = point
            return '·'
        elif vertices == 2 or vertices == 3:
            # 2-3 vertices = line (or simple angle)
            return '—'
        elif vertices >= 4:
            # 4+ vertices = curve (complex shape)
            return '￿'
        else:
            # Fallback (should not reach here)
            return '∅'
    
    def _render_ascii(self, glyph_data):
        """
        Render glyph as ASCII art.
        
        Creates a text-based visualization of the 7-segment glyph showing
        the atomic assignments for each segment.
        
        Layout:
                a
             f     b
                g
             e     c
                d
        
        Args:
            glyph_data (dict): Segment name -> atom symbol mapping
            
        Returns:
            str: Multi-line ASCII representation
        """
        # Extract atoms for each segment (default to absence if not present)
        a = glyph_data.get('a', '∅')
        b = glyph_data.get('b', '∅')
        c = glyph_data.get('c', '∅')
        d = glyph_data.get('d', '∅')
        e = glyph_data.get('e', '∅')
        f = glyph_data.get('f', '∅')
        g = glyph_data.get('g', '∅')
        
        # Build ASCII representation
        return f"""
      {a}
   {f}     {b}
      {g}
   {e}     {c}
      {d}
        """
    
    def _calculate_confidence(self, segments):
        """
        Calculate analysis confidence score.
        
        Confidence is based on how many segments were detected:
        - More detected segments = higher confidence
        - 4+ segments = maximum confidence (1.0)
        
        Formula: confidence = min(1.0, detected_segments / 4.0)
        
        Args:
            segments (dict): Detected segment mappings
            
        Returns:
            float: Confidence score from 0.0 to 1.0
        """
        detected = len(segments)  # Count detected segments
        # Normalize: 4 segments = 1.0, fewer = proportional
        return min(1.0, detected / 4.0)


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    """
    Main entry point for command-line usage.
    
    Usage:
        python3 vision_processor.py <image_path> [expected_glyph]
    
    If expected_glyph is provided, performs validation comparison.
    Otherwise, just analyzes and displays results.
    """
    # Check command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 vision_processor.py <image_path> [expected_glyph]")
        print("Example: python3 vision_processor.py sketch.png ￿￿￿——∅∅")
        sys.exit(1)
    
    # Parse arguments
    image_path = sys.argv[1]                     # First arg: image path
    expected = sys.argv[2] if len(sys.argv) > 2 else None  # Optional: expected glyph
    
    # Initialize processor
    processor = GlyphVisionProcessor()
    
    # Run analysis (with or without expected value)
    if expected:
        result = processor.compare_to_expected(image_path, expected)
    else:
        result = processor.analyze_image(image_path)
    
    # Print formatted results
    print("╔════════════════════════════════════════╗")
    print("║     GLYPH VISION ANALYSIS              ║")
    print("╚════════════════════════════════════════╝")
    print()
    
    # Handle errors
    if 'error' in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    
    # Print main results
    print(f"Detected Glyph: {result['glyph_string']}")
    print(f"Confidence: {result['analysis_confidence']:.1%}")
    print()
    
    # Print segment breakdown
    print("Segment Breakdown:")
    for seg, atom in result['segments'].items():
        print(f"  {seg}: {atom}")
    print()
    
    # Print ASCII visualization
    print("Visualization:")
    print(result['ascii_art'])
    
    # Print comparison results if expected was provided
    if 'expected' in result:
        print(f"Expected: {result['expected']}")
        print(f"Similarity: {result['similarity']:.1%}")
        print(f"Match: {'✓ YES' if result['match'] else '✗ NO'}")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    main()
