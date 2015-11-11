import java.io.*;

public class SerializeDemo {

	public static void main(String [] args){
		Employee e = new Employee();
		
		e.name = "Reyan ALi";
		e.address = "Phokka Kuan, Ambehta Peer";
		e.SSN = 11111;
		e.number = 101;
		
		try {
			FileOutputStream fileOut = new FileOutputStream("p1.dat");
			ObjectOutputStream out = new ObjectOutputStream(fileOut);
			out.writeObject(e);
			out.close();
			fileOut.close();
			System.out.printf("Serialized Data is Saved in p1.dat");
		}catch (IOException i){
			i.printStackTrace();
		}
		
		e.name = "Mike";
		System.out.println(e.name);
		
		try {
			FileOutputStream fileOut = new FileOutputStream("p1.dat");
			ObjectOutputStream out = new ObjectOutputStream(fileOut);
			out.writeObject(e);
			out.close();
			fileOut.close();
			System.out.printf("Serialized Data is Saved in p1.dat");
		}catch (IOException i){
			i.printStackTrace();
		}
		
	}
	
}
