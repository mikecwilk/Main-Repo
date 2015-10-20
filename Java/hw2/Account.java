
public class Account {

	private String number; // 4 digit string 
	private double balance;
	private boolean active;
	private int array_number;
	
	public Account(int Account_Number, int total_accounts){
		String Accnt_Num = String.valueOf(Account_Number);
		this.number = Accnt_Num;
		this.balance = 0;
		this.active = true;
		this.array_number = total_accounts;
	}

	void check_balance(){
		System.out.println("Account number: " + this.number);
		System.out.println("Account balance: " + this.balance);
		System.out.println("Active?: " + this.active);
		
	}
	
	int info(){
		
		
		System.out.println("Account number: " + this.number);
		System.out.println("Account balance: " + this.balance);
		System.out.println("Active?: " + this.active);
		System.out.println("array number: " + this.array_number);
		return this.array_number;
	}
	
	int getArray(){
		return array_number;		
	}
	
	String getNumber(){
		return this.number;
		
	}
	
	String validateAccount(){
		
		array_number += 1;
		return this.number;
		
	}
	
	void addDeposit(double deposit){
		System.out.println("\n**Account balance updated**");
		this.balance =+ deposit;
		this.info();
	}
	
	void checkIndex(String account){
		if(this.number == account){
			System.out.println("maybe");		
		}
	}
	

}
