package mouse;

import javax.swing.*;

/**
 * A frame containing a panel for testing mouse operations
 */
public class MouseFrame extends JFrame {
	
	private static final int DEFAULT_WIDTH = 300;
	private static final int DEFAULT_HEIGHT = 200;
	public MouseFrame() {

		add(new MouseComponent());
		setSize(DEFAULT_WIDTH, DEFAULT_HEIGHT);
		//pack();
	}
}