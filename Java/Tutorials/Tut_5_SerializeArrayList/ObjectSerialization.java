import java.io.*;
import java.util.ArrayList;

public class ObjectSerialization {

	public static void main(String[] args){
		File file = new File("p2.dat");
		ArrayList<Student> students = new ArrayList<Student>();
		
		students.add(new Student("Tom", 3.921));
		students.add(new Student("Dave", 100));
		students.add(new Student("Bill", 1));
		
		//Serialize the collection of students
		try{
			FileOutputStream fo = new FileOutputStream(file);
			ObjectOutputStream output = new ObjectOutputStream(fo);
			
			for (Student s: students) {
				output.writeObject(s);
			}
			//Close the output stream and file
			output.close();
			fo.close();
		
			//Catch exceptions	
		}catch(FileNotFoundException e){
			e.printStackTrace();
		}catch(IOException i){
			i.printStackTrace();
		}		
		
	}
}
