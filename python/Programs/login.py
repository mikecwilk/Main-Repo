
loop = 'true'
while (loop == 'true'):
	username = input("Username Please : ")
	password = input("Password Please : ")
	if(username == "mike" and password == "wilk"):
		print ('Logged in Successfully as ' + username)
		loop = 'false'
		loop1 = 'true'
		while(loop1 == 'true'):
			command = input(username + "{} > > ")
			if(command == "exit" or command == "Exit"):
				break
			else:
				print ("'" + command + "' is not a valid command!")
	else:
		print('Invalid Credentials!')
	
