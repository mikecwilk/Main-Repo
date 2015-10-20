import java.io.*;
import java.util.ArrayList;

public class Customer implements java.io.Serializable{
	File file = new File("p1.dat");
	
	private String name;
	private String id; 	//3 digits string
	private String pin; //4 digits string
	private ArrayList <Account> acct;
	private int my_account_num;
	private int transactions;
	
//	private double total_bal; //for all accounts
	public static int total_accounts;
	public static int total_customers;
	public static int total_transactions;
	private int total;
	
	
	public Customer(String new_name, String new_id, String new_pin) { //Constructor
		acct = new ArrayList<>(100);
		this.name = new_name;
		this.id = new_id;
		this.pin = new_pin;
		this.my_account_num = 0;
		this.transactions = 0;
		
	}

//This Method Simply Prints Useful Customer Info
	void info(){
				
		System.out.println("Customer Name: " + this.name);
		System.out.println("Customer pin: " + this.pin);
		System.out.println("Customer ID: " + this.id);

	}

//This Method Validates the Account By Checking Whether it Exists (It also functions to deposit funds if the account does exist)
	void validateAccount(String account, String deposit){
		double dbl_deposit = Double.parseDouble(deposit);
		boolean dep = false;
		for (int i = 0; i <  this.my_account_num; i++){

			if((this.acct.get(i).getNumber()).equals(account) && (this.acct.get(i).getActive())){
				this.acct.get(i).addDeposit(dbl_deposit);
				dep = true;
				Customer.total_transactions += 1;
				break;
			}
			
		} 
		if (!dep){
			System.out.println("\nAccount " + account + " Does not Exist For This User!");
		}
	}

//This Method Validates the Account By Checking Whether it Exists (It also functions to withdraw funds if the account does exist)
	void validateAccountWithdraw(String account, String withdraw){
		double dbl_withdraw = Double.parseDouble(withdraw);
		boolean dep = false;
		for (int i = 0; i <  this.my_account_num; i++){

			if((this.acct.get(i).getNumber()).equals(account) && (this.acct.get(i).getActive())){
				this.acct.get(i).subWithdraw(dbl_withdraw);
				dep = true;
				Customer.total_transactions += 1;
				break;
			}
			
		} 
		if (!dep){
			System.out.println("\nAccount " + account + " Does not Exist For This User!");
		}
	}

//This Method Validates the Account By Checking Whether it Exists (Used For Transfers)
	boolean validateAccountToFrom(String account){
		boolean dep = false;
		for (int i = 0; i < this.my_account_num; i++){

			if((this.acct.get(i).getNumber()).equals(account) && (this.acct.get(i).getActive())){
				dep = true;
				
				return true;
				
			}
			
		} 
		if (!dep){
			System.out.println("\nAccount " + account + " Does not Exist For This User!");
			return false;
		}
		
		return false;
	}

//This Method Checks All The Balances of The Accounts and Updates Totals When Interest is Added
	void checkBalances(){

		double total = 0;
		System.out.println("\nAccount Owner's Name: " + this.name);
		System.out.println("Account Owner's ID Number " + this.id);
//		for (int i = 0; i < this.total; i++){
		for (int i = 0; i < this.my_account_num; i++){
			if(this.acct.get(i).getType() == true){
				this.acct.get(i).check_balance();
				((Sav_Acct)this.acct.get(i)).getInterest();
				total += this.acct.get(i).getBalance();
			}else{
				this.acct.get(i).check_balance();
				
				total += this.acct.get(i).getBalance();
				
			}
			
		} 
		System.out.println("Total Balance: " + total);
	}

//This Method Adds a Checking Account to The Customers Corresponding Account Array List
	void addAccountChecking(int Account_Number){
		Account new_account = new Account(Account_Number, total_accounts);
		System.out.println("\n**Checking Account Created**");
		new_account.info();
		new_account.setTypeChecking();
		this.acct.add(total, new_account);
		total_accounts +=1;
		this.my_account_num +=1;

	}

//This Method Adds a Savings Account to The Customers Corresponding Account Array List
	void addAccountSaving(int Account_Number){
		Account new_account = new Sav_Acct(Account_Number, total_accounts);
		System.out.println("\n**Savings Account Created**");
		new_account.info();
		new_account.setTypeSavings();
		this.acct.add(total, new_account);
		total_accounts += 1;
		this.my_account_num +=1;

	}

//This Method is Implemented to Check The Interest on Savings Accounts (For future implementation of different interest rates)
	void checkSavings(){
		((Sav_Acct) this.acct.get(0)).getInterest();
	}

//This Method Transfers Funds From One Account to Another
	void makeTransfer(String account_from, String account_to, String transfer_amount){
			
		int int_account_from = -1;
		int int_account_to = -1;
		double dbl_transfer_amount = Double.parseDouble(transfer_amount);
		
			for (int i = 0; i < this.my_account_num; i++){
				if((this.acct.get(i).getNumber()).equals(account_from)){
					
					int_account_from = i;
				}
			}
			
			for (int i = 0; i < this.my_account_num; i++){

				if((this.acct.get(i).getNumber()).equals(account_to)){
					int_account_to = i;
					
				}
			}
			
			if(int_account_from != -1 && int_account_to != -1){
				
				System.out.println("\nTransferring " + transfer_amount + " from account " + account_from);
				this.acct.get(int_account_from).removeFunds(dbl_transfer_amount);
				System.out.println("Transferring " + transfer_amount + " to account " + account_to);
				this.acct.get(int_account_to).addFunds(dbl_transfer_amount);
				
				System.out.println("\n**Updated Account Info**");
				
				this.acct.get(int_account_from).info();
				this.acct.get(int_account_to).info();
			}else{
				System.out.println("Account does not exist!");
			}
		
		
	}
	
//This Method is Used to Make Sure the Customer Has Enough Money in Their Account To Transfer Funds
	boolean checkAmount(String account_from, String transfer_amount){
		
		double dbl_transfer_amount = Double.parseDouble(transfer_amount);;
		
		int int_account_from = -1;
		
		for (int i = 0; i < this.my_account_num; i++){
			if((this.acct.get(i).getNumber()).equals(account_from)){
				
				int_account_from = i;
			}
		}
		
		if (int_account_from != -1){
			if(this.acct.get(int_account_from).getBalance() >= dbl_transfer_amount){
				return true;
			}else{
				return false;
			}
						
		} else{
			return false;
		}
		

	}

//This Method Sets the Selected Accounts Active Flag to False 
	void closeAccount(String account){
		int int_account = -1;
		
		for (int i = 0; i < this.my_account_num; i++){
			if((this.acct.get(i).getNumber()).equals(account)){
				
				int_account = i;
			}
		}
		
		if(int_account != -1){
			this.acct.get(int_account).setActiveFalse();
			System.out.println("\n**Updated Account Info**");
			this.acct.get(int_account).info();
		}else{
			System.out.println("Account does not exist!");
			
		}
		
	}

//This Method Adds Interest to All the Savings Accounts 
	void addInterest(){
		for (int i = 0; i < this.my_account_num; i++){
			if(this.acct.get(i).getType() == true){ //Savings
				
				this.acct.get(i).addInterest();
				//this.acct.get(i).check_balance();
				
			}else{ 									//Checking
				//No Action because there is no interest on Checking accounts			
			}		
		}
	}

//This Method Prints Out Account Information for Each of a Customers Accounts	
	public void listAccounts(){
		System.out.println("\n[Account #]\t[Account Type]");
		for (int i = 0; i < this.my_account_num; i++){
			if(this.acct.get(i).getActive()){
				System.out.printf("\n[" + this.acct.get(i).getNumber() + "]\t\t" + "["); 
				if(this.acct.get(i).getType()){
					System.out.printf( "Savings]");
				}else{
					System.out.printf( "Checking]");
				}
			}
		}
		System.out.println("");
		
	}
////////////////////////////////////////////////////////////////////////////////
//						Simple Getters and Setters							  //
////////////////////////////////////////////////////////////////////////////////

	public String getName(){
		return this.name;
	}
	
	public String getId(){
		return this.id;
	}
	
	public String getPin(){
		return this.pin;
	}

	public ArrayList <Account> getAccountArrayList(){
		return this.acct;
	}
	public Account getAccountArray(int i){
		return this.acct.get(i);
	}
	
	public int getAccountNum(){
		return my_account_num;
	}

	public int getTransactions(){
		return this.transactions;
	}
	
	public void addTransaction(){
		this.transactions += 1;
	}
	

	public void getTotal(){
		this.total +=1;
	}

	String validatePin(){
		
		return this.pin;
		
	}	

	

	
	
	
	
}
