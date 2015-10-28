package simpleFrame;

import java.awt.*;
import javax.swing.*;

public class SimpleFrameTest {

	public static void main (String[] args){
		EventQueue.invokeLater(new Runnable(){
			public void run (){
				SimpleFrame frame = new SimpleFrame();
				frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				frame.setVisible(true);
			}
		});
	}
	
}
