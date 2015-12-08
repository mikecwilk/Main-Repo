
public class Factorial {

	//return n!
	//prcondition n >=0 and n <= 20
	
	public static long factorial(long n){
		System.out.println("factorial: " + n);
		if 				(n < 0) throw new RuntimeException("Underflow error in factorial");
		else if 		(n > 20) throw new RuntimeException("Overflow error in factorial");
		else if 		(n == 0) return 1;
		else 			return n * factorial(n - 1);
	}
	
	public static void main(String[] args) {
		System.out.println(factorial(5));
	}
	
}
