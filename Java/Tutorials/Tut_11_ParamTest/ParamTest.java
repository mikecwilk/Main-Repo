/*
 * This program demonstrates parameter passing in Java
 * 
 */
public class ParamTest {
	public static void main(String[] args){
		/*
		 * Test 1: Methods cant modify numeric parameters
		 */
		
		System.out.println("Testing tripleValue");
		double percent = 10;
		System.out.println("Before percent = " + percent);
		tripleValue(percent);
		System.out.println("After percent = " + percent);
		
		/*
		 * Test 2: Methods can change state of object parameters
		 */
		
		System.out.println("\nTesting tripleSalary");
		Employee Harry = new Employee("Harry", 50000);
		System.out.println("Before salary = " + Harry.getSalary());
		tripleSalary(Harry);
		System.out.println("After salary = " + Harry.getSalary());
		
		/*
		 * Test 3: Methods can't attach new objects to object parameters
		 */
		System.out.println("\nTesting swap");
		Employee a = new Employee("Alice", 70000);
		Employee b = new Employee("Bob", 60000);
		System.out.println("Before a = " + a.getName());
		System.out.println("Before b = " + b.getName());
		swap(a,b);
		System.out.println("After a = " + a.getName());
		System.out.println("After b = " + b.getName());		
	}
	
	public static void tripleValue(double x){
		x = 3 * x;
		System.out.println("End of method x = " + x);
	}
	
	public static void tripleSalary(Employee x){
		x.raiseSalary(200);
		System.out.println("End of method salary = " + x.getSalary());
	}
	
	public static void swap (Employee x, Employee y){
		Employee temp = x;
		x = y;
		y = temp;
		System.out.println("End of method x = " + x.getName());
		System.out.println("End of method y = " + y.getName());
	}
	
}


class Employee{
	private String name;
	private double salary;
	
	public Employee(String n, double s){
		name = n;
		salary = s;
	}
	
	public String getName(){
		return name;
	}
	
	public double getSalary(){
		return salary;
	}
	
	public void raiseSalary(double byPercent){
		double raise = salary*byPercent/100;
		salary += raise;
	}
}