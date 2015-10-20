package hw1;

public class hw1{

  public static void main(String[] args)
  {
    final int ACTION_1        = 1;
    final int ACTION_2        = 2;
    final int ACTION_3        = 3;
    final String ACTION_a		  = "a";
    final String ACTION_b		  = "b";
    final String ACTION_c		  = "c";
    final String ACTION_d		  = "d";
    final int ACTION_EXIT     = 9;

    int action = 9;
    String action_string = "";

    ConsoleReader console = new ConsoleReader(System.in);

    while(true)
    {
      System.out.println("\nWelcome to CS49J Programming Example\n");
      System.out.println(ACTION_1 + ") Print your name in HEX");
      System.out.println(ACTION_2 + ") Simple number calculations");
      System.out.println(ACTION_3 + ") HW 1");
      System.out.println(ACTION_EXIT + ") Exit\n");

      System.out.print("Enter choice ==> ");
      action = console.readInt();

      switch(action)
      {
        case ACTION_1:
        {
	  int i;
	  String name;

          System.out.println("\nPlease enter your name");
          System.out.print("==> ");
          name = console.readLine();

	  for (i = 0; i < name.length(); i++)
	  {
            System.out.printf("%c  ", name.charAt(i));
	  }

          System.out.printf("\n");

	  for (i = 0; i < name.length(); i++)
	  {
            System.out.printf("%x ", name.codePointAt(i));
	  }

          System.out.printf("\n");

          break;
        }

        case ACTION_2:
        {
	  double n1, n2;

          System.out.println("\nEnter first number");
          System.out.print("==> ");
          n1 = console.readDouble();

          System.out.println("Enter second number");
          System.out.print("==> ");
          n2 = console.readDouble();

	  System.out.printf("\nAdd = %f\n", n1 + n2);
	  System.out.printf("Sub = %f\n", n1 - n2);
	  System.out.printf("Mul = %f\n", n1 * n2);
	  System.out.printf("Div = %f\n", n1 / n2);

          break;
        }

        case ACTION_3:
        {
        	int hw1 = 1;
        	while(hw1 == 1)
 	        {   
	            System.out.println("\nWelcome to CS49J Homework 1!\n");
	            System.out.println(ACTION_a + ") Find the remainder of two integers");
	            System.out.println(ACTION_b + ") Calculate the factorial of an integer");
	            System.out.println(ACTION_c + ") Sum of all positive odd integer numbers for an integer");
	            System.out.println(ACTION_d + ") Main Menu\n");
	            
	            System.out.print("Enter choice ==> ");
	            action_string = console.readLine(); 
	            
	               
	            switch(action_string)
	            {
	            	case ACTION_a:
	            	{
	            		int int1;
	            		int int2;
	            		int result;
            	  
	            		System.out.println("Enter Integer 1 ==>");
	            		int1 = console.readInt();
	            		System.out.println("Enter Integer 2 ==>");
	            		int2 = console.readInt();
	            		System.out.printf("Remainder of %d / %d", int1, int2);
	            		result = int1 % int2;
	            		System.out.printf(" is %d\n", result);
	            		
	            		System.out.printf("Remainder of %d / %d", int2, int1);
	            		result = int2 % int1;
	            		System.out.printf(" is %d\n", result);
	            		
	            		
	            		break;
            	  
	            	}
	            	
	            	case ACTION_b:
	            	{
	            		int int1;
	         	            		            	  
	            		System.out.println("Enter Integer For Factorial ==>");
	            		int1 = console.readInt();
	            		long result = int1;
	            		for(int i = int1 - 1; i > 0; i--) {
	            			//DEBUG System.out.printf(" %d",i);
	            			result = result *i;
	            		}
	            		System.out.printf("Factorial of %d is %d\n",int1, result);
	            		
	            		break;
            	  
	            	}
	            	
	            	case ACTION_c:
	            	{
	            		int int1;
		            	  
	            		System.out.println("Enter Integer n to Find The Sum of All Positive Odd Integer Numbers Up to n ==>");
	            		int1 = console.readInt();
	            		int result = 0;
	            		for (int i = 0; i <= int1; i++){
	            			
	            			if(i % 2 == 1){
	            				//DEBUG System.out.printf(" %d",i);
	            				result = result + i;
	            				
	            			}
	            			
	            		}
	            		System.out.printf("Sum of All Positive Odd Integers of %d is %d\n",int1 ,result);
	            		break;
            	  
	            	}
	            	
	            	case ACTION_d:
	            	{
	            		hw1 = 0;
	            		break;
            	  
	            	}
	            }
	        }
        	//hw1 = false;
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