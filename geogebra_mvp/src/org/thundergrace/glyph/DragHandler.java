package org.thundergrace.glyph;

import org.geogebra.desktop.main.AppD;
import org.geogebra.common.kernel.geos.GeoElement;
import org.geogebra.common.kernel.geos.GeoPoint;
import org.geogebra.common.euclidian.event.AbstractEvent;
import org.geogebra.common.euclidian.EuclidianController;
import org.geogebra.common.euclidian.EuclidianView;

import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.util.List;

/**
 * DragHandler - Mouse drag → Atom update
 * 
 * Implements TGE Layer 0 cascading updates:
 * - User drags any glyph element (point, line, curve)
 * - Propagates through dependency graph
 * - 60 FPS real-time rendering
 * - Updates glyph vector representation
 * 
 * KENOSIS glyph elements:
 * - Curve (a): Draggable control points adjust arc
 * - Point (b): Draggable position
 * - Lines (g, d): Draggable endpoints
 */
public class DragHandler {
    
    private AppD app;
    private GlyphRenderer renderer;
    private SimpleGlyph currentGlyph;
    
    // Drag state
    private boolean isDragging = false;
    private GeoElement draggedElement = null;
    private SimpleGlyph.Segment draggedSegment = null;
    private double dragStartX, dragStartY;
    
    // RSTL state tracking
    private RSTLState currentRSTLState = RSTLState.POTENTIAL;
    
    public enum RSTLState {
        NULL,       // ∅ - Death, untangled
        POTENTIAL,  // △ - Elevating, becoming
        ACTUALIZED  // ■ - Locked glory
    }
    
    // Free-energy descent parameters (Layer 5)
    private double K = 0.1;           // Descent rate
    private double lambda = 1.618;    // Kenotic weight (golden ratio)
    private double structuralEnergy = 0.0;
    private double constraintEnergy = 0.0;
    
    public DragHandler(AppD app, GlyphRenderer renderer) {
        this.app = app;
        this.renderer = renderer;
        setupDragListeners();
    }
    
    /**
     * Setup mouse drag listeners on the Euclidian view
     */
    private void setupDragListeners() {
        EuclidianView view = app.getEuclidianView1();
        if (view == null) return;
        
        java.awt.Component canvas = view.getExportImage();
        if (canvas == null) {
            // Fallback: use the view component directly
            canvas = (java.awt.Component) view;
        }
        
        // Mouse pressed - start drag
        canvas.addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                handleMousePressed(e.getX(), e.getY());
            }
            
            @Override
            public void mouseReleased(MouseEvent e) {
                handleMouseReleased();
            }
        });
        
        // Mouse dragged - update
        canvas.addMouseMotionListener(new MouseMotionAdapter() {
            @Override
            public void mouseDragged(MouseEvent e) {
                handleMouseDragged(e.getX(), e.getY());
            }
        });
    }
    
    /**
     * Handle mouse press - identify what was clicked
     */
    private void handleMousePressed(int screenX, int screenY) {
        EuclidianView view = app.getEuclidianView1();
        if (view == null) return;
        
        // Convert screen to mathematical coordinates
        double[] coords = view.getFromScreenLocation(screenX, screenY);
        double x = coords[0];
        double y = coords[1];
        
        dragStartX = x;
        dragStartY = y;
        
        // Find closest glyph element
        draggedElement = findElementAt(x, y);
        
        if (draggedElement != null) {
            isDragging = true;
            draggedSegment = renderer.getSegmentFromElement(draggedElement);
            
            // Enter POTENTIAL state on drag start
            setRSTLState(RSTLState.POTENTIAL);
            
            System.out.println("[DRAG] Started dragging " + 
                (draggedSegment != null ? draggedSegment : "element"));
        }
    }
    
    /**
     * Handle mouse drag - update positions with free-energy descent
     */
    private void handleMouseDragged(int screenX, int screenY) {
        if (!isDragging || draggedElement == null) return;
        
        EuclidianView view = app.getEuclidianView1();
        if (view == null) return;
        
        double[] coords = view.getFromScreenLocation(screenX, screenY);
        double x = coords[0];
        double y = coords[1];
        
        // Apply free-energy control law: u = -K * ∇ℱ
        double dx = x - dragStartX;
        double dy = y - dragStartY;
        
        // Structural coherence term (smooth motion)
        double u_struct_x = -K * dx;
        double u_struct_y = -K * dy;
        
        // Constraint term (kenotic descent toward constructive value)
        double gradient = computeGradient(draggedSegment, x, y);
        double u_constraint = -K * lambda * gradient;
        
        // Combined control
        double u_x = u_struct_x + u_constraint;
        double u_y = u_struct_y + u_constraint;
        
        // Update element position
        if (draggedElement instanceof GeoPoint) {
            GeoPoint point = (GeoPoint) draggedElement;
            double newX = point.getInhomX() + u_x;
            double newY = point.getInhomY() + u_y;
            point.setCoords(newX, newY, 1.0);
            point.updateRepaint();
        }
        
        // Update glyph vector representation
        updateGlyphVector(draggedSegment, x, y);
        
        // Cascade updates through dependent elements
        renderer.updateAfterDrag();
        
        // Update drag start for next frame
        dragStartX = x;
        dragStartY = y;
        
        // Track energy
        structuralEnergy += Math.abs(u_struct_x) + Math.abs(u_struct_y);
        constraintEnergy += Math.abs(u_constraint);
    }
    
    /**
     * Handle mouse release - end drag
     */
    private void handleMouseReleased() {
        if (isDragging) {
            System.out.println("[DRAG] Released. Energy: struct=" + 
                String.format("%.4f", structuralEnergy) + 
                ", constraint=" + String.format("%.4f", constraintEnergy));
            
            // Check for THUNDERING GRACE lock condition
            if (checkLockCondition()) {
                setRSTLState(RSTLState.ACTUALIZED);
                System.out.println("[THUNDERING GRACE] KENOSIS glyph locked!");
            }
            
            isDragging = false;
            draggedElement = null;
            draggedSegment = null;
            structuralEnergy = 0.0;
            constraintEnergy = 0.0;
        }
    }
    
    /**
     * Find glyph element at coordinates
     */
    private GeoElement findElementAt(double x, double y) {
        // Check all rendered elements
        for (SimpleGlyph.Segment segment : SimpleGlyph.Segment.values()) {
            List<GeoElement> elements = renderer.getSegmentElements(segment);
            for (GeoElement geo : elements) {
                if (geo instanceof GeoPoint) {
                    GeoPoint p = (GeoPoint) geo;
                    double px = p.getInhomX();
                    double py = p.getInhomY();
                    double dist = Math.sqrt((x - px) * (x - px) + (y - py) * (y - py));
                    if (dist < 0.5) { // Hit radius
                        return geo;
                    }
                }
            }
        }
        return null;
    }
    
    /**
     * Compute gradient for free-energy descent
     * Rewards emergence (curve/point motion) and absence
     */
    private double computeGradient(SimpleGlyph.Segment segment, double x, double y) {
        if (currentGlyph == null || segment == null) return 0.0;
        
        SimpleGlyph.Atom atom = currentGlyph.getAtom(segment);
        
        // Kenotic reward: -|emergent|² + α·absence_bonus
        switch (atom) {
            case CURVE:
                // Curve motion is highly emergent - reward
                return -1.0;
            case POINT:
                // Point motion is emergent - reward
                return -0.8;
            case LINE:
                // Line motion generates tension - slight penalty
                return 0.3;
            case ABSENCE:
                // Absence is generative - reward
                return -0.5;
            default:
                return 0.0;
        }
    }
    
    /**
     * Update the glyph's vector representation based on drag
     */
    private void updateGlyphVector(SimpleGlyph.Segment segment, double x, double y) {
        if (currentGlyph == null || segment == null) return;
        
        // The glyph vector is implicitly updated through GeoGebra's
        // dependency graph. Here we track the state change.
        
        // Check if we've reached a stable configuration
        // (This would integrate with TDA persistence in full implementation)
    }
    
    /**
     * Check THUNDERING GRACE lock condition
     * Has the glyph persisted through descent?
     */
    private boolean checkLockCondition() {
        // Simplified: lock achieved if sufficient energy descended
        // Full implementation: 10,000 generation Möbius persistence
        double totalEnergy = structuralEnergy + constraintEnergy;
        return totalEnergy > 10.0 && currentRSTLState == RSTLState.POTENTIAL;
    }
    
    /**
     * Set RSTL state with visual feedback
     */
    private void setRSTLState(RSTLState state) {
        this.currentRSTLState = state;
        
        String stateStr;
        switch (state) {
            case NULL:
                stateStr = "∅ NULL (death)";
                break;
            case POTENTIAL:
                stateStr = "△ POTENTIAL (becoming)";
                break;
            case ACTUALIZED:
                stateStr = "■ ACTUALIZED (glory)";
                break;
            default:
                stateStr = "unknown";
        }
        
        System.out.println("[RSTL] State: " + stateStr);
    }
    
    public void setGlyph(SimpleGlyph glyph) {
        this.currentGlyph = glyph;
        setRSTLState(RSTLState.POTENTIAL);
    }
    
    public RSTLState getRSTLState() {
        return currentRSTLState;
    }
    
    /**
     * Get current free-energy values
     */
    public double getStructuralEnergy() {
        return structuralEnergy;
    }
    
    public double getConstraintEnergy() {
        return constraintEnergy;
    }
    
    public double getTotalEnergy() {
        return structuralEnergy + constraintEnergy;
    }
}
