import java.util.ArrayList;

public class Customer {
	
	
	private String name;
	private String id; 	//3 digits string
	private String pin; //4 digits string
	private ArrayList <Account> acct;
//	private double total_bal; //for all accounts
	public static int total_customers;
	public int total;
	
	public Customer(String new_name, String new_id, String new_pin) { //Constructor
		acct = new ArrayList<>(100);
		this.name = new_name;
		this.id = new_id;
		this.pin = new_pin;
		
	}
	
	void info(){
		System.out.println("\n**Customer Created**");		
		System.out.println("Customer Name: " + this.name);
		System.out.println("Customer pin: " + this.pin);
		System.out.println("Customer ID: " + this.id);
		System.out.println("Total Customers: " + total_customers);		
		
	}
	
	String validatePin(){
		
		return this.pin;
		
	}
	
	void validateAccount(String account, double deposit){
		boolean dep = false;
		for (int i = 0; i < this.total; i++){

			if((this.acct.get(i).getNumber()).equals(account)){
				this.acct.get(i).addDeposit(deposit);
				dep = true;
				break;
			}
			
		} 
		if (!dep){
			System.out.println("Account " + account + " Does not Exist!");
		}
	}
	
	void checkAccount(String account){
		boolean check = false;
		for (int i = 0; i < this.total; i++){

			if((this.acct.get(i).getNumber()).equals(account)){
				System.out.println("\nAccount Owner's Name: " + this.name);
				System.out.println("Account Owner's ID Number " + this.id);
				this.acct.get(i).check_balance();
				check = true;
				break;
			}
			
		} 
		if (!check){
			System.out.println("Account " + account + " Does not Exist!");
		}
	}
	
	void addAccount(int Account_Number){
		Account new_account = new Account(Account_Number, total_customers);
		System.out.println("\n**Account Created**");
		new_account.info();
		this.acct.add(total, new_account);
		total_customers += 1;

	}
	

	
	public double cal_total_bal()  { //different than the stuff given by instructor

		return 0;
	}
	
}
