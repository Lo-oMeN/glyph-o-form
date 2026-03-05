#!/usr/bin/env python3
"""
Glyph-o-betics MVP - Minimal Functional Demo
Converts English words to 7-segment glyph representations

Usage: python mvp_glyph_converter.py <WORD> [WORD2]
"""

import sys
import math
import re
from typing import List, Tuple, Dict

# =============================================================================
# GLYPHOBETICS CONSTANTS
# =============================================================================

# Four Atoms
ATOMS = ['·', '—', '￿', '∅']  # Point, Line, Curve, Absence
ATOM_NAMES = ['Point', 'Line', 'Curve', 'Absence']

# 7-Segment Layout
SEGMENTS = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

# Segment positions for visualization (row, col_start, col_end)
SEGMENT_POSITIONS = {
    'a': (0, 2, 6),
    'b': (1, 6, 8),
    'c': (3, 6, 8),
    'd': (4, 2, 6),
    'e': (3, 0, 2),
    'f': (1, 0, 2),
    'g': (2, 2, 6)
}

# Phoneme to atom mapping (simplified)
PHONETIC_MAP = {
    # Vowels → Curve
    'a': '￿', 'e': '￿', 'i': '￿', 'o': '￿', 'u': '￿',
    'A': '￿', 'E': '￿', 'I': '￿', 'O': '￿', 'U': '￿',
    # Plosives → Point  
    'p': '·', 't': '·', 'k': '·', 'b': '·', 'd': '·', 'g': '·',
    'P': '·', 'T': '·', 'K': '·', 'B': '·', 'D': '·', 'G': '·',
    # Fricatives → Line
    'f': '—', 'v': '—', 's': '—', 'z': '—', 'h': '—',
    'F': '—', 'V': '—', 'S': '—', 'Z': '—', 'H': '—',
    'w': '—', 'W': '—',
    # Nasals → Absence
    'm': '∅', 'n': '∅', 'M': '∅', 'N': '∅',
    # Liquids → Curve-Point hybrid (use Curve)
    'l': '￿', 'r': '￿', 'L': '￿', 'R': '￿',
    # Others default to Curve
    'y': '￿', 'Y': '￿',
}

# Orthographic stroke mapping (letter → atoms)
ORTHGRAPHIC_MAP = {
    'A': ['—', '—', '—'],      # Two diagonals + cross
    'B': ['—', '—', '￿'],      # Vertical + two curves  
    'C': ['￿'],                 # Curve
    'D': ['—', '￿'],            # Vertical + curve
    'E': ['—', '—', '—'],      # Three horizontals
    'F': ['—', '—'],            # Two horizontals + vertical
    'G': ['￿', '—'],            # Curve + horizontal
    'H': ['—', '—', '—'],      # Two verticals + cross
    'I': ['—', '·', '—'],      # Vertical + two caps
    'J': ['￿'],                 # Hook curve
    'K': ['—', '—', '—'],      # Vertical + two diagonals
    'L': ['—', '—'],            # Vertical + horizontal
    'M': ['—', '—', '—'],       # Two verticals + two diagonals
    'N': ['—', '—', '—'],       # Two verticals + diagonal
    'O': ['￿'],                 # Closed curve
    'P': ['—', '￿'],            # Vertical + curve
    'Q': ['￿', '·'],            # Circle + tail
    'R': ['—', '￿', '·'],       # P + diagonal
    'S': ['￿'],                 # Curve
    'T': ['—', '—'],            # Horizontal + vertical
    'U': ['￿'],                 # Curve
    'V': ['—', '—'],            # Two diagonals
    'W': ['—', '—', '—', '—'],  # Complex diagonals
    'X': ['—', '—'],            # Two diagonals
    'Y': ['—', '—', '—'],       # Two diagonals + vertical
    'Z': ['—', '—', '—'],       # Three horizontals (with diagonals)
}

# Semantic field mappings (simplified - based on word patterns)
SEMANTIC_PATTERNS = {
    # Love/Connection words
    'LOV': ['￿', '·', '￿', '∅', '—', '￿', '—'],
    'HEA': ['￿', '·', '￿', '∅', '—', '￿', '—'],
    'BO': ['￿', '·', '￿', '∅', '—', '￿', '—'],
    # Truth/Knowledge words
    'TRU': ['·', '—', '·', '∅', '—', '￿', '∅'],
    'KNO': ['·', '—', '·', '∅', '—', '￿', '∅'],
    'FAC': ['·', '—', '·', '∅', '—', '￿', '∅'],
    # Freedom/Open words
    'FRE': ['￿', '—', '∅', '∅', '—', '￿', '—'],
    'OPE': ['￿', '—', '∅', '∅', '—', '￿', '—'],
    'WID': ['￿', '—', '∅', '∅', '—', '￿', '—'],
    # Life/Growth words
    'LIF': ['￿', '·', '￿', '·', '—', '￿', '—'],
    'GRO': ['￿', '·', '￿', '·', '—', '￿', '—'],
    # Death/End words
    'DEA': ['∅', '∅', '·', '∅', '￿', '∅', '·'],
    'END': ['∅', '∅', '·', '∅', '￿', '∅', '·'],
}

# =============================================================================
# GLYPH CONVERTER CLASS
# =============================================================================

class GlyphConverter:
    """English → 7-Segment Glyph converter"""
    
    def __init__(self):
        self.atoms = ATOMS
        self.segments = SEGMENTS
        
    def phonetic_descent(self, word: str) -> List[str]:
        """
        Pathway 1: Phonetic descent (sound → curve)
        Maps letters to atoms based on phonetic character
        """
        atoms = []
        for char in word:
            if char in PHONETIC_MAP:
                atoms.append(PHONETIC_MAP[char])
            else:
                atoms.append('￿')  # Default to Curve
        return self._distribute_to_segments(atoms)
    
    def orthographic_descent(self, word: str) -> List[str]:
        """
        Pathway 2: Orthographic descent (shape → atom)
        Maps letter strokes to atoms
        """
        atoms = []
        for char in word.upper():
            if char in ORTHGRAPHIC_MAP:
                strokes = ORTHGRAPHIC_MAP[char]
                atoms.extend(strokes)
            else:
                atoms.append('·')  # Default to Point
        return self._distribute_to_segments(atoms)
    
    def semantic_descent(self, word: str) -> List[str]:
        """
        Pathway 3: Semantic descent (meaning → topology)
        Maps semantic field to atoms
        """
        word_upper = word.upper()
        
        # Check for semantic patterns
        for prefix, pattern in SEMANTIC_PATTERNS.items():
            if word_upper.startswith(prefix):
                return pattern
        
        # Default: Generate from word characteristics
        atoms = []
        word_len = len(word)
        vowel_count = sum(1 for c in word if c.lower() in 'aeiou')
        
        for i in range(7):
            # Use word length and vowel ratio to determine atoms
            position_ratio = i / 6.0
            char_idx = int(position_ratio * (word_len - 1)) if word_len > 1 else 0
            char = word[char_idx].upper() if char_idx < word_len else 'A'
            
            # Heuristic: Vowel-heavy words get more Curves
            vowel_ratio = vowel_count / max(word_len, 1)
            
            if vowel_ratio > 0.4:
                # High vowel ratio → Curve dominant
                atom_choices = ['￿', '￿', '·', '∅']
            elif vowel_ratio > 0.2:
                # Medium → Mixed
                atom_choices = ['—', '￿', '·', '∅']
            else:
                # Low → Line/Point dominant
                atom_choices = ['—', '—', '·', '∅']
            
            # Deterministic selection based on character
            char_val = ord(char) if char.isalpha() else 65
            atom_idx = (char_val + i * 7) % 4
            atoms.append(atom_choices[atom_idx])
        
        return atoms
    
    def _distribute_to_segments(self, atoms: List[str]) -> List[str]:
        """Distribute atoms across 7 segments"""
        segments = ['∅'] * 7
        for i, atom in enumerate(atoms[:7]):
            segments[i] = atom
        return segments
    
    def fuse_pathways(self, phonetic: List[str], orthographic: List[str], 
                     semantic: List[str]) -> str:
        """
        Fuse three descent pathways into final glyph
        Uses majority voting with kenotic bias (Absence amplification)
        """
        final = []
        
        for i in range(7):
            votes = [phonetic[i], orthographic[i], semantic[i]]
            
            # Count occurrences
            counts = {}
            for v in votes:
                counts[v] = counts.get(v, 0) + (0.5 if v == '∅' else 1)
            
            # Kenotic amplification: if two ∅, ∅ wins
            if votes.count('∅') >= 2:
                final.append('∅')
            else:
                # Get atom with highest count
                final.append(max(counts, key=counts.get))
        
        return ''.join(final)
    
    def english_to_glyph(self, word: str) -> str:
        """
        Full transformation pipeline
        English word → 7-segment glyph
        """
        if not word or not word.strip():
            return '∅∅∅∅∅∅∅'
        
        p = self.phonetic_descent(word)
        o = self.orthographic_descent(word)
        s = self.semantic_descent(word)
        
        return self.fuse_pathways(p, o, s)
    
    def glyph_to_vector(self, glyph: str) -> List[float]:
        """
        Convert glyph string to 28-dimensional vector
        (7 segments × 4 atoms, one-hot encoding)
        """
        vector = [0.0] * 28
        for i, atom in enumerate(glyph):
            if i >= 7:
                break
            if atom in ATOMS:
                atom_idx = ATOMS.index(atom)
                vector[i * 4 + atom_idx] = 1.0
        return vector
    
    def compute_resonance(self, word1: str, word2: str) -> float:
        """
        Compute Looman resonance between two words
        Returns resonance score (0.0 to 1.0+)
        """
        g1 = self.english_to_glyph(word1)
        g2 = self.english_to_glyph(word2)
        
        v1 = self.glyph_to_vector(g1)
        v2 = self.glyph_to_vector(g2)
        
        return self._atomic_resonance(v1, v2)
    
    def _atomic_resonance(self, v1: List[float], v2: List[float], 
                         kenotic_lambda: float = 1.618) -> float:
        """
        Atomic Looman Resonance Engine
        Computes resonance between two 28-dim atomic vectors
        """
        import math
        
        golden = (1 + math.sqrt(5)) / 2  # φ
        
        # Vector similarity (cosine)
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        
        if norm1 < 1e-8 or norm2 < 1e-8:
            return 0.0
        
        vec_sim = dot_product / (norm1 * norm2)
        
        # Absence bonus (kenosis weighting)
        # Absence is at index 3 of each segment
        v1_absence = [v1[i] for i in range(3, 28, 4)]
        v2_absence = [v2[i] for i in range(3, 28, 4)]
        absence_bonus = sum(v1_absence) + sum(v2_absence)
        absence_bonus = absence_bonus / 14.0  # Normalize
        
        # Curve flow (transformation continuity)
        # Curves are at index 2
        v1_curve = [v1[i] for i in range(2, 28, 4)]
        v2_curve = [v2[i] for i in range(2, 28, 4)]
        curve_diff = sum(abs(a - b) for a, b in zip(v1_curve, v2_curve))
        curve_flow = curve_diff
        
        # Golden-ratio harmonic
        angle = math.acos(max(-1, min(1, vec_sim)))
        harmonic_dists = [abs(angle - math.pi / golden * k) for k in range(1, 5)]
        harmonic = math.exp(-min(harmonic_dists))
        
        # Final resonance
        resonance = (vec_sim * (1 + absence_bonus) * 
                    math.exp(-kenotic_lambda * curve_flow * 0.1) * 
                    (1 + 0.2 * harmonic))
        
        return max(0.0, min(1.0, resonance))
    
    def visualize_glyph(self, glyph: str, label: str = "") -> str:
        """
        Create ASCII art visualization of a glyph on 7-segment display
        """
        # Create 5x9 canvas
        canvas = [[' ' for _ in range(9)] for _ in range(5)]
        
        # Map segments to positions
        segment_map = dict(zip(SEGMENTS, list(glyph)))
        
        # Segment a (top)
        if segment_map.get('a') != '∅':
            char = '—' if segment_map.get('a') == '—' else ('￿' if segment_map.get('a') == '￿' else '·')
            for c in range(2, 7):
                canvas[0][c] = char if char != '·' else ('━' if c == 4 else '─')
            if segment_map.get('a') == '·':
                canvas[0][4] = '●'
        
        # Segment b (upper right)
        if segment_map.get('b') != '∅':
            char = segment_map.get('b')
            canvas[1][7] = '┃' if char != '·' else '●'
            canvas[2][7] = '┃' if char != '·' else '●'
        
        # Segment c (lower right)
        if segment_map.get('c') != '∅':
            char = segment_map.get('c')
            canvas[3][7] = '┃' if char != '·' else '●'
            canvas[4][7] = '┃' if char != '·' else '●'
        
        # Segment d (bottom)
        if segment_map.get('d') != '∅':
            char = segment_map.get('d')
            for c in range(2, 7):
                canvas[4][c] = '━' if char != '·' else ('─' if c != 4 else '─')
            if segment_map.get('d') == '·':
                canvas[4][4] = '●'
        
        # Segment e (lower left)
        if segment_map.get('e') != '∅':
            char = segment_map.get('e')
            canvas[3][1] = '┃' if char != '·' else '●'
            canvas[4][1] = '┃' if char != '·' else '●'
        
        # Segment f (upper left)
        if segment_map.get('f') != '∅':
            char = segment_map.get('f')
            canvas[1][1] = '┃' if char != '·' else '●'
            canvas[2][1] = '┃' if char != '·' else '●'
        
        # Segment g (middle)
        if segment_map.get('g') != '∅':
            char = segment_map.get('g')
            for c in range(2, 7):
                canvas[2][c] = '━' if char != '·' else '─'
            if segment_map.get('g') == '·':
                canvas[2][4] = '●'
        
        # Build output
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
        """Get atom assignments for each segment"""
        return {seg: atom for seg, atom in zip(SEGMENTS, glyph)}


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    converter = GlyphConverter()
    
    # Check arguments
    if len(sys.argv) < 2:
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
    
    # Single word: Show glyph
    if len(words) == 1:
        word = words[0]
        glyph = converter.english_to_glyph(word)
        
        print(f"\n{'='*60}")
        print(f"  GLYPH-o-BETICS CONVERSION")
        print(f"{'='*60}")
        print(f"\n  English Input: {word}")
        print(f"  Glyph Output:  {glyph}")
        print()
        
        # Show three pathways
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
        
        # Atom stats
        atom_counts = {atom: glyph.count(atom) for atom in ATOMS}
        print(f"  Atom Composition:")
        for atom, name in zip(ATOMS, ATOM_NAMES):
            count = atom_counts[atom]
            bar = '█' * count + '░' * (7 - count)
            print(f"    {atom} ({name:8}): {bar} ({count}/7)")
        print()
    
    # Two or more words: Show glyphs and resonance matrix
    else:
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
        
        # Header
        header = "         " + "  ".join(f"{w:>6}" for w in words)
        print(f"  {header}")
        
        # Rows
        for w1 in words:
            row = f"  {w1:6} │"
            for w2 in words:
                resonance = converter.compute_resonance(w1, w2)
                if w1 == w2:
                    row += "   1.00"
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
                    
                    # Determine relationship
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
    """Run built-in tests"""
    converter = GlyphConverter()
    
    test_words = ["LOVE", "TRUTH", "FREEDOM"]
    
    print("\n" + "="*60)
    print("  GLYPH-o-BETICS SELF-TEST")
    print("="*60)
    print()
    
    all_passed = True
    
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
    
    print()
    if all_passed:
        print("  ✓ All tests passed!")
    else:
        print("  ✗ Some tests failed!")
    
    print()
    return all_passed


if __name__ == "__main__":
    # Check for test flag
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        self_test()
    else:
        main()
