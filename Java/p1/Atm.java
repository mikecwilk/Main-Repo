import java.io.EOFException;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Collections;

////////////////////////////////////////////////////////////////////////////////
//				   Class Admin Used for Easier Sorting						  //
////////////////////////////////////////////////////////////////////////////////

class Admin{
	private String Customer_Name;
	private String Customer_ID;
	private String Account_ID;
	private String PIN;
	private double balance;
	private boolean active;
	


	public Admin(String Customer_Name, String Customer_ID, String Account_ID, String PIN, double balance, boolean active){
		this.Customer_Name = Customer_Name;
		this.Customer_ID = Customer_ID;
		this.Account_ID = Account_ID;
		this.PIN = PIN;
		this.balance = balance;
		this.active = active;
	}
	
	public void info(){
		double rounded;
		rounded = round(this.balance, 2);
		if (this.Customer_Name.length() < 8){
			System.out.println(this.Customer_Name + "\t\t" + this.Customer_ID + "\t\t" + this.Account_ID + "\t\t" + this.PIN + "\t\t$" + rounded);
		}else{
			System.out.println(this.Customer_Name + "\t" + this.Customer_ID + "\t\t" + this.Account_ID + "\t\t" + this.PIN + "\t\t$" + rounded);
		}
		}
	
	public String getName(){
		return Customer_Name;
	}
	
	public double getBalance(){
		return balance;
	}
	
	public boolean getActive(){
		return active;
	}
	
	public double getAccount_ID(){
		double dbl_Account_ID = Double.parseDouble(this.Account_ID);
		return dbl_Account_ID;
		
	}
	
	public static double round(double value, int places) {
	    if (places < 0) throw new IllegalArgumentException();

	    BigDecimal bd = new BigDecimal(value);
	    bd = bd.setScale(places, RoundingMode.HALF_UP);
	    return bd.doubleValue();
	}
}

////////////////////////////////////////////////////////////////////////////////
//						Persistent ATM Class						 		  //
////////////////////////////////////////////////////////////////////////////////

public class Atm {
	
	//Create a file object for p1.dat
	ConsoleReader console2 = new ConsoleReader(System.in);  
	File file = new File("p1.dat");
	

//This Method is a Simple Check To Whether A String is Numeric or Not	
	public static boolean isNumeric(String str)  {  
		  try  {  
			  double d = Double.parseDouble(str);  
		  }  
		  catch(NumberFormatException nfe)  {  
		    return false;  
		  }  
		  return true;  
		}
	private ArrayList<Customer>cust = new ArrayList<Customer>();
	private int starting_account_number;
	private int starting_customer_number;

	
	public Atm() {//constructor
		cust = new ArrayList<>(100);
		
		int i = 0;
		int j = 0;
		int k = 0;
		this.readFromFile();

		
////////////////////////////////////////////////////////////////////////////////
//					Initialize Variables for Customer Class				      //
////////////////////////////////////////////////////////////////////////////////
				
		for(Customer e: cust){

//*****DEBUG*****	
//			System.out.println("\n");
//			System.out.println(e);
//			e.info();
//*****DEBUG*****	
			i +=1;
			j = j + e.getAccountNum();
			k = k + e.getTransactions();
		}
//*****DEBUG*****	
//		System.out.println("\ntotal accounts: " + j);
//		System.out.println("total transactions: " + k);
//*****DEBUG*****	
		
		starting_account_number =  1001 + j;
	    starting_customer_number = 101 + i;
	    Customer.total_customers = i;
	    Customer.total_accounts = j;
	    Customer.total_transactions = k;
		
	}
	

////////////////////////////////////////////////////////////////////////////////
//						Common ATM Class Methods				      		  //
////////////////////////////////////////////////////////////////////////////////	

	
//This Method Creates a New Customer Object and Adds it to The Array List
	public void create_customer(String NAME, String PIN){
		int array = starting_customer_number - 101;
		String ID;
			
		//Generate a customer ID
		ID = String.valueOf(starting_customer_number);
		
		//Add new customer to array list
		Customer new_cust = new Customer(NAME, ID, PIN);
		System.out.println("\n**Customer Created**");
		new_cust.info();
		
				
		starting_customer_number += 1;
		Customer.total_transactions += 1;
		Customer.total_customers += 1;
		if(Customer.total_transactions %5 == 0){
			System.out.println("\nAdding interest to savings accounts!");
			this.addInterest();
		}
		cust.add(array, new_cust);
		System.out.println("Total Transactions " + Customer.total_transactions);
		this.writeToFile();
		
	}

//This Method is Used Throughout the Program to Verify Account ID and PIN Information
	int login(){
    	String ID = "";
    	String PIN = "";
    	int n = 0; //This will represent the location in the arrayList the cust is found at
    	
    	System.out.println("\nPlease Enter Your 3 Digit ID Number");
		System.out.print("==> ");
		ID = console2.readLine();
		
		for (Customer c: cust){
			//DEBUG System.out.println(n);
			n++;
			if (ID.equals(c.getId())){
				System.out.println("\nPlease Enter Your 4 digit PIN (characters are not allowed)");
				System.out.print("==> ");
				PIN = console2.readLine();
				
				if (PIN.equals(c.getPin())){
					System.out.println("PIN Validated");
					return n - 1;
				} else {
					System.out.println("Incorrect PIN!");
					return -1;
				}
				
			
			}
		}
		System.out.println("Customer Does not Exist!");
		return -1;
	}

//This Method Creates a New Account Object For a Customer and Adds it to The Corresponding ArrayList
	void open_account(int ID){
       	String account_type = "";
       	
       	System.out.println("\nWill this be a [S]avings or [C]hecking account?");
       	System.out.print("==> ");
		account_type = console2.readLine();
		

		if (account_type.equalsIgnoreCase("C") || account_type.equalsIgnoreCase("Checking")){
			cust.get(ID).addAccountChecking(starting_account_number);
			starting_account_number += 1;
			Customer.total_transactions += 1;
			if(Customer.total_transactions %5 == 0){
				System.out.println("\nAdding interest to savings accounts!");
				this.addInterest();
			}
			System.out.println(Customer.total_transactions);
			this.writeToFile();
			cust.get(ID).getTotal();
		}else if(account_type.equalsIgnoreCase("Savings") || account_type.equalsIgnoreCase("S")){
			cust.get(ID).addAccountSaving(starting_account_number);
			System.out.println("Interest Rate is set to: 5%");
			starting_account_number += 1;
			Customer.total_transactions += 1;
			if(Customer.total_transactions %5 == 0){
				System.out.println("\nAdding interest to savings accounts!");
				this.addInterest();
			}
			System.out.println("Total Transactions " + Customer.total_transactions);
			this.writeToFile();
			cust.get(ID).getTotal();
		}else{
			System.out.println("\nThat is not a type of account!");
			
		}
	
	}

//This Method Deposits Money to a Customers Account by Updating That Accounts Balance
	void deposit(int ID){
		String account = "";
		String deposit = "";
		
		cust.get(ID).listAccounts();
    	System.out.println("\nSelect an account");
		System.out.print("==> ");
		account = console2.readLine();
		
		if (isNumeric(account)){
		
	    	System.out.println("\nEnter the Amount you want to deposit");
			System.out.print("==> ");
			deposit = console2.readLine();
		
			if(isNumeric(deposit)){
				cust.get(ID).validateAccount(account, deposit);
				//Debug to keep track of transactions
				System.out.println("Total Transactions " + Customer.total_transactions);
				if(Customer.total_transactions %5 == 0){
					System.out.println("\nAdding interest to savings accounts!");
					this.addInterest();
				}
				
			}else{
				System.out.println("\nDeposit Amounts Must Be Numeric!");
			}
		}else{
			System.out.println("\nAccounts Must Be Numeric!");
		}
		
		this.writeToFile();
		
	}

//This Method Withdraws Money From a Customers Account by Updating That Accounts Balance
	public void withdraw(int ID){
		String account = "";
		String withdraw = "";
		
		cust.get(ID).listAccounts();
    	System.out.println("\nSelect an account to withdraw from");
		System.out.print("==> ");
		account = console2.readLine();
		

		if (isNumeric(account) ){
			
		    System.out.println("\nEnter the Amount you want to withdraw");
			System.out.print("==> ");
			withdraw = console2.readLine();
			
			if(isNumeric(withdraw)){
				cust.get(ID).validateAccountWithdraw(account, withdraw);
				//cust.get(ID).addTransaction();
				//Debug to keep track of transactions
				System.out.println("Total Transactions " + Customer.total_transactions);
				if(Customer.total_transactions %5 == 0){
					System.out.println("\nAdding interest to savings accounts!");
					this.addInterest();
				}
			}else{
				System.out.println("\nWithdraw Amounts Must Be Numeric!");
			}
						
		}else{
			System.out.println("\nAccounts Must Be Numeric!");
		}
		this.writeToFile();


	}

//This Method Deposits Money to a Customers Account and Withdraws Money From an Account then Updates The Account Balances
	public void transfer(int ID){
		String account_to = "";
		String account_from = "";
		
		String transfer_amount = "";
		
		cust.get(ID).listAccounts();
    	System.out.println("\nSelect an account to transfer funds *from*");
		System.out.print("==> ");
		account_from = console2.readLine();
		
		if(isNumeric(account_from)){
			
			if(cust.get(ID).validateAccountToFrom(account_from)){
				
		    	System.out.println("\nSelect an account to transfer funds *to*");
				System.out.print("==> ");
				account_to = console2.readLine();
				
				if(isNumeric(account_to)){
					
				
					if(cust.get(ID).validateAccountToFrom(account_to)){
				
						System.out.println("\nEnter The Amount You Want to Transfer");
						System.out.print("==> ");
						transfer_amount = console2.readLine();
						
						if(isNumeric(transfer_amount)){
							if(cust.get(ID).checkAmount(account_from, transfer_amount)){
							
								cust.get(ID).makeTransfer(account_from, account_to, transfer_amount);
								Customer.total_transactions += 1;
								//cust.get(ID).addTransaction();
								//Debug to keep track of transactions
								System.out.println("Total Transactions " + Customer.total_transactions);
								if(Customer.total_transactions %5 == 0){
									System.out.println("\nAdding interest to savings accounts!");
									this.addInterest();
								}
							
								
							
							}else{
								System.out.println("Insufficient funds in account!");
							}
						}else{
							System.out.println("\nTransfer Amount Must Be Numeric!");
						}
					}
					
				}else{
					System.out.println("\nAccounts Must Be Numeric!");
				}
					
					
			}else{
				//System.out.println("\nAccount Does Not Exist For This User!");
			}
			
		}else{
			System.out.println("\nAccounts Must Be Numeric!");
		}
		
		this.writeToFile();
	}

//This Method Gets The Balances for A Specific Customer
	boolean get_balance(int ID){
    
	
		cust.get(ID).checkBalances();
	
		return true;
				
	}
	
//This Method Closes an Account by Setting the Account Active Parameter to False for the Specific Account 
 	public void close_account(int ID){
 		
 		String account = "";
 		cust.get(ID).listAccounts();
    	System.out.println("\nSelect an account to close");
		System.out.print("==> ");
		account = console2.readLine();
		
		cust.get(ID).closeAccount(account);
		Customer.total_transactions += 1;
		if(Customer.total_transactions %5 == 0){
			System.out.println("\nAdding interest to savings accounts!");
			this.addInterest();
		}
		System.out.println("Total Transactions " + Customer.total_transactions);
		this.writeToFile();

 	}

 //This Method Loops Through All the Customers and Adds Interest to Their Savings Accounts
 	public void addInterest(){
 		
 		for(Customer e: cust){
 			e.addInterest();
 		}
 		
 	}

////////////////////////////////////////////////////////////////////////////////
//							Persistent File IO				      		 	  //
////////////////////////////////////////////////////////////////////////////////
 	
 	public void readFromFile(){
try{
			
			FileInputStream fi = new FileInputStream(file);
			ObjectInputStream input = new ObjectInputStream(fi);
			
		try{
			while (true){
				Customer s = (Customer)input.readObject();
				cust.add(s);
			}
			
			}catch (EOFException ex){
			
			}

		}catch(FileNotFoundException g){
			System.out.println("File Not Found Creating p1.dat file");
			try{
			file.createNewFile();
			}catch (IOException t){
				t.printStackTrace();
			}
			
		}catch(IOException h){
			h.printStackTrace();
		}catch(ClassNotFoundException f){
			f.printStackTrace();
		}
 	}
	public void writeToFile(){
		try{
			FileOutputStream fo = new FileOutputStream(file);
			ObjectOutputStream output = new ObjectOutputStream(fo);
			//DEBUG
			//System.out.println("\nwriting");
			
			for (Customer s: cust) {
				output.writeObject(s);
			}
			//Close the output stream and file
			output.close();
			fo.close();
		
			//Catch exceptions	
		}catch(FileNotFoundException e){
			e.printStackTrace();
		}catch(IOException i){
			i.printStackTrace();
		}
	}

////////////////////////////////////////////////////////////////////////////////
//					Administrative Sorting Methods				      		  //
////////////////////////////////////////////////////////////////////////////////

	
//This Method Rounds Doubles To a Desired Number of Places 
	public static double round(double value, int places) {
	    if (places < 0) throw new IllegalArgumentException();

	    BigDecimal bd = new BigDecimal(value);
	    bd = bd.setScale(places, RoundingMode.HALF_UP);
	    return bd.doubleValue();
	}

//This Method Prints a List of All Accounts w/ Info Sorted by Customer Name
	public void adminNames(){
		int p = 0;
		int l = 0;
		
		ArrayList<Admin>new_admin = new ArrayList<Admin>();
		System.out.println("[Name]\t\t[Cust ID]\t[Acct ID]\t[Pin #]\t\t[Balance]");
		for (Customer c: cust){
			for (int i = 0; i < c.getAccountNum(); i++){
				String Customer_Name = c.getName();
				String Customer_ID = c.getId();
				String Account_ID = c.getAccountArray(i).getNumber();
				String PIN = c.getPin();
				double balance = c.getAccountArray(i).getBalance();
				boolean active = c.getAccountArray(i).getActive();
				
				new_admin.add(new Admin(Customer_Name, Customer_ID, Account_ID, PIN, balance,active));
				p++;
			}
		}
		
		for (int j = (p - 1); j >= 0; j--){
			for (int i = 0; i < (p - 1); i++){
				l = i + 1;
				if(new_admin.get(i).getName().compareTo(new_admin.get(l).getName()) == 1){
					
					Collections.swap(new_admin,i,l);
					
				}
			}
		}
		//Prints out the Sorted Array List
		
				for (int i = 0; i < p; i++){
					if(new_admin.get(i).getActive()){
						new_admin.get(i).info();
					}
				}
				new_admin.clear();
	}


//This Method Prints Out a List of All Accounts w/ Info Sorted by Balance (Highest to Lowest)	
	public void adminBalance(){

		int p = 0;
		int l = 0;

//Builds up an Array List of Admin Objects to Be Sorted and Printed
		
		ArrayList<Admin>new_admin = new ArrayList<Admin>();
		System.out.println("[Name]\t\t[Cust ID]\t[Acct ID]\t[Pin #]\t\t[Balance]");
		for (Customer c: cust){
			for (int i = 0; i < c.getAccountNum(); i++){
				
				String Customer_Name = c.getName();
				String Customer_ID = c.getId();
				String Account_ID = c.getAccountArray(i).getNumber();
				String PIN = c.getPin();
				double balance = c.getAccountArray(i).getBalance();
				boolean active = c.getAccountArray(i).getActive();
				
				new_admin.add(new Admin(Customer_Name, Customer_ID, Account_ID, PIN, balance,active));
				p++;
			}
		}
		
//Sorts the Array List for Balance Highest to Lowest (Bubble Sort Algorithm)
		
		for (int j = (p - 1); j >= 0; j--){
			for (int i = 0; i < (p - 1); i++){
				l = i + 1;
				if(new_admin.get(i).getBalance() < new_admin.get(l).getBalance()){
					
					Collections.swap(new_admin,i,l);
					
				}
			}
		}
//Prints out the Sorted Array List
		
		for (int i = 0; i < p; i++){
			if(new_admin.get(i).getActive()){
				new_admin.get(i).info();
			}
		}
		new_admin.clear();
	}
	
	
//This Method Prints a List of A Single Customers Accounts w/ Info Sorted by Account Number
	public void adminCustomer(){
		ArrayList<Admin>new_admin = new ArrayList<Admin>();
		boolean found = false;
		
		String ID = "";
		int n = 0;
		int p = 0;
		int l = 0;
		
		System.out.println("\nEnter the Desired Customer ID");
		System.out.print("==> ");
		ID = console2.readLine();
		
		for (Customer c: cust){
			
			if(ID.equals(c.getId())){
				found = true;
				break;
			}
			n++;
			
		}
		
		if (!found){
			System.out.println("Customer Not Found");
			return;
			
		}else{
			System.out.println(n);
			System.out.println("[Name]\t\t[Cust ID]\t[Acct ID]\t[Pin #]\t\t[Balance]");
			for (int i = 0; i < cust.get(n).getAccountNum(); i++){
				String Customer_Name = cust.get(n).getName();
				String Customer_ID = cust.get(n).getId();
				String Account_ID = cust.get(n).getAccountArray(i).getNumber();
				String PIN = cust.get(n).getPin();
				double balance = cust.get(n).getAccountArray(i).getBalance();
				boolean active = cust.get(n).getAccountArray(i).getActive();
				
				new_admin.add(new Admin(Customer_Name, Customer_ID, Account_ID, PIN, balance,active));
				p++;
				//if(cust.get(n).getAccountArray(i).getActive()){
					
					//System.out.println(c.getName() + "\t\t\t" + c.getId() + "\t\t\t" + ID + "\t\t\t"+ c.getPin() + "\t\t$" + rounded);
				//}
				
			}
			
			for (int j = (p - 1); j >= 0; j--){
				for (int i = 0; i < (p - 1); i++){
					l = i + 1;
					if(new_admin.get(i).getAccount_ID() > new_admin.get(l).getAccount_ID()){
						
						Collections.swap(new_admin,i,l);
						
					}
				}
			}
			
			for (int i = 0; i < p; i++){
				if(new_admin.get(i).getActive()){
					new_admin.get(i).info();
				}
			}
			new_admin.clear();
			
		}
		
	}

}




