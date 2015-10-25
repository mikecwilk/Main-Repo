package abstract_classes;

/*
	This program demonstrates abstract classes
*/

public class PersonTest {
	
	public static void main (String[] args){
		Person[] people = new Person[2];
		
		//fill the people with Student and Employee objects
		people[0] = new Employee("Harry Hacker", 50000, 1989, 10, 1);
		people[1] = new Student("Maria Morris", "computer science");
		
		//print out the names and descriptions of all person objects
		for (Person p: people){
			System.out.println(p.getName() + ", " + p.getDescription()); 
		}
		
	}

}
