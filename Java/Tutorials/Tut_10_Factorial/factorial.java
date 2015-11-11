
public class factorial {
	 public static void main(String[] args){
		 
		 int factorial = 1;
		 int n = 5;
		 
		 for (int i = n; i > 1; i--){
			 System.out.println(factorial + " " +i);
			 
			 factorial = (i)*(factorial);
			 //System.out.println(factorial);
		 }
		 
		 System.out.println(factorial);
	 }
}
