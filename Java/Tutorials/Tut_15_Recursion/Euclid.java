
public class Euclid {
	//recursive implementation
	
	public static int gcd(int p, int q){
		System.out.println("Recursive: " + q);
		
		if (q == 0) return p;
		else return gcd(q, p % q);
	}
	
	public static int gcd2(int p, int q) {
		while (q != 0){
			System.out.println("Non-Recursive: " + q);
		
			int temp = q;
			q = p % q;
			p = temp;
		}
		return p;
	}
	
	
	 public static void main(String[] args) {
		 
		 System.out.println(gcd (15, 85));
		 
		 System.out.println();
		 System.out.println(gcd2(15, 85));
		 
		 
	 }
}
