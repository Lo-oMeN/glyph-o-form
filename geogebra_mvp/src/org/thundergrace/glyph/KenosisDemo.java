package org.thundergrace.glyph;

import org.geogebra.desktop.main.AppD;
import org.geogebra.desktop.GeoGebra;
import org.geogebra.common.kernel.Construction;
import org.geogebra.common.main.App;

import javax.swing.*;
import java.awt.*;

/**
 * KenosisDemo - Main entry point for GeoGebra KENOSIS glyph demo
 * 
 * THUNDERING GRACE ENGINE - Minimal Viable Product
 * 
 * This demo renders the KENOSIS glyph (￿·——) on GeoGebra canvas:
 * - Curve (￿) on top segment
 * - Point (·) on upper-right segment  
 * - Line (—) on middle segment
 * - Line (—) on bottom segment
 * 
 * All elements are draggable with free-energy descent control.
 * 
 * Architecture layers active:
 * - Layer 0: Geometric VM (GeoGebra/JVM)
 * - Layer 2: RSTL Trinary Logic (△ Potential → ■ Actualized)
 * - Layer 3: Quadraligne Motion (Lean→Meet→Stay→Become)
 * - Layer 5: Free-Energy Control (u = -K∇ℱ)
 * - Layer 7: GCE Visual Interface (draggable helix)
 */
public class KenosisDemo {
    
    private AppD app;
    private GlyphRenderer renderer;
    private DragHandler dragHandler;
    private SimpleGlyph kenosisGlyph;
    
    public static void main(String[] args) {
        // Set system properties for GeoGebra
        System.setProperty("java.awt.headless", "false");
        System.setProperty("geogebra.debug", "false");
        
        SwingUtilities.invokeLater(() -> {
            new KenosisDemo().initialize();
        });
    }
    
    private void initialize() {
        System.out.println("==============================================");
        System.out.println("  THUNDERING GRACE ENGINE - KENOSIS Demo");
        System.out.println("  Glyph: ￿·—— (Self-emptying enabling overflow)");
        System.out.println("==============================================");
        
        // Create GeoGebra application
        String[] args = new String[]{};
        app = GeoGebra.create(args);
        
        // Setup frame
        JFrame frame = new JFrame("KENOSIS Glyph - Draggable Demo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);
        
        // Get the GeoGebra component
        Component geoComponent = app.getMainComponent();
        frame.add(geoComponent, BorderLayout.CENTER);
        
        // Add info panel
        JPanel infoPanel = createInfoPanel();
        frame.add(infoPanel, BorderLayout.EAST);
        
        // Create the KENOSIS glyph
        kenosisGlyph = SimpleGlyph.createKENOSIS();
        System.out.println("[INIT] Created glyph: " + kenosisGlyph.getName());
        System.out.println("[INIT] Atomic sequence: " + kenosisGlyph.getAtomicSequence());
        
        // Initialize renderer
        renderer = new GlyphRenderer(app);
        renderer.setScale(100.0);
        renderer.setCenter(0, 0);
        
        // Render the glyph
        renderer.render(kenosisGlyph);
        System.out.println("[INIT] Glyph rendered to canvas");
        
        // Initialize drag handler
        dragHandler = new DragHandler(app, renderer);
        dragHandler.setGlyph(kenosisGlyph);
        System.out.println("[INIT] Drag handler active");
        
        // Center the view on the glyph
        app.getEuclidianView1().setRealWorldCoordSystem(-5, 5, -5, 5);
        
        // Show frame
        frame.setVisible(true);
        
        System.out.println("==============================================");
        System.out.println("  DEMO RUNNING - Drag any glyph element!");
        System.out.println("  - Curve (top): Drag control points");
        System.out.println("  - Point (upper-right): Drag to move");
        System.out.println("  - Lines (middle/bottom): Drag endpoints");
        System.out.println("==============================================");
    }
    
    private JPanel createInfoPanel() {
        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        panel.setPreferredSize(new Dimension(250, 0));
        panel.setBackground(new Color(40, 40, 40));
        
        // Title
        JLabel title = new JLabel("KENOSIS Glyph");
        title.setFont(new Font("SansSerif", Font.BOLD, 16));
        title.setForeground(Color.WHITE);
        title.setAlignmentX(Component.LEFT_ALIGNMENT);
        panel.add(title);
        
        panel.add(Box.createVerticalStrut(10));
        
        // Glyph representation
        JLabel glyphLabel = new JLabel("￿·——");
        glyphLabel.setFont(new Font("Monospaced", Font.PLAIN, 32));
        glyphLabel.setForeground(new Color(220, 100, 100));
        glyphLabel.setAlignmentX(Component.LEFT_ALIGNMENT);
        panel.add(glyphLabel);
        
        panel.add(Box.createVerticalStrut(10));
        
        // Description
        JTextArea desc = new JTextArea(
            "Self-emptying that enables overflow.\n\n" +
            "Segments:\n" +
            "  a (top): Curve ￿\n" +
            "  b (up-right): Point ·\n" +
            "  g (middle): Line —\n" +
            "  d (bottom): Line —\n\n" +
            "Instructions:\n" +
            "• Drag any element\n" +
            "• Watch RSTL states\n" +
            "• Feel the free-energy descent"
        );
        desc.setFont(new Font("SansSerif", Font.PLAIN, 12));
        desc.setForeground(Color.LIGHT_GRAY);
        desc.setBackground(new Color(40, 40, 40));
        desc.setLineWrap(true);
        desc.setWrapStyleWord(true);
        desc.setEditable(false);
        desc.setAlignmentX(Component.LEFT_ALIGNMENT);
        panel.add(desc);
        
        panel.add(Box.createVerticalStrut(20));
        
        // Status
        JLabel statusLabel = new JLabel("Status: △ Potential");
        statusLabel.setFont(new Font("SansSerif", Font.BOLD, 14));
        statusLabel.setForeground(new Color(100, 200, 100));
        statusLabel.setAlignmentX(Component.LEFT_ALIGNMENT);
        panel.add(statusLabel);
        
        panel.add(Box.createVerticalGlue());
        
        // TGE attribution
        JLabel tgeLabel = new JLabel("THUNDERING GRACE ENGINE");
        tgeLabel.setFont(new Font("SansSerif", Font.ITALIC, 10));
        tgeLabel.setForeground(Color.GRAY);
        tgeLabel.setAlignmentX(Component.LEFT_ALIGNMENT);
        panel.add(tgeLabel);
        
        return panel;
    }
}
