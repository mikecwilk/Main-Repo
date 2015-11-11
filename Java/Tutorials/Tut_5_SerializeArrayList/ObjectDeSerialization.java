import java.io.*;

import java.util.ArrayList;


public class ObjectDeSerialization {

	public static void main(String [] args) throws ClassNotFoundException{
		File file = new File("p2.dat");
		ArrayList<Student> students = new ArrayList<Student>();
		
		try{
			
			FileInputStream fi = new FileInputStream(file);
			ObjectInputStream input = new ObjectInputStream(fi);
			
		try{
			while (true){
				Student s = (Student)input.readObject();
				students.add(s);
			}
			
			}catch (EOFException ex){
			
			}
	
		}catch(FileNotFoundException f){
			f.printStackTrace();
		}catch(IOException f){
			f.printStackTrace();
		}catch(ClassNotFoundException f){
			f.printStackTrace();
		}
		
		for (Student s: students) {
			System.out.println(s);
			s.getName();
			s.getGpa();
		}
		
	}
}