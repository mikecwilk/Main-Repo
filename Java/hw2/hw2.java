/*
  Name:	hw2.java
  	Desc:	This program will emulate an online banking system that has seven basic 
	operations (create,open,close,deposit,withdraw,transfer,get balance).
	For HW2 we are just implementing options 1,2,3,6 and 9
*/
//import java.io.*;

public class hw2{
	
	public static boolean isNumeric(String str)  {  
	  try  {  
		  double d = Double.parseDouble(str);  
	  }  
	  catch(NumberFormatException nfe)  {  
	    return false;  
	  }  
	  return true;  
	}
	
  public static void main(String[] args)
  
  {
    final int ACTION_ADMIN        = 0;
    final int ACTION_CREATE       = 1;
    final int ACTION_OPEN         = 2;
    final int ACTION_DEPOSIT      = 3;
    final int ACTION_WITHDRAW     = 4;
    final int ACTION_TRANSFER     = 5;
    final int ACTION_ACCOUNT_INFO = 6;
    final int ACTION_CLOSE        = 7;
    final int ACTION_EXIT         = 9;

    int action =0;
    


    ConsoleReader console = new ConsoleReader(System.in);        

    Atm atm = new Atm();
    
    while(true)
    {      
      System.out.println("\nWelcome to the CS49J Banking System\n");
      System.out.println(ACTION_CREATE + ") Create Customer");
      System.out.println(ACTION_OPEN + ") Open Account");
      System.out.println(ACTION_DEPOSIT + ") Deposit");
      System.out.println(ACTION_WITHDRAW + ") Withdraw");
      System.out.println(ACTION_TRANSFER + ") Transfer");
      System.out.println(ACTION_ACCOUNT_INFO + ") Account Information");
      System.out.println(ACTION_CLOSE + ") Close Account");
      System.out.println(ACTION_EXIT + ") Exit ATM\n");

      System.out.print("Enter choice ==> ");
      action = console.readInt();

      switch(action)
      {

        case ACTION_ADMIN:
        {
        
        System.out.println("\nNot Available for this assignment\n");
        //atm.admin();
          break;
        }

        case ACTION_CREATE:
        {
            String PIN = "";
            String NAME = "";
        	
        	System.out.println("\nPlease Enter Your Desired Name");
    		System.out.print("==> ");
    		NAME = console.readLine();
        	System.out.println("\nPlease Enter Your Desired 4 digit PIN (characters are not allowed)");
    		System.out.print("==> ");
    		PIN = console.readLine();
    		if (isNumeric(PIN) && PIN.length() == 4){
    			atm.create_customer(NAME, PIN);
    		}else{
    			System.out.println("\nThat was not a 4 digit number!");
    		}
    		
    		break;
        }

        case ACTION_OPEN:
        {
        	
        	String ID = "";
        	String PIN = "";
 
        	System.out.println("\nPlease Enter Your 3 Digit ID Number");
    		System.out.print("==> ");
    		ID = console.readLine();   		
        	
        	System.out.println("\nPlease Enter Your 4 digit PIN (characters are not allowed)");
    		System.out.print("==> ");
    		PIN = console.readLine();
        	
    		
    		if (isNumeric(ID) && isNumeric(PIN) && PIN.length() == 4 ){
    			atm.open_account(ID, PIN);
    		}else{
    			System.out.println("ID and/or PIN Incorrect!");
    			break;
    		}
    		
        	
    		
    		break;
        }

        case ACTION_DEPOSIT:
        {
        	String ID = "";
        	String PIN = "";
        	String amount = "";
        	String account = "";
        	double deposit = 0;
        	boolean validated = false;
    		   	
        	System.out.println("\nPlease Enter Your ID Number");
    		System.out.print("==> ");
    		ID = console.readLine();   		
        	
        	System.out.println("\nPlease Enter Your 4 digit PIN (characters are not allowed)");
    		System.out.print("==> ");
    		PIN = console.readLine();
    		
    		if (isNumeric(ID) && isNumeric(PIN) && PIN.length() == 4 ){
    			if(!atm.deposit(ID, PIN, validated, deposit, account)){
    				break;
    			}//else if(atm.deposit(ID, PIN, validated, deposit, account)){
    				
    			//}
    		}else{
    			System.out.println("ID and/or PIN Incorrect!!");
    			break;
    		}
			amount = console.readLine();
        	System.out.println("\nSelect an account");
    		System.out.print("==> ");
			account = console.readLine();
			deposit = Double.parseDouble(amount);
			validated = true;
			
			atm.deposit(ID, PIN, validated, deposit, account);
 
			break;
        }

        case ACTION_WITHDRAW:
        {
        	
        	//System.out.println("\nNot Available for this assignment\n");	
        	atm.withdraw();
        	break;
        }

        case ACTION_TRANSFER:
        {
        	//System.out.println("\nNot Available for this assignment\n");
        	//atm.transfer();
        	break;
        }

        case ACTION_ACCOUNT_INFO:
        {
        	String ID = "";
        	String PIN = "";
        	String account = "";
        	boolean validated = false;
 
        	System.out.println("\nPlease Enter Your ID Number");
    		System.out.print("==> ");
    		ID = console.readLine();   		
        	
        	System.out.println("\nPlease Enter Your 4 digit PIN (characters are not allowed)");
    		System.out.print("==> ");
    		PIN = console.readLine();
    		

    		if(atm.get_balance(ID, PIN, validated, account)){		
    			validated = true;
    			System.out.println("\nSelect an account");
    			System.out.print("==> ");
    			account = console.readLine();
				
			
    			atm.get_balance(ID, PIN, validated, account);
    		         
    			break;
    		}else{
    			break;
    		}
    		
    	
        }

        case ACTION_CLOSE:
        {
        	System.out.println("\nNot Available for this assignment\n");
        	//atm.close_account();
        	break;
        }
        
        case ACTION_EXIT:
        {
          System.out.println("\n Good bye\n");
          return;
        }
      }
    }
  }
}