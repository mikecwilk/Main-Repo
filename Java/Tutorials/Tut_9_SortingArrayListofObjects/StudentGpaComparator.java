import java.util.Comparator;

public class StudentGpaComparator implements Comparator<Students>{
	
	@Override
	
	public int compare(Students s1, Students s2){
		
		double gpa1 = s1.getGpa() * 1000;
		double gpa2 = s2.getGpa() * 1000;
		
		return (int) (gpa2 - gpa1);
		
	}
	
	

}
