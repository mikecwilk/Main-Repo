/*
  Name:	hw2.java
  	Desc:	This program will emulate an online banking system that has seven basic 
	operations (create,open,close,deposit,withdraw,transfer,get balance).
	For HW2 we are just implementing options 1,2,3,6 and 9
*/
//import java.io.*;

public class p1{
	
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
    final String ACTION_ADMIN        = "0";
    final String ACTION_CREATE       = "1";
    final String ACTION_OPEN         = "2";
    final String ACTION_DEPOSIT      = "3";
    final String ACTION_WITHDRAW     = "4";
    final String ACTION_TRANSFER     = "5";
    final String ACTION_ACCOUNT_INFO = "6";
    final String ACTION_CLOSE        = "7";
    final String ACTION_EXIT         = "9";
    
    final String ACTION_ADMIN_1		 = "1";
    final String ACTION_ADMIN_2		 = "2";	
    final String ACTION_ADMIN_3		 = "3";	
    final String ACTION_ADMIN_4		 = "4";	
    
    String action = "0";
    String action_admin = "0";
    String admin_pin = "";



    ConsoleReader console = new ConsoleReader(System.in);        

    Atm atm = new Atm();
    
    while(true)
    { 
      
      System.out.println("\nWelcome to the CS49J Banking System\n");
 //     System.out.println("Total customers: " + Customer.total_customers);
      System.out.println(ACTION_CREATE + ") Create Customer");
      System.out.println(ACTION_OPEN + ") Open Account");
      System.out.println(ACTION_DEPOSIT + ") Deposit");
      System.out.println(ACTION_WITHDRAW + ") Withdraw");
      System.out.println(ACTION_TRANSFER + ") Transfer");
      System.out.println(ACTION_ACCOUNT_INFO + ") Account Information");
      System.out.println(ACTION_CLOSE + ") Close Account");
      System.out.println(ACTION_EXIT + ") Exit ATM\n");

      System.out.print("Enter choice ==> ");
      action = console.readLine();

	      switch(action)
	      {
	
	        case ACTION_ADMIN:
	        {
	        	
	        	System.out.print("Enter Admin Password ==> ");
	            admin_pin = console.readLine();

	            if (admin_pin.equals("abcd")){
	                System.out.println("\nWelcome to the CS49J Administrative Banking System\n");
		        	System.out.println(1 + ") Show accounts order by customer name");
		            System.out.println(2 + ") Show accounts order by highest balance");
		            System.out.println(3 + ") Show accounts belonging to the same customer\n");
		            
		            System.out.print("Enter choice ==> ");
		            action_admin = console.readLine();
		            
		            switch(action_admin)
		            {
		            	case ACTION_ADMIN_1:
			            	{
			            		atm.adminNames();
			            		break;
			            	}
		            	case ACTION_ADMIN_2:
			            	{
			            		atm.adminBalance();
			            		break;
			            	}
		            	case ACTION_ADMIN_3:
			            	{
			            		atm.adminCustomer();
			            		break;
			            	}
		            	case ACTION_ADMIN_4:
		            		{
			            		System.out.println("Exiting Admin");
			            		break;
			            	}
			            	
			            default: 
			            	{
			            		System.out.println("Exiting Admin");
			            		break;
			            	}
		            }
		        //atm.admin();
		          break;
		        }else{
		        	break;
		        }
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
	        	
	        	int ID = atm.login();
	        	
	    		if (ID != -1){
	    			atm.open_account(ID);
	    			break;
	    		}
	    			break;	
	    			
	        }
	 
	
	
	        case ACTION_DEPOSIT:
	        {
	    		
	        	int ID = atm.login();      	
	    		if (ID != -1){
	    			atm.deposit(ID);
	    			break;
	    		}
	 
				break;
	        }
	
	        case ACTION_WITHDRAW:
	        {

	        	int ID = atm.login();      	
	    		if (ID != -1){
	    			atm.withdraw(ID);
	    			break;
	    		}
	    		
	    		break;
	        }
	        
	        case ACTION_TRANSFER:
	        {
	        	int ID = atm.login();      	
	    		if (ID != -1){
	    			atm.transfer(ID);
	    			break;
	    		}
	    		
	    		break;
	        
	        }
	
	        case ACTION_ACCOUNT_INFO:
	        {
	        		
	        	int ID = atm.login();      	
	    		if (ID != -1){
	    			atm.get_balance(ID);
	    			break;
	    		}	
	    		break;
					
	        }
	
	        case ACTION_CLOSE:
	        {
	        	
	        	int ID = atm.login();      	
	    		if (ID != -1){
	    			atm.close_account(ID);
	    			break;
	    		}	
	    		break;
	        }
	        
	        case ACTION_EXIT:
	        {
	          System.out.println("\n Good bye\n");
	          return;
	        }
	        
	        default:
	        {
	        	System.out.println("\nPlease select an option from the list!!");
	        	break;
	        
	        }
	      }
	    }
	  } 
}