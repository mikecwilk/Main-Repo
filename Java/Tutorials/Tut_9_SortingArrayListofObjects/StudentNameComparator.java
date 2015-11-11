import java.util.Comparator;

public class StudentNameComparator implements Comparator<Students> {
	@Override
	public int compare(Students s1, Students s2){

		
		return s1.getName().compareToIgnoreCase(s2.getName());
	}
	
	

}
