package calculator;

import java.awt.EventQueue;
import javax.swing.JFrame;


public class CalculatorTest {
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				JFrame frame = new CalculatorPanel();
				frame.setTitle("Calculator");
				frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				frame.setVisible(true);
			}
		});
	}
}