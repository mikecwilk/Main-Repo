package mainframe;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JPanel;

public class ButtonPanel extends JPanel implements ActionListener{
	
	private JButton helloButton;
	private JButton exitButton;
	private TextPanel textPanel;
	
	public ButtonPanel(){
		
		setLayout(new FlowLayout());
		
		helloButton = new JButton("Hello");
		exitButton = new JButton("Exit");
		
		helloButton.addActionListener(this);
		exitButton.addActionListener(this);
		
		
		//add the buttons to the panel
		add(helloButton);
		add(exitButton);
		
	}
	
	public void setTextPanel(TextPanel textPanel) {
		
		this.textPanel = textPanel;
		
	}
	
	@Override
	public void actionPerformed(ActionEvent e) {
		JButton buttonPressed = (JButton) e.getSource();
		
		if (buttonPressed.equals(helloButton)){
			textPanel.addTextToPanel("Hello\n");
		}
		
		else{
			
			System.exit(0);
			
		}
	}

}
