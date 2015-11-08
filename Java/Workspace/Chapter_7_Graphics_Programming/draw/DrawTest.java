package draw;

import java.awt.*;
import java.awt.geom.*;
import javax.swing.*;

public class DrawTest {
	
	public static void main(String[] args){
		
		EventQueue.invokeLater(new Runnable(){
			public void run(){
				JFrame frame = new DrawFrame();
				frame.setTitle("DrawTest");
				frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				frame.setVisible(true);
			}
		});
		
		
		
	}

}
