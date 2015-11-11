import java.util.ArrayList;
import java.util.Collections;

public class SortingSearchingStudentsUsingComparator {
	
	public static void main(String[] args){
		//ArrayLists are dynamic collections of objects (reference types only)
		ArrayList<Students> psy101 = new ArrayList<Students>();
		
		psy101.add(new Students("Sally", 4.0));
		psy101.add(new Students("Dave", 3.6));
		psy101.add(new Students("Alice", 3.15));
		
		printStudents(psy101);
		
		System.out.println("SORT BY NAME");
		Collections.sort(psy101, new StudentNameComparator());
		
		printStudents(psy101);
		
		System.out.println("SORT BY GPA");
		Collections.sort(psy101, new StudentGpaComparator());
		printStudents(psy101);
		
	}
	
	public static void printStudents(ArrayList<Students> students){
		System.out.printf("Student\tGPA\n");
		for (Students s : students) {
			System.out.println(s.getName() + "\t" + s.getGpa());


		}
		System.out.println();
	}

}
