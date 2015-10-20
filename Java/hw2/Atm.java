import java.util.ArrayList;

public class Atm {

	private ArrayList<Customer>cust;
	private int starting_account_number;
	private int starting_customer_number;
//	private String admin_pin;
//	private int interest_rate;
//	private int transaction_counter;
	
	public Atm() {//constructor

		cust = new ArrayList<>(100);
		starting_account_number = 1001;
	    starting_customer_number = 101;
//	    admin_pin = "abcd";
//	    interest_rate = 5;
//	    transaction_counter = 0;

		
	}
	
	public void create_customer(String NAME, String PIN){
		int array = starting_customer_number - 101;
		String ID;
		//Prompt for customer name and 4 digit/char PIN (Done in hw2.java)
			
		//Generate a customer ID
		ID = String.valueOf(starting_customer_number);
		
		//Add new customer to array list
		Customer new_cust = new Customer(NAME, ID, PIN);
		new_cust.info();
		
		starting_customer_number += 1;
		cust.add(array, new_cust);
		
		

		
	}
	
	public void open_account(String ID, String PIN){
		int int_ID = Integer.parseInt(ID) - 101;
		
		//Check for Existence of Customers
		if (starting_customer_number == 101){ 
			System.out.println("No Customers Created Yet!");
			return;
		}
		
		//Check for Existence of Entered Customer ID
		if (Customer.total_customers < int_ID || int_ID < 0){
			System.out.println("That Customer Does Not Exist!");
			return;
		}
		
		//Check if the entered customer PIN matches the PIN stored for that customer if so create a new account 
		if (cust.get(int_ID).validatePin().equals(PIN)) {
			System.out.println("Pin number validated");
			cust.get(int_ID).addAccount(starting_account_number);
			starting_account_number += 1;
			cust.get(int_ID).total += 1;
			
		//If the ID is not a match state this and return to main menu	
		}else if(!(cust.get(int_ID).validatePin().equals(PIN))){
			System.out.println("Pin number does not match ID");
		}
		

		//Get customer ID and pin to login +
		//Validate user information +
		//Generate an account number add to acct array list 
		//Display account information
	
	}
	
	boolean deposit(String ID, String PIN, boolean validated, double deposit, String account){
		int int_ID = Integer.parseInt(ID) - 101;
		
    	//Check for Existence of Customers
		if (starting_customer_number == 101){ 
			System.out.println("No Customers Created Yet!");
			return false;
		}    
		
		//Check for Existence of Entered Customer ID
		if (Customer.total_customers < int_ID || int_ID < 0){
			System.out.println("That Customer Does Not Exist!");
			return false;
		}
		
		//Check for PIN validation
		if (!validated){
			if (cust.get(int_ID).validatePin().equals(PIN)) {
				System.out.println("Pin number validated");
				System.out.println("\nHow much would you like to deposit?");
				System.out.print("==> ");
				return true;
			}
		}else{
			
			cust.get(int_ID).validateAccount(account, deposit);
			
			
		}
		//- Get customer ID and pin to login.
		//- Validate user information.
		//- Get the deposit amount.
		//- Update the balance.
		//- Display account information.
		return true;
		
	}
	
	public void withdraw(){
		

	//- Get customer ID and pin to login.
	//- Validate user information.
	//- Get the withdraw amount.
	//- Validate and update balance
	//- Display account information.
	}
/*	
	Transfer
	- Get customer ID and pin to login.
	- Validate user information.
	- Get the transfer amount.
	- Validate and update balance on both accounts.
	- Display account information.
*/
	
	boolean get_balance(String ID, String PIN, boolean validated, String account){
		int int_ID = Integer.parseInt(ID) - 101;
		if (!validated){
			if (cust.get(int_ID).validatePin().equals(PIN)) {
				System.out.println("Pin number validated");
				
			}else if(!cust.get(int_ID).validatePin().equals(PIN)){
				System.out.println("Pin number does not match ID");
				return false;
			}
		}else{
			
			cust.get(int_ID).checkAccount(account);
			return true;
			
		}
		//Get customer ID and pin to login
		//Validate user information
		//Display User information
		return true;
		
	}
	
/*
 	Close account
	- Get customer ID and pin to login.
	- Validate user information.
	- Clear out account information for this customer.

 */
	
	
}

/*
Notes:
-	PIN is a 4 digit character string.
-	Both Customer ID and account # are “system” generated.  ID starts with 101 and Account # starts with 1001 (Hint: add a public static attribute in both Customer and Account)
-	You should not make any changes to ConsoleReader.java file.
-	You need to submit 5 files: 4 *.java files and hw2.readme.
-	Print the appropriate error message when necessary.
-	Make sure there are plenty of comments in the code.
-	You should have a log-in method inside Atm to prompt for customer ID and pin.
-	You should have a validate_ID_PW method inside Atm to validate the ID and pin from the customer array-list.
*/
