
public class Account implements java.io.Serializable{

	private String number; // 4 digit string 
	private double balance;
	private boolean active;
	private int array_number;
	private boolean type;
	int interest = 5;
	
	public Account(int Account_Number, int total_accounts) {
		String Accnt_Num = String.valueOf(Account_Number);
		this.number = Accnt_Num;
		this.balance = 0;
		this.active = true;
		this.array_number = total_accounts;

	}

//This Method Simply Checks Whether the Account is Checking or Savings and Prints out Relevant Information 	
	void check_balance(){
		
		String type = "";
		if(this.type == true){
			type = "Savings";
		}else{
			type = "Checking";
		}
		System.out.println("\nAccount Type: " +  type);
		System.out.println("Account number: " + this.number);
		System.out.println("Account balance: " + this.balance);
		System.out.println("Active?: " + this.active);
		
	}
	
//This Method Just Prints Out Account Info and returns the Array Number
	int info(){
		
		System.out.println("Account number: " + this.number);
		System.out.println("Account balance: " + this.balance);
		System.out.println("Active?: " + this.active);
		//System.out.println("array number: " + this.array_number);
		return this.array_number;
	}

//This Method Returns the account number and increments the 
	String validateAccount(){
		
		array_number += 1;
		return this.number;
		
	}

//This Method Updates the Balance for This Account and Runs the Method info() to Print Account Info
	void addDeposit(double deposit){
		System.out.println("\n**Account balance updated**");
		this.balance = this.balance + deposit;
		this.info();
	}

//This Method Checks This Account to See if There are Enough Funds For Withdraw If So it Updates the Balance Accordingly and Prints Account Info
	void subWithdraw(double withdraw){
		
		if (withdraw > this.balance){
			System.out.println("\nInsufficient Funds!");
		}else{
			System.out.println("\n**Account balance updated**");
			this.balance = this.balance - withdraw;
			this.info();
		}
	}

//This Method is Used When Transferring From One Account To Another and Removes Funds From the Balance
	void removeFunds(double transfer_amount){
		
		this.balance = this.balance - transfer_amount;
		
	}

//This Method is Used When Transferring From One Account To Another and Adds Funds To the Balance
	void addFunds(double transfer_amount){
		
		this.balance = this.balance + transfer_amount;
		
	}

//This Method Adds To the Balance (Every 5 transactions) The Interest Rate for All Savings Accounts	
	void addInterest(){
		this.balance = this.balance + this.balance * this.interest/100;
	}

////////////////////////////////////////////////////////////////////////////////
//						Simple Getters and Setters							  //
////////////////////////////////////////////////////////////////////////////////

	int getArray(){
		return array_number;		
	}
	
	String getNumber(){
		return this.number;
		
	}
	
	double getBalance(){
		
		return this.balance;
		
	}
	
	boolean getType(){
		return type;
	}
	
	void setTypeSavings(){
		this.type = true;
	}
	
	void setTypeChecking(){
		this.type = false;
	}
	
	void setActiveFalse(){
		
		this.active = false;
		this.balance = 0;
	}
	
	boolean getActive(){
		return this.active;
	}

}