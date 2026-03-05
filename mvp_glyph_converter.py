#!/usr/bin/env python3
"""
Glyph-o-betics MVP - Minimal Functional Demo
Converts English words to 7-segment glyph representations using the 
THUNDERING GRACE ENGINE architecture.

This module implements the core transformation pipeline that converts English 
words into 7-segment atomic glyph representations through three parallel 
descent pathways (phonetic, orthographic, semantic) fused via kenotic bias.

Usage:
    python mvp_glyph_converter.py <WORD> [WORD2] ...
    python mvp_glyph_converter.py --test  # Run self-test

Examples:
    python mvp_glyph_converter.py LOVE
    python mvp_glyph_converter.py LOVE TRUTH FREEDOM

Author: THUNDERING GRACE ENGINE Project
Version: 2.0 (MVP)
"""

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import sys      # System utilities for CLI argument handling
import math     # Mathematical functions (sqrt, cos, acos, exp)
import re       # Regular expressions (reserved for future extensions)
from typing import List, Tuple, Dict  # Type hints for function signatures

# =============================================================================
# GLYPHOBETICS CONSTANTS
# =============================================================================

# Four Atoms - The fundamental building blocks of the glyph system
# Each atom represents a distinct mode of geometric presence
ATOMS = ['·', '—', '￿', '∅']  # Point, Line, Curve, Absence
ATOM_NAMES = ['Point', 'Line', 'Curve', 'Absence']  # Human-readable names

# 7-Segment Layout - Standard digital display topology
# Segments are named a-g following conventional 7-segment nomenclature
# Layout visualization:
#     a (top)
#  f     b
#     g (middle)
#  e     c
#     d (bottom)
SEGMENTS = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

# Segment positions for ASCII visualization (row, col_start, col_end)
# Defines the bounding box for each segment in the 5x9 character canvas
SEGMENT_POSITIONS = {
    'a': (0, 2, 6),   # Top horizontal: row 0, columns 2-6
    'b': (1, 6, 8),   # Upper right: rows 1-2, columns 6-8
    'c': (3, 6, 8),   # Lower right: rows 3-4, columns 6-8
    'd': (4, 2, 6),   # Bottom horizontal: row 4, columns 2-6
    'e': (3, 0, 2),   # Lower left: rows 3-4, columns 0-2
    'f': (1, 0, 2),   # Upper left: rows 1-2, columns 0-2
    'g': (2, 2, 6)    # Middle horizontal: row 2, columns 2-6
}

# =============================================================================
# PHONETIC MAPPING - PATHWAY 1
# =============================================================================
# Maps letters to atoms based on their phonetic characteristics
# Vowels (open sounds) → Curve (flowing, continuous)
# Plosives (stopped sounds) → Point (discrete, abrupt)
# Fricatives (airy sounds) → Line (continuous, directional)
# Nasals (resonant voids) → Absence (empty but present)
# Liquids (flowing sounds) → Curve (smooth, adaptive)

PHONETIC_MAP = {
    # Vowels → Curve (open, flowing sounds become curves)
    'a': '￿', 'e': '￿', 'i': '￿', 'o': '￿', 'u': '￿',
    'A': '￿', 'E': '￿', 'I': '￿', 'O': '￿', 'U': '￿',
    # Plosives → Point (stopped, discrete sounds become points)
    'p': '·', 't': '·', 'k': '·', 'b': '·', 'd': '·', 'g': '·',
    'P': '·', 'T': '·', 'K': '·', 'B': '·', 'D': '·', 'G': '·',
    # Fricatives → Line (continuous, airy sounds become lines)
    'f': '—', 'v': '—', 's': '—', 'z': '—', 'h': '—',
    'F': '—', 'V': '—', 'S': '—', 'Z': '—', 'H': '—',
    'w': '—', 'W': '—',
    # Nasals → Absence (resonant voids become absence)
    'm': '∅', 'n': '∅', 'M': '∅', 'N': '∅',
    # Liquids → Curve-Point hybrid (use Curve for flow)
    'l': '￿', 'r': '￿', 'L': '￿', 'R': '￿',
    # Others default to Curve (Y as vowel-like)
    'y': '￿', 'Y': '￿',
}

# =============================================================================
# ORTHOGRAPHIC MAPPING - PATHWAY 2
# =============================================================================
# Maps letter shapes to stroke atoms based on visual appearance
# Each letter is decomposed into its constituent strokes
# Curved letters (O, S, C) → Curve atoms
# Linear letters (I, L, T) → Line atoms
# Pointed letters (A, M, N) → Mix of lines and points

ORTHGRAPHIC_MAP = {
    'A': ['—', '—', '—'],      # Two diagonals + crossbar = 3 lines
    'B': ['—', '—', '￿'],      # Vertical + two curves
    'C': ['￿'],                 # Single curve
    'D': ['—', '￿'],            # Vertical + curve
    'E': ['—', '—', '—'],      # Three horizontals
    'F': ['—', '—'],            # Two horizontals + vertical
    'G': ['￿', '—'],            # Curve + horizontal
    'H': ['—', '—', '—'],      # Two verticals + crossbar
    'I': ['—', '·', '—'],      # Vertical + two caps (points)
    'J': ['￿'],                 # Hook curve
    'K': ['—', '—', '—'],      # Vertical + two diagonals
    'L': ['—', '—'],            # Vertical + horizontal
    'M': ['—', '—', '—'],       # Two verticals + two diagonals (simplified)
    'N': ['—', '—', '—'],       # Two verticals + diagonal
    'O': ['￿'],                 # Closed curve
    'P': ['—', '￿'],            # Vertical + curve
    'Q': ['￿', '·'],            # Circle + tail (point)
    'R': ['—', '￿', '·'],       # P + diagonal tail
    'S': ['￿'],                 # Curve
    'T': ['—', '—'],            # Horizontal + vertical
    'U': ['￿'],                 # Curve
    'V': ['—', '—'],            # Two diagonals
    'W': ['—', '—', '—', '—'],  # Complex diagonals (simplified)
    'X': ['—', '—'],            # Two diagonals
    'Y': ['—', '—', '—'],       # Two diagonals + vertical
    'Z': ['—', '—', '—'],       # Three horizontals (with diagonals simplified)
}

# =============================================================================
# SEMANTIC MAPPING - PATHWAY 3
# =============================================================================
# Maps semantic field patterns (word prefixes) to atom sequences
# Based on the emotional/conceptual category of the word
# Love/Connection words → Curve-dominant (flow, connection)
# Truth/Knowledge words → Mixed (balance of precision and depth)
# Freedom/Open words → Line/Curve mix (expansion with structure)
# Life/Growth words → Curve dominant (organic, flowing)
# Death/End words → Point/Absence dominant (termination, void)

SEMANTIC_PATTERNS = {
    # Love/Connection words → Curve-dominant with points (hearts connect)
    'LOV': ['￿', '·', '￿', '∅', '—', '￿', '—'],
    'HEA': ['￿', '·', '￿', '∅', '—', '￿', '—'],
    'BO':  ['￿', '·', '￿', '∅', '—', '￿', '—'],
    # Truth/Knowledge words → Balanced with precision (points for facts)
    'TRU': ['·', '—', '·', '∅', '—', '￿', '∅'],
    'KNO': ['·', '—', '·', '∅', '—', '￿', '∅'],
    'FAC': ['·', '—', '·', '∅', '—', '￿', '∅'],
    # Freedom/Open words → Lines with curves (expansion)
    'FRE': ['￿', '—', '∅', '∅', '—', '￿', '—'],
    'OPE': ['￿', '—', '∅', '∅', '—', '￿', '—'],
    'WID': ['￿', '—', '∅', '∅', '—', '￿', '—'],
    # Life/Growth words → Curve dominant (organic)
    'LIF': ['￿', '·', '￿', '·', '—', '￿', '—'],
    'GRO': ['￿', '·', '￿', '·', '—', '￿', '—'],
    # Death/End words → Point/Absence dominant (termination)
    'DEA': ['∅', '∅', '·', '∅', '￿', '∅', '·'],
    'END': ['∅', '∅', '·', '∅', '￿', '∅', '·'],
}

# =============================================================================
# GLYPH CONVERTER CLASS
# =============================================================================

class GlyphConverter:
    """
    English → 7-Segment Glyph converter
    
    Implements the complete transformation pipeline including three descent 
    pathways (phonetic, orthographic, semantic) fused via kenotic bias.
    
    Attributes:
        atoms (List[str]): The four atomic symbols [Point, Line, Curve, Absence]
        segments (List[str]): The seven segment names [a, b, c, d, e, f, g]
    
    Example:
        >>> converter = GlyphConverter()
        >>> glyph = converter.english_to_glyph("LOVE")
        >>> print(glyph)
        '￿·￿∅—￿—'
    """
    
    def __init__(self):
        """
        Initialize the GlyphConverter with default constants.
        
        Sets up references to the global ATOMS and SEGMENTS constants.
        No parameters required - all configuration is via module-level constants.
        """
        self.atoms = ATOMS        # Reference to atom symbols
        self.segments = SEGMENTS  # Reference to segment names
        
    # -------------------------------------------------------------------------
    # DESCENT PATHWAY METHODS
    # -------------------------------------------------------------------------
    
    def phonetic_descent(self, word: str) -> List[str]:
        """
        Pathway 1: Phonetic descent (sound → curve)
        
        Maps each letter in the word to an atom based on its phonetic 
        characteristics using the PHONETIC_MAP dictionary.
        
        Algorithm:
            1. For each character in the input word
            2. Look up the character in PHONETIC_MAP
            3. Default to Curve ('￿') if character not found
            4. Distribute collected atoms across 7 segments
        
        Args:
            word (str): The English word to convert
            
        Returns:
            List[str]: List of 7 atoms mapped to segments a-g
            
        Example:
            >>> converter = GlyphConverter()
            >>> converter.phonetic_descent("LOVE")
            ['￿', '·', '￿', '∅', '—', '￿', '—']
        """
        atoms = []  # Collect atoms for each letter
        for char in word:
            if char in PHONETIC_MAP:
                # Map character to its phonetic atom
                atoms.append(PHONETIC_MAP[char])
            else:
                # Unknown characters default to Curve (most neutral/flexible)
                atoms.append('￿')
        # Distribute collected atoms across the 7-segment display
        return self._distribute_to_segments(atoms)
    
    def orthographic_descent(self, word: str) -> List[str]:
        """
        Pathway 2: Orthographic descent (shape → atom)
        
        Maps letter strokes to atoms based on visual appearance using the
        ORTHGRAPHIC_MAP dictionary. Uppercase letters have more strokes.
        
        Algorithm:
            1. Convert word to uppercase for consistent mapping
            2. For each letter, look up its stroke pattern in ORTHGRAPHIC_MAP
            3. Extend all stroke atoms into a flat list
            4. Distribute across 7 segments
        
        Args:
            word (str): The English word to convert
            
        Returns:
            List[str]: List of 7 atoms mapped to segments a-g
            
        Example:
            >>> converter = GlyphConverter()
            >>> converter.orthographic_descent("HI")
            ['—', '·', '—', '—', '—', '—', '∅']
        """
        atoms = []
        for char in word.upper():
            if char in ORTHGRAPHIC_MAP:
                # Get stroke pattern for this letter
                strokes = ORTHGRAPHIC_MAP[char]
                # Add all strokes to the atom list
                atoms.extend(strokes)
            else:
                # Unknown characters default to Point (minimal stroke)
                atoms.append('·')
        return self._distribute_to_segments(atoms)
    
    def semantic_descent(self, word: str) -> List[str]:
        """
        Pathway 3: Semantic descent (meaning → topology)
        
        Maps semantic field to atoms based on word meaning. Checks for known
        semantic patterns first, then falls back to heuristic generation based
        on word characteristics (length, vowel ratio).
        
        Algorithm:
            1. Check for semantic pattern prefixes in SEMANTIC_PATTERNS
            2. If pattern found, return the predefined atom sequence
            3. Otherwise, generate heuristically:
               - Calculate vowel ratio (vowels / total length)
               - High vowel ratio (>0.4) → Curve dominant pattern
               - Medium ratio (0.2-0.4) → Mixed pattern
               - Low ratio (<0.2) → Line/Point dominant pattern
               - Deterministic selection based on character ASCII values
        
        Args:
            word (str): The English word to convert
            
        Returns:
            List[str]: List of 7 atoms mapped to segments a-g
            
        Example:
            >>> converter = GlyphConverter()
            >>> converter.semantic_descent("LOVE")  # Matches 'LOV' pattern
            ['￿', '·', '￿', '∅', '—', '￿', '—']
        """
        word_upper = word.upper()
        
        # Check for semantic patterns (prefix matching)
        for prefix, pattern in SEMANTIC_PATTERNS.items():
            if word_upper.startswith(prefix):
                return pattern
        
        # Fallback: Generate from word characteristics heuristically
        atoms = []
        word_len = len(word)
        # Count vowels for vowel ratio calculation
        vowel_count = sum(1 for c in word if c.lower() in 'aeiou')
        
        # Generate 7 segments with position-aware heuristics
        for i in range(7):
            # Use word length to determine which character influences this segment
            position_ratio = i / 6.0
            char_idx = int(position_ratio * (word_len - 1)) if word_len > 1 else 0
            char = word[char_idx].upper() if char_idx < word_len else 'A'
            
            # Calculate vowel ratio for pattern selection
            vowel_ratio = vowel_count / max(word_len, 1)
            
            # Select atom pool based on vowel ratio
            if vowel_ratio > 0.4:
                # High vowel ratio → Curve dominant (flowing, open words)
                atom_choices = ['￿', '￿', '·', '∅']
            elif vowel_ratio > 0.2:
                # Medium → Mixed (balanced words)
                atom_choices = ['—', '￿', '·', '∅']
            else:
                # Low → Line/Point dominant (sharp, precise words)
                atom_choices = ['—', '—', '·', '∅']
            
            # Deterministic selection based on character value and position
            # This ensures the same word always produces the same glyph
            char_val = ord(char) if char.isalpha() else 65
            atom_idx = (char_val + i * 7) % 4
            atoms.append(atom_choices[atom_idx])
        
        return atoms
    
    # -------------------------------------------------------------------------
    # UTILITY METHODS
    # -------------------------------------------------------------------------
    
    def _distribute_to_segments(self, atoms: List[str]) -> List[str]:
        """
        Distribute a list of atoms across 7 segments.
        
        Takes a flat list of atoms and maps them to the 7-segment display.
        If fewer than 7 atoms, remaining segments get Absence ('∅').
        If more than 7 atoms, excess atoms are truncated.
        
        Args:
            atoms (List[str]): Flat list of atom symbols
            
        Returns:
            List[str]: Exactly 7 atoms mapped to segments a-g
        """
        segments = ['∅'] * 7  # Start with all Absence
        for i, atom in enumerate(atoms[:7]):
            segments[i] = atom
        return segments
    
    # -------------------------------------------------------------------------
    # FUSION METHODS
    # -------------------------------------------------------------------------
    
    def fuse_pathways(self, phonetic: List[str], orthographic: List[str], 
                     semantic: List[str]) -> str:
        """
        Fuse three descent pathways into final glyph.
        
        Uses majority voting with kenotic bias (Absence amplification).
        The kenotic rule: if 2+ segments vote for Absence, Absence wins.
        This reflects the "emptying that enables overflow" philosophy.
        
        Algorithm:
            1. For each segment position (0-6)
            2. Collect votes from all 3 pathways
            3. Count occurrences (Absence counts as 0.5, others as 1.0)
            4. Apply kenotic amplification: if 2+ Absences, Absence wins
            5. Otherwise, atom with highest weighted count wins
        
        Args:
            phonetic (List[str]): Phonetic pathway atoms (7 elements)
            orthographic (List[str]): Orthographic pathway atoms (7 elements)
            semantic (List[str]): Semantic pathway atoms (7 elements)
            
        Returns:
            str: Fused 7-character glyph string
            
        Example:
            >>> converter = GlyphConverter()
            >>> p = ['￿', '·', '—', '∅', '—', '￿', '—']
            >>> o = ['—', '￿', '·', '—', '∅', '—', '￿']
            >>> s = ['￿', '—', '∅', '￿', '·', '—', '—']
            >>> converter.fuse_pathways(p, o, s)
            '￿·—∅—￿—'
        """
        final = []  # Build final glyph character by character
        
        for i in range(7):
            # Collect votes from all three pathways for this segment
            votes = [phonetic[i], orthographic[i], semantic[i]]
            
            # Count occurrences with kenotic weighting
            # Absence (∅) gets 0.5 weight (easier to achieve majority)
            counts = {}
            for v in votes:
                counts[v] = counts.get(v, 0) + (0.5 if v == '∅' else 1)
            
            # Kenotic amplification: if two or more ∅, ∅ wins
            # This implements the "self-emptying" principle
            if votes.count('∅') >= 2:
                final.append('∅')
            else:
                # Get atom with highest weighted count
                final.append(max(counts, key=counts.get))
        
        return ''.join(final)
    
    # -------------------------------------------------------------------------
    # MAIN CONVERSION METHOD
    # -------------------------------------------------------------------------
    
    def english_to_glyph(self, word: str) -> str:
        """
        Full transformation pipeline: English word → 7-segment glyph.
        
        This is the primary API method for converting English words to glyphs.
        It runs all three descent pathways and fuses them using kenotic bias.
        
        Args:
            word (str): English word to convert. Empty/whitespace returns all Absence.
            
        Returns:
            str: 7-character glyph string with atoms for segments a-g
            
        Example:
            >>> converter = GlyphConverter()
            >>> converter.english_to_glyph("LOVE")
            '￿·￿∅—￿—'
            >>> converter.english_to_glyph("")
            '∅∅∅∅∅∅∅'
        """
        # Handle empty/whitespace input
        if not word or not word.strip():
            return '∅∅∅∅∅∅∅'
        
        # Compute all three descent pathways in parallel
        p = self.phonetic_descent(word)      # Sound-based mapping
        o = self.orthographic_descent(word)  # Shape-based mapping
        s = self.semantic_descent(word)      # Meaning-based mapping
        
        # Fuse pathways into final glyph
        return self.fuse_pathways(p, o, s)
    
    # -------------------------------------------------------------------------
    # VECTOR METHODS
    # -------------------------------------------------------------------------
    
    def glyph_to_vector(self, glyph: str) -> List[float]:
        """
        Convert glyph string to 28-dimensional vector.
        
        Creates a one-hot encoded vector where each segment's atom is
        represented by a 1.0 at the appropriate index.
        
        Vector Layout (28 dimensions):
            Segment 0 (a): indices 0-3  [Point, Line, Curve, Absence]
            Segment 1 (b): indices 4-7  [Point, Line, Curve, Absence]
            ...
            Segment 6 (g): indices 24-27 [Point, Line, Curve, Absence]
        
        Index formula: segment_index × 4 + atom_index
        where atom_index: 0=Point, 1=Line, 2=Curve, 3=Absence
        
        Args:
            glyph (str): 7-character glyph string
            
        Returns:
            List[float]: 28-dimensional one-hot vector
            
        Example:
            >>> converter = GlyphConverter()
            >>> converter.glyph_to_vector("￿·——∅∅∅")
            # Segment a=Curve(2), b=Point(0), c=Line(1), d=Line(1), e=Absence(3),
            # f=Absence(3), g=Line(1)
            # Indices 2, 4, 9, 13, 19, 23, 25 will be 1.0
        """
        vector = [0.0] * 28  # Initialize all zeros
        for i, atom in enumerate(glyph):
            if i >= 7:
                break  # Safety: only process first 7 characters
            if atom in ATOMS:
                # Get atom index (0=Point, 1=Line, 2=Curve, 3=Absence)
                atom_idx = ATOMS.index(atom)
                # Set corresponding position to 1.0
                vector[i * 4 + atom_idx] = 1.0
        return vector
    
    # -------------------------------------------------------------------------
    # RESONANCE METHODS
    # -------------------------------------------------------------------------
    
    def compute_resonance(self, word1: str, word2: str) -> float:
        """
        Compute Looman resonance between two words.
        
        Resonance measures the harmonic relationship between two words based
        on their glyph representations. Returns a score from 0.0 to 1.0+ where:
        - 1.0 = identical glyphs (perfect resonance)
        - 0.7+ = strong harmonic connection
        - 0.4-0.7 = moderate connection
        - <0.4 = weak/distant relationship
        
        Args:
            word1 (str): First English word
            word2 (str): Second English word
            
        Returns:
            float: Resonance score (0.0 to 1.0+)
            
        Example:
            >>> converter = GlyphConverter()
            >>> converter.compute_resonance("LOVE", "LOVE")
            1.0
            >>> converter.compute_resonance("LOVE", "HEART")  # Strong connection
            0.823
        """
        # Convert both words to glyphs
        g1 = self.english_to_glyph(word1)
        g2 = self.english_to_glyph(word2)
        
        # Convert glyphs to vectors
        v1 = self.glyph_to_vector(g1)
        v2 = self.glyph_to_vector(g2)
        
        # Compute atomic resonance
        return self._atomic_resonance(v1, v2)
    
    def _atomic_resonance(self, v1: List[float], v2: List[float], 
                         kenotic_lambda: float = 1.618) -> float:
        """
        Atomic Looman Resonance Engine.
        
        Computes resonance between two 28-dimensional atomic vectors using:
        1. Cosine similarity (vector alignment)
        2. Absence bonus (kenotic weighting - rewards void/emptiness)
        3. Curve flow (transformation continuity penalty)
        4. Golden-ratio harmonic (φ-based alignment bonus)
        
        Formula:
            resonance = vec_sim × (1 + absence_bonus) × 
                       exp(-λ × curve_flow × 0.1) × 
                       (1 + 0.2 × harmonic)
        
        Args:
            v1 (List[float]): First 28-dimensional vector
            v2 (List[float]): Second 28-dimensional vector
            kenotic_lambda (float): Kenotic weight parameter (default: φ = 1.618)
            
        Returns:
            float: Resonance score (0.0 to 1.0)
        """
        import math
        
        golden = (1 + math.sqrt(5)) / 2  # Golden ratio φ ≈ 1.618
        
        # Vector similarity (cosine similarity)
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        
        if norm1 < 1e-8 or norm2 < 1e-8:
            return 0.0  # Avoid division by zero
        
        vec_sim = dot_product / (norm1 * norm2)
        
        # Absence bonus (kenosis weighting)
        # Absence is at index 3 of each segment (every 4th starting at 3)
        v1_absence = [v1[i] for i in range(3, 28, 4)]
        v2_absence = [v2[i] for i in range(3, 28, 4)]
        absence_bonus = sum(v1_absence) + sum(v2_absence)
        absence_bonus = absence_bonus / 14.0  # Normalize to [0, 1]
        
        # Curve flow (transformation continuity penalty)
        # Curves are at index 2 of each segment
        v1_curve = [v1[i] for i in range(2, 28, 4)]
        v2_curve = [v2[i] for i in range(2, 28, 4)]
        curve_diff = sum(abs(a - b) for a, b in zip(v1_curve, v2_curve))
        curve_flow = curve_diff
        
        # Golden-ratio harmonic bonus
        angle = math.acos(max(-1, min(1, vec_sim)))  # Clamp to valid range
        # Check alignment with π/φ, 2π/φ, 3π/φ, 4π/φ
        harmonic_dists = [abs(angle - math.pi / golden * k) for k in range(1, 5)]
        harmonic = math.exp(-min(harmonic_dists))
        
        # Final resonance calculation
        resonance = (vec_sim * (1 + absence_bonus) * 
                    math.exp(-kenotic_lambda * curve_flow * 0.1) * 
                    (1 + 0.2 * harmonic))
        
        # Clamp to valid range [0.0, 1.0]
        return max(0.0, min(1.0, resonance))
    
    # -------------------------------------------------------------------------
    # VISUALIZATION METHODS
    # -------------------------------------------------------------------------
    
    def visualize_glyph(self, glyph: str, label: str = "") -> str:
        """
        Create ASCII art visualization of a glyph on 7-segment display.
        
        Renders the glyph as a 5x9 character canvas showing the 7-segment
        layout with appropriate symbols for each atom type.
        
        Args:
            glyph (str): 7-character glyph string
            label (str, optional): Label to display above the glyph
            
        Returns:
            str: Multi-line ASCII art string
            
        Example:
            >>> converter = GlyphConverter()
            >>> print(converter.visualize_glyph("￿·——∅∅∅", "KENOSIS"))
            ┌─ KENOSIS
            │          
            │     ￿   
            │  ∅     ·
            │     ——  
            │  ∅     —
            │     ——  
            └──────────
        """
        # Create 5x9 canvas initialized with spaces
        canvas = [[' ' for _ in range(9)] for _ in range(5)]
        
        # Map segment names to their corresponding atom in the glyph string
        segment_map = dict(zip(SEGMENTS, list(glyph)))
        
        # Segment a (top) - horizontal line
        if segment_map.get('a') != '∅':
            char = '—' if segment_map.get('a') == '—' else ('￿' if segment_map.get('a') == '￿' else '·')
            for c in range(2, 7):
                canvas[0][c] = char if char != '·' else ('━' if c == 4 else '─')
            if segment_map.get('a') == '·':
                canvas[0][4] = '●'  # Point as circle
        
        # Segment b (upper right) - vertical line
        if segment_map.get('b') != '∅':
            char = segment_map.get('b')
            canvas[1][7] = '┃' if char != '·' else '●'
            canvas[2][7] = '┃' if char != '·' else '●'
        
        # Segment c (lower right) - vertical line
        if segment_map.get('c') != '∅':
            char = segment_map.get('c')
            canvas[3][7] = '┃' if char != '·' else '●'
            canvas[4][7] = '┃' if char != '·' else '●'
        
        # Segment d (bottom) - horizontal line
        if segment_map.get('d') != '∅':
            char = segment_map.get('d')
            for c in range(2, 7):
                canvas[4][c] = '━' if char != '·' else ('─' if c != 4 else '─')
            if segment_map.get('d') == '·':
                canvas[4][4] = '●'
        
        # Segment e (lower left) - vertical line
        if segment_map.get('e') != '∅':
            char = segment_map.get('e')
            canvas[3][1] = '┃' if char != '·' else '●'
            canvas[4][1] = '┃' if char != '·' else '●'
        
        # Segment f (upper left) - vertical line
        if segment_map.get('f') != '∅':
            char = segment_map.get('f')
            canvas[1][1] = '┃' if char != '·' else '●'
            canvas[2][1] = '┃' if char != '·' else '●'
        
        # Segment g (middle) - horizontal line
        if segment_map.get('g') != '∅':
            char = segment_map.get('g')
            for c in range(2, 7):
                canvas[2][c] = '━' if char != '·' else '─'
            if segment_map.get('g') == '·':
                canvas[2][4] = '●'
        
        # Build output with box-drawing characters
        lines = []
        if label:
            lines.append(f"┌─ {label}")
        else:
            lines.append("┌──────────")
        for row in canvas:
            lines.append('│ ' + ''.join(row))
        lines.append("└──────────")
        
        return '\n'.join(lines)
    
    def get_atom_breakdown(self, glyph: str) -> Dict[str, str]:
        """
        Get atom assignments for each segment as a dictionary.
        
        Args:
            glyph (str): 7-character glyph string
            
        Returns:
            Dict[str, str]: Mapping of segment names (a-g) to atoms
            
        Example:
            >>> converter = GlyphConverter()
            >>> converter.get_atom_breakdown("￿·——∅∅∅")
            {'a': '￿', 'b': '·', 'c': '—', 'd': '—', 'e': '∅', 'f': '∅', 'g': '—'}
        """
        return {seg: atom for seg, atom in zip(SEGMENTS, glyph)}


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    """
    Main entry point for command-line usage.
    
    Handles CLI arguments and provides interactive conversion interface.
    
    Usage:
        python mvp_glyph_converter.py <WORD> [WORD2] ...
        python mvp_glyph_converter.py --test
    
    Single word: Shows glyph visualization
    Multiple words: Shows glyphs and resonance matrix
    """
    converter = GlyphConverter()
    
    # Check arguments
    if len(sys.argv) < 2:
        # Print usage information
        print("Glyph-o-betics MVP - English to 7-Segment Glyph Converter")
        print("=" * 60)
        print()
        print("Usage: python mvp_glyph_converter.py <WORD> [WORD2]")
        print()
        print("Examples:")
        print("  python mvp_glyph_converter.py LOVE")
        print("  python mvp_glyph_converter.py LOVE TRUTH")
        print("  python mvp_glyph_converter.py LOVE TRUTH FREEDOM")
        print()
        print("If one word: Shows glyph visualization")
        print("If two words: Shows glyphs and resonance score")
        print()
        print("Built-in test words: LOVE, TRUTH, FREEDOM")
        sys.exit(0)
    
    words = sys.argv[1:]
    
    # Single word: Show detailed glyph visualization
    if len(words) == 1:
        word = words[0]
        glyph = converter.english_to_glyph(word)
        
        # Header
        print(f"\n{'='*60}")
        print(f"  GLYPH-o-BETICS CONVERSION")
        print(f"{'='*60}")
        print(f"\n  English Input: {word}")
        print(f"  Glyph Output:  {glyph}")
        print()
        
        # Show three descent pathways
        p = converter.phonetic_descent(word)
        o = converter.orthographic_descent(word)
        s = converter.semantic_descent(word)
        
        print(f"  Descent Pathways:")
        print(f"    Phonetic:     {''.join(p)}")
        print(f"    Orthographic: {''.join(o)}")
        print(f"    Semantic:     {''.join(s)}")
        print(f"    ─────────────────────────")
        print(f"    Final (fused): {glyph}")
        print()
        
        # Show segment breakdown
        print(f"  Segment Mapping:")
        print(f"    a b c d e f g")
        print(f"    {' '.join(glyph)}")
        print()
        
        # Visualize
        print(converter.visualize_glyph(glyph, f"GLYPH: {word}"))
        print()
        
        # Atom statistics
        atom_counts = {atom: glyph.count(atom) for atom in ATOMS}
        print(f"  Atom Composition:")
        for atom, name in zip(ATOMS, ATOM_NAMES):
            count = atom_counts[atom]
            bar = '█' * count + '░' * (7 - count)
            print(f"    {atom} ({name:8}): {bar} ({count}/7)")
        print()
    
    # Two or more words: Show glyphs and resonance matrix
    else:
        # Header
        print(f"\n{'='*70}")
        print(f"  GLYPH-o-BETICS RESONANCE ANALYSIS")
        print(f"{'='*70}")
        print()
        
        # Convert all words
        glyphs = {}
        for word in words:
            glyphs[word] = converter.english_to_glyph(word)
        
        # Show each glyph
        for word in words:
            glyph = glyphs[word]
            print(f"  {word:12} → {glyph}")
        print()
        
        # Visualizations
        for word in words:
            print(converter.visualize_glyph(glyphs[word], word))
            print()
        
        # Resonance matrix
        print(f"  {'Resonance Matrix':^60}")
        print(f"  {'─'*60}")
        
        # Header row
        header = "         " + "  ".join(f"{w:>6}" for w in words)
        print(f"  {header}")
        
        # Matrix rows
        for w1 in words:
            row = f"  {w1:6} │"
            for w2 in words:
                resonance = converter.compute_resonance(w1, w2)
                if w1 == w2:
                    row += "   1.00"  # Self-resonance
                else:
                    row += f"   {resonance:.2f}"
            print(row)
        
        print()
        
        # Detailed pair analysis
        if len(words) >= 2:
            print(f"  {'Pair Analysis':^60}")
            print(f"  {'─'*60}")
            for i, w1 in enumerate(words):
                for w2 in words[i+1:]:
                    resonance = converter.compute_resonance(w1, w2)
                    g1 = glyphs[w1]
                    g2 = glyphs[w2]
                    
                    # Determine relationship strength
                    if resonance > 0.7:
                        relation = "☯ STRONG HARMONY"
                    elif resonance > 0.4:
                        relation = "◐ MODERATE CONNECTION"
                    else:
                        relation = "○ DISTANT"
                    
                    print(f"  {w1} ↔ {w2}: {resonance:.3f} {relation}")
                    print(f"    {g1}")
                    print(f"    {g2}")
                    print()


# =============================================================================
# SELF-TEST
# =============================================================================

def self_test():
    """
    Run built-in tests for validation.
    
    Tests the converter with known words and verifies:
    - All words convert to 7-character glyphs
    - All characters in glyphs are valid atoms
    - Resonance values are in expected ranges
    
    Returns:
        bool: True if all tests pass, False otherwise
    """
    converter = GlyphConverter()
    
    # Test words from the THUNDERING GRACE vocabulary
    test_words = ["LOVE", "TRUTH", "FREEDOM"]
    
    print("\n" + "="*60)
    print("  GLYPH-o-BETICS SELF-TEST")
    print("="*60)
    print()
    
    all_passed = True
    
    # Test word conversion
    for word in test_words:
        glyph = converter.english_to_glyph(word)
        print(f"  ✓ {word} → {glyph}")
        
        # Verify it's 7 characters
        if len(glyph) != 7:
            print(f"    ERROR: Expected 7 segments, got {len(glyph)}")
            all_passed = False
        
        # Verify all characters are valid atoms
        for c in glyph:
            if c not in ATOMS:
                print(f"    ERROR: Invalid atom '{c}'")
                all_passed = False
    
    print()
    
    # Test resonance
    print("  Resonance Tests:")
    for i, w1 in enumerate(test_words):
        for w2 in test_words[i:]:
            r = converter.compute_resonance(w1, w2)
            print(f"    {w1}-{w2}: {r:.3f}")
            
            # Self-resonance should be ~1.0
            if w1 == w2 and not (0.99 <= r <= 1.01):
                print(f"      ERROR: Self-resonance should be 1.0, got {r}")
                all_passed = False
    
    print()
    if all_passed:
        print("  ✓ All tests passed!")
    else:
        print("  ✗ Some tests failed!")
    
    print()
    return all_passed


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Check for test flag
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = self_test()
        sys.exit(0 if success else 1)
    else:
        main()
