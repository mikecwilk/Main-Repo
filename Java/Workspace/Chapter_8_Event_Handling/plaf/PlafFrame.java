package plaf;

import java.awt.EventQueue;
import java.awt.event.*;
import javax.swing.*;


/**
 * A frame with a button panel for changing look-and-feel
 */
public class PlafFrame extends JFrame {
	
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				JFrame frame = new PlafFrame();
				frame.setTitle("Plaf");
				frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				frame.setVisible(true);
			}
		});
	}
		
	
	private JPanel buttonPanel;

	public PlafFrame() {
		buttonPanel = new JPanel();

		UIManager.LookAndFeelInfo[] infos = UIManager.getInstalledLookAndFeels();
		for (UIManager.LookAndFeelInfo info : infos)
			makeButton(info.getName(), info.getClassName());

		add(buttonPanel);
		pack();
	}

	/**
	 * Makes a button to change the pluggable look-and-feel.
	 * 
	 * @param name
	 *            the button name
	 * @param plafName
	 *            the name of the look-and-feel class
	 */
	void makeButton(String name, final String plafName) {
		// add button to panel

		JButton button = new JButton(name);
		buttonPanel.add(button);

		// set button action

		button.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent event) {
				// button action: switch to the new look-and-feel
				try {
					UIManager.setLookAndFeel(plafName);
					SwingUtilities.updateComponentTreeUI(PlafFrame.this);
					pack();
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
}