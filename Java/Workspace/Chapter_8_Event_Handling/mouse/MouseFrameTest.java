package mouse;

import java.awt.EventQueue;
import javax.swing.JFrame;

public class MouseFrameTest {
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				JFrame frame = new MouseFrame();
				frame.setTitle("MouseFrame");
				frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				frame.setVisible(true);
			}
		});
	}
}