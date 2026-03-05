package org.thundergrace.glyph;

import java.util.EnumMap;

/**
 * SimpleGlyph - 7-Segment Lattice Representation
 * 
 * Implements the Glyphobetics v2.0 atomic specification:
 * - 4 atoms: POINT(·), LINE(—), CURVE(￿), ABSENCE(∅)
 * - 7 segments: a,b,c,d,e,f,g (standard digital display topology)
 * - 28-dimensional vector representation
 * 
 * KENOSIS glyph: ￿·—— (Curve, Point, Line, Line)
 *   a(top)=￿, b(ur)=·, g(mid)=—, d(bot)=—
 */
public class SimpleGlyph {
    
    public enum Atom {
        POINT("·", 0),
        LINE("—", 1),
        CURVE("￿", 2),
        ABSENCE("∅", 3);
        
        private final String symbol;
        private final int index;
        
        Atom(String symbol, int index) {
            this.symbol = symbol;
            this.index = index;
        }
        
        public String getSymbol() { return symbol; }
        public int getIndex() { return index; }
    }
    
    public enum Segment {
        A(0, "top"),
        B(1, "upperRight"),
        C(2, "lowerRight"),
        D(3, "bottom"),
        E(4, "lowerLeft"),
        F(5, "upperLeft"),
        G(6, "middle");
        
        private final int index;
        private final String description;
        
        Segment(int index, String description) {
            this.index = index;
            this.description = description;
        }
        
        public int getIndex() { return index; }
        public String getDescription() { return description; }
    }
    
    // 28-dimensional vector: 7 segments × 4 atoms
    private double[] vector;
    private EnumMap<Segment, Atom> assignment;
    private String name;
    
    public SimpleGlyph(String name) {
        this.name = name;
        this.vector = new double[28];
        this.assignment = new EnumMap<>(Segment.class);
        // Initialize all segments to ABSENCE
        for (Segment s : Segment.values()) {
            setAtom(s, Atom.ABSENCE);
        }
    }
    
    public void setAtom(Segment segment, Atom atom) {
        // Clear previous atom for this segment
        for (Atom a : Atom.values()) {
            vector[segment.index * 4 + a.index] = 0.0;
        }
        // Set new atom
        vector[segment.index * 4 + atom.index] = 1.0;
        assignment.put(segment, atom);
    }
    
    public Atom getAtom(Segment segment) {
        return assignment.getOrDefault(segment, Atom.ABSENCE);
    }
    
    public double[] getVector() {
        return vector.clone();
    }
    
    public String getName() {
        return name;
    }
    
    /**
     * Create the KENOSIS glyph: ￿·——
     * Curve top, Point upper-right, Line middle, Line bottom
     */
    public static SimpleGlyph createKENOSIS() {
        SimpleGlyph glyph = new SimpleGlyph("KENOSIS");
        glyph.setAtom(Segment.A, Atom.CURVE);   // ￿ top
        glyph.setAtom(Segment.B, Atom.POINT);   // · upper right
        glyph.setAtom(Segment.G, Atom.LINE);    // — middle
        glyph.setAtom(Segment.D, Atom.LINE);    // — bottom
        // c, e, f remain ABSENCE
        return glyph;
    }
    
    /**
     * Create the GRACE glyph: ·￿——
     */
    public static SimpleGlyph createGRACE() {
        SimpleGlyph glyph = new SimpleGlyph("GRACE");
        glyph.setAtom(Segment.A, Atom.POINT);
        glyph.setAtom(Segment.B, Atom.CURVE);
        glyph.setAtom(Segment.G, Atom.LINE);
        glyph.setAtom(Segment.D, Atom.LINE);
        return glyph;
    }
    
    /**
     * Compute resonance with another glyph (Looman resonance)
     */
    public double computeResonance(SimpleGlyph other) {
        double[] v1 = this.vector;
        double[] v2 = other.vector;
        
        // Vector similarity (cosine)
        double dot = 0.0, norm1 = 0.0, norm2 = 0.0;
        for (int i = 0; i < 28; i++) {
            dot += v1[i] * v2[i];
            norm1 += v1[i] * v1[i];
            norm2 += v2[i] * v2[i];
        }
        double cosSim = dot / (Math.sqrt(norm1) * Math.sqrt(norm2) + 1e-8);
        
        // Absence bonus (kenotic weighting)
        double absenceBonus = 0.0;
        for (int i = 3; i < 28; i += 4) {
            absenceBonus += v1[i] + v2[i];
        }
        absenceBonus /= 14.0;
        
        // Golden ratio harmonic
        double golden = (1 + Math.sqrt(5)) / 2;
        double angle = Math.acos(Math.max(-1, Math.min(1, cosSim)));
        double minDiff = Double.MAX_VALUE;
        for (int k = 1; k <= 4; k++) {
            double diff = Math.abs(angle - Math.PI / golden * k);
            minDiff = Math.min(minDiff, diff);
        }
        double harmonic = Math.exp(-minDiff);
        
        return cosSim * (1 + absenceBonus) * harmonic;
    }
    
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(name).append(": ");
        for (Segment s : Segment.values()) {
            sb.append(getAtom(s).getSymbol());
        }
        return sb.toString();
    }
    
    /**
     * Get atomic sequence as string (non-absence atoms only)
     */
    public String getAtomicSequence() {
        StringBuilder sb = new StringBuilder();
        for (Segment s : new Segment[]{Segment.A, Segment.B, Segment.G, Segment.D, Segment.F, Segment.E, Segment.C}) {
            Atom a = getAtom(s);
            if (a != Atom.ABSENCE) {
                sb.append(a.getSymbol());
            }
        }
        return sb.toString();
    }
}
