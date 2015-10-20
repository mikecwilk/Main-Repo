Program 1 Readme File

To run this program you must have the files Account.java, ATM.java, ConsoleReader.java, Customer.java, p1.java, and Sav_Acct.java all in your working directory.
-type: javac Account.java etc until you have all your .class files generated
-type: java p1 to run the program!

This program consists of Choices that are user inputs in the form of numbers.

The Choices Are:

1) Create Customer
2) Open Account
3) Deposit
4) Withdraw
5) Transfer
6) Account Information
7) Close Account
9) Exit ATM

Create Customer:
This Choice will create a new customer object and add it to an ArrayList

Open Account: 
This Choice will add an account object to an existing customer object and add it to a corresponding ArrayList

Deposit:
This Choice will add funds to a Customer objects specific account that is selected by the user

Withdraw: 
This Choice will withdraw funds from a Customer objects specific account that is selected by the user

Tranfser:
This choice will take funds from A Customers account and place them in another one of their accounts

Account Information:
This choice will print out all account information for a chosen customer

Close Account:
This choice will close an account for a given Customer

Exit ATM:
This choice closes the program

A secret choice exists that I will call Admin (it is accessed by selecting 0 at the initial menu)
Admin has a pin requirement which is hard coded at "abcd" and will open a menu

1) Show accounts order by customer name
2) Show accounts order by highest balance
3) Show accounts belonging to the same customer

Show accounts order by customer name:
This runs a sorting algorithm that prints out all the accounts information sorted by name

Show accounts order by highest balance:
This runs a sorting algorithm that prints out all the accounts information sorted by balance

Show accounts belonging to the same customer:
This runs a sorting algorithm that prints out the accounts information sorted by account number for a selected customer