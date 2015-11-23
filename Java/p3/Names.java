
public class Names {
	int ID;
	String name;
	
	Names(int new_ID, String new_name){
		
		this.ID = new_ID;
		this.name = new_name;
		
	}
	
	public void printInfo(){
		System.out.println(name +" has ID " + ID);
	}
}
