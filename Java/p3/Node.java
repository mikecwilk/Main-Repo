import java.util.ArrayList;

public class Node {
	int original_ID;
	String original_name;
	ArrayList<Names> names = new ArrayList<Names>();
	int total_names; 
	
	
	Node leftChild;
	Node rightChild;
	
	Node(int ID, String name){
		this.original_ID = ID;
		this.original_name = name;
		total_names = 0;
	}
	
	public String toString(){
		return original_name + " is at ID: " + original_ID;
	}
	
	public void addName(int new_ID, String new_name){
		Names name = new Names(new_ID, new_name);
		names.add(total_names, name);
		total_names += 1;
	}
	
	public void printNames(){
		for(Names e: names){
			e.printInfo();
		}
	}
	
}


