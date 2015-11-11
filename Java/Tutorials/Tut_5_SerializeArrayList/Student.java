
public class Student implements java.io.Serializable {

	private String name;
	private double gpa;
	
	public Student(String name, double gpa) {
		this.name = name;
		this.gpa = gpa;
	}

	void getName(){
		System.out.println(this.name);
	}
	void getGpa(){
		System.out.println(this.gpa);
	}
}





