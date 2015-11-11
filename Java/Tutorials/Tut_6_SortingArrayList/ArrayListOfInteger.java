import java.util.*;
public class ArrayListOfInteger  {

	public static void main(String args[]){
	   ArrayList<Integer> arraylist = new ArrayList<Integer>();
	   arraylist.add(11);
	   arraylist.add(2);
	   arraylist.add(7);
	   arraylist.add(3);
	   /* ArrayList before the sorting*/
	   System.out.println("Before Sorting:");
	   for(int counter: arraylist){
			System.out.println(counter);
		}

	   /* Sorting of arraylist using Collections.sort*/
	   Collections.sort(arraylist);

	   /* ArrayList after sorting*/
	   System.out.println("After Sorting:");
	   for(int counter: arraylist){
			System.out.println(counter);
		}
	}
}