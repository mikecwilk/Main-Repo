package action;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class ActionFrame extends JFrame {
	
	private JPanel buttonPanel;
	private static final int DEFAULT_WIDTH = 300;
	private static final int DEFAULT_HEIGHT = 200;
	
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				JFrame frame = new ActionFrame();
				frame.setTitle("ActionTest");
				frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				frame.setVisible(true);
				frame.setSize(300, 300);
			}
		});
	}
	
	public ActionFrame(){
		
		buttonPanel = new JPanel ();
		
		//define actions
		Action yellowAction = new ColorAction("Yellow", new ImageIcon("yellow-ball.gif"), Color.YELLOW);
		Action blueAction = new ColorAction("Blue", new ImageIcon("blueball.gif"), Color.BLUE);
		Action redAction = new ColorAction("Red", new ImageIcon("redball.gif"), Color.RED);
		
		//add buttons for these actions
		buttonPanel.add(new JButton(yellowAction));
		buttonPanel.add(new JButton(blueAction));
		buttonPanel.add(new JButton(redAction));
		
		//add panel to frame
		add(buttonPanel);
		
		//associate the Y, B, and R keys with names
		InputMap imap = buttonPanel.getInputMap(JComponent.WHEN_ANCESTOR_OF_FOCUSED_COMPONENT);
		imap.put(KeyStroke.getKeyStroke("ctrl Y"), "panel.yellow");
		imap.put(KeyStroke.getKeyStroke("ctrl B"), "panel.blue");
		imap.put(KeyStroke.getKeyStroke("ctrl R"), "panel.red");
		
		//associate the names with action
		ActionMap amap = buttonPanel.getActionMap();
		amap.put("panel.yellow", yellowAction);
		amap.put("panel.blue", blueAction);
		amap.put("panel.red", redAction);
		
	}
	
	public class ColorAction extends AbstractAction{

		/*
		 * 
		 * Constructs a color action
		 * 
		 */
		
		public ColorAction(String name, Icon icon, Color c){
			
			putValue(Action.NAME, name);
			putValue(Action.SMALL_ICON, icon);
			putValue(Action.SHORT_DESCRIPTION, "Set panel color to " + name.toLowerCase());
			putValue("color", c);
			
		}
		
		public void actionPerformed(ActionEvent event){
			Color c = (Color) getValue("color");
			buttonPanel.setBackground(c);
		}
		
	}
	
}
