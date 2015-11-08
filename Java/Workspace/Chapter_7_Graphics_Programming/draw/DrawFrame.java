package draw;

import java.awt.*;
import java.awt.geom.*;
import javax.swing.*;

public class DrawFrame extends JFrame{
	
	public DrawFrame(){
		
		add(new DrawComponent());
		pack();
		
	}

}
