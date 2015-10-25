package abstract_classes;

public class Student extends Person{
	
	private String major;
	
	public Student(String n, String m){
		super(n); //Pass n to the superclass constructor
		major = m;
	}
	
	public String getDescription(){
		
		return "a student majoring in " + major;
		
	}

}
