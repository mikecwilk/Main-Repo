package mainframe;

import java.awt.BorderLayout;
import javax.swing.JFrame;

public class MainFrame extends JFrame {
	
	private ButtonPanel buttonPanel;
	private TextPanel textPanel;
	
	public MainFrame(){
		
		
		
		super("Swing Application");
		setLayout(new BorderLayout());
		setSize(500, 500);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		buttonPanel = new ButtonPanel();
		textPanel = new TextPanel();
		
		buttonPanel.setTextPanel(textPanel);
		
		add(buttonPanel, BorderLayout.NORTH);
		add(textPanel, BorderLayout.CENTER);
		
		setVisible(true);

		
	}

}
