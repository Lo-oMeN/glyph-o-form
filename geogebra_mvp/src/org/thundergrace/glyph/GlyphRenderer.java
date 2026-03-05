package org.thundergrace.glyph;

import org.geogebra.desktop.main.AppD;
import org.geogebra.common.kernel.Construction;
import org.geogebra.common.kernel.geos.GeoPoint;
import org.geogebra.common.kernel.geos.GeoLine;
import org.geogebra.common.kernel.geos.GeoConic;
import org.geogebra.common.kernel.geos.GeoElement;
import org.geogebra.common.kernel.kernelND.GeoPointND;
import org.geogebra.common.awt.GColor;
import org.geogebra.common.awt.GGraphics2D;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * GlyphRenderer - Draws atomic glyphs on GeoGebra canvas
 * 
 * Maps the 7-segment lattice to draggable GeoGebra elements:
 * - POINT (·) → GeoPoint
 * - LINE (—) → GeoLine (segment)
 * - CURVE (￿) → GeoConic (arc) or parametric curve
 * - ABSENCE (∅) → No rendering
 * 
 * Implements 60 FPS cascading updates from TGE Layer 0.
 */
public class GlyphRenderer {
    
    private AppD app;
    private Construction cons;
    private SimpleGlyph currentGlyph;
    
    // Map segments to their rendered GeoGebra elements
    private Map<SimpleGlyph.Segment, List<GeoElement>> segmentElements;
    private Map<SimpleGlyph.Segment, double[]> segmentPositions;
    
    // Visual styling
    private GColor curveColor;
    private GColor pointColor;
    private GColor lineColor;
    private double scale = 100.0;
    private double centerX = 0.0;
    private double centerY = 0.0;
    
    public GlyphRenderer(AppD app) {
        this.app = app;
        this.cons = app.getKernel().getConstruction();
        this.segmentElements = new HashMap<>();
        this.segmentPositions = new HashMap<>();
        
        // THUNDERING GRACE colors
        this.curveColor = GColor.newColor(220, 100, 100);  // Reddish (Axis of Fact)
        this.pointColor = GColor.newColor(255, 200, 50);   // Gold
        this.lineColor = GColor.newColor(100, 150, 220);   // Blue
        
        initializePositions();
    }
    
    /**
     * Initialize 7-segment lattice positions
     * Standard digital display topology centered at origin
     */
    private void initializePositions() {
        double w = scale;      // width
        double h = scale * 1.5; // height
        double m = scale * 0.1;  // margin
        
        // Segment centers (for element placement)
        segmentPositions.put(SimpleGlyph.Segment.A, new double[]{centerX, centerY - h/2});
        segmentPositions.put(SimpleGlyph.Segment.B, new double[]{centerX + w/2 - m, centerY - h/4});
        segmentPositions.put(SimpleGlyph.Segment.C, new double[]{centerX + w/2 - m, centerY + h/4});
        segmentPositions.put(SimpleGlyph.Segment.D, new double[]{centerX, centerY + h/2});
        segmentPositions.put(SimpleGlyph.Segment.E, new double[]{centerX - w/2 + m, centerY + h/4});
        segmentPositions.put(SimpleGlyph.Segment.F, new double[]{centerX - w/2 + m, centerY - h/4});
        segmentPositions.put(SimpleGlyph.Segment.G, new double[]{centerX, centerY});
    }
    
    /**
     * Render a glyph to the GeoGebra canvas
     */
    public void render(SimpleGlyph glyph) {
        // Clear previous rendering
        clear();
        
        this.currentGlyph = glyph;
        
        // Render each segment according to its atom
        for (SimpleGlyph.Segment segment : SimpleGlyph.Segment.values()) {
            SimpleGlyph.Atom atom = glyph.getAtom(segment);
            renderSegment(segment, atom);
        }
        
        // Update view
        app.getKernel().notifyRepaint();
    }
    
    /**
     * Render a single segment with its assigned atom
     */
    private void renderSegment(SimpleGlyph.Segment segment, SimpleGlyph.Atom atom) {
        List<GeoElement> elements = new ArrayList<>();
        double[] pos = segmentPositions.get(segment);
        double x = pos[0];
        double y = pos[1];
        double size = scale * 0.4;
        
        switch (atom) {
            case CURVE:
                // CURVE (￿) - Render as arc or sine wave segment
                elements.addAll(createCurveElement(segment, x, y, size));
                break;
                
            case POINT:
                // POINT (·) - Render as point
                elements.add(createPointElement(segment, x, y, size * 0.3));
                break;
                
            case LINE:
                // LINE (—) - Render as line segment
                elements.addAll(createLineElement(segment, x, y, size));
                break;
                
            case ABSENCE:
                // ABSENCE (∅) - No rendering (generative void)
                break;
        }
        
        segmentElements.put(segment, elements);
    }
    
    /**
     * Create a POINT element (GeoPoint)
     */
    private GeoElement createPointElement(SimpleGlyph.Segment segment, double x, double y, double size) {
        GeoPoint point = new GeoPoint(cons, x, y, 1.0);
        point.setLabel(null);
        point.setObjColor(pointColor);
        point.setPointSize((int)(size * 10));
        point.setFixed(false); // Draggable
        point.setSelectionAllowed(true);
        
        // Add to construction
        cons.addToConstructionList(point, false);
        
        return point;
    }
    
    /**
     * Create LINE elements (GeoLine segments)
     */
    private List<GeoElement> createLineElement(SimpleGlyph.Segment segment, double x, double y, double size) {
        List<GeoElement> elements = new ArrayList<>();
        
        double x1, y1, x2, y2;
        
        // Orientation based on segment position
        switch (segment) {
            case A: // Top horizontal
                x1 = x - size; y1 = y;
                x2 = x + size; y2 = y;
                break;
            case D: // Bottom horizontal
                x1 = x - size; y1 = y;
                x2 = x + size; y2 = y;
                break;
            case G: // Middle horizontal
                x1 = x - size; y1 = y;
                x2 = x + size; y2 = y;
                break;
            case B: // Upper right vertical
            case C: // Lower right vertical
                x1 = x; y1 = y - size * 0.6;
                x2 = x; y2 = y + size * 0.6;
                break;
            case F: // Upper left vertical
            case E: // Lower left vertical
                x1 = x; y1 = y - size * 0.6;
                x2 = x; y2 = y + size * 0.6;
                break;
            default:
                x1 = x - size; y1 = y;
                x2 = x + size; y2 = y;
        }
        
        // Create endpoints as draggable points
        GeoPoint p1 = new GeoPoint(cons, x1, y1, 1.0);
        GeoPoint p2 = new GeoPoint(cons, x2, y2, 1.0);
        p1.setLabel(null);
        p2.setLabel(null);
        p1.setSelectionAllowed(true);
        p2.setSelectionAllowed(true);
        p1.setFixed(false);
        p2.setFixed(false);
        
        // Create line through points
        GeoLine line = new GeoLine(cons, null, p1, p2);
        line.setObjColor(lineColor);
        line.setLineThickness(4);
        
        cons.addToConstructionList(p1, false);
        cons.addToConstructionList(p2, false);
        cons.addToConstructionList(line, false);
        
        elements.add(p1);
        elements.add(p2);
        elements.add(line);
        
        return elements;
    }
    
    /**
     * Create CURVE elements (parametric arc)
     * For KENOSIS: Top curve (￿) - represents dimensional decompressor
     */
    private List<GeoElement> createCurveElement(SimpleGlyph.Segment segment, double x, double y, double size) {
        List<GeoElement> elements = new ArrayList<>();
        
        // For segment A (top), create an upward arc
        if (segment == SimpleGlyph.Segment.A) {
            // Create control points for the curve
            GeoPoint left = new GeoPoint(cons, x - size, y, 1.0);
            GeoPoint peak = new GeoPoint(cons, x, y - size * 0.5, 1.0);
            GeoPoint right = new GeoPoint(cons, x + size, y, 1.0);
            
            left.setLabel(null);
            peak.setLabel(null);
            right.setLabel(null);
            
            // Make all points draggable
            for (GeoPoint p : new GeoPoint[]{left, peak, right}) {
                p.setSelectionAllowed(true);
                p.setFixed(false);
                p.setObjColor(curveColor);
                cons.addToConstructionList(p, false);
                elements.add(p);
            }
            
            // Create conic arc through three points
            GeoConic arc = createConicArc(left, peak, right);
            arc.setObjColor(curveColor);
            arc.setLineThickness(5);
            cons.addToConstructionList(arc, false);
            elements.add(arc);
        } else {
            // For other segments, create a sine-like wave
            int numPoints = 5;
            GeoPoint[] points = new GeoPoint[numPoints];
            for (int i = 0; i < numPoints; i++) {
                double t = (double) i / (numPoints - 1);
                double px = x - size + 2 * size * t;
                double py = y + size * 0.2 * Math.sin(t * Math.PI * 2);
                points[i] = new GeoPoint(cons, px, py, 1.0);
                points[i].setLabel(null);
                points[i].setSelectionAllowed(true);
                points[i].setFixed(false);
                points[i].setObjColor(curveColor);
                cons.addToConstructionList(points[i], false);
                elements.add(points[i]);
            }
        }
        
        return elements;
    }
    
    /**
     * Create a conic arc through three points
     */
    private GeoConic createConicArc(GeoPoint p1, GeoPoint p2, GeoPoint p3) {
        // Create a circle through three points (simplest conic arc)
        GeoConic circle = new GeoConic(cons, new GeoPoint[]{p1, p2, p3});
        return circle;
    }
    
    /**
     * Clear all rendered elements
     */
    public void clear() {
        for (List<GeoElement> elements : segmentElements.values()) {
            for (GeoElement geo : elements) {
                geo.remove();
            }
        }
        segmentElements.clear();
    }
    
    /**
     * Get elements for a specific segment (for drag handling)
     */
    public List<GeoElement> getSegmentElements(SimpleGlyph.Segment segment) {
        return segmentElements.getOrDefault(segment, new ArrayList<>());
    }
    
    /**
     * Get segment from an element (reverse lookup)
     */
    public SimpleGlyph.Segment getSegmentFromElement(GeoElement element) {
        for (Map.Entry<SimpleGlyph.Segment, List<GeoElement>> entry : segmentElements.entrySet()) {
            if (entry.getValue().contains(element)) {
                return entry.getKey();
            }
        }
        return null;
    }
    
    public SimpleGlyph getCurrentGlyph() {
        return currentGlyph;
    }
    
    public void setScale(double scale) {
        this.scale = scale;
        initializePositions();
    }
    
    public void setCenter(double x, double y) {
        this.centerX = x;
        this.centerY = y;
        initializePositions();
    }
    
    /**
     * Update rendering after a drag operation
     */
    public void updateAfterDrag() {
        app.getKernel().notifyRepaint();
    }
}
