#SMTP with Python to send emails

import smtplib

smtpObj = smtplib.SMTP('smtp.gmail.com', 587) 		#gets SMTP object

smtpObj.ehlo()										#says hello (protocol) to SMTP server

smtpObj.stattls()									#starts TLS encryption
smtpObj.login('mikecwilk@gmail.com','<password goes here>')	#login into email account info
smtpObj.sendmail('mikecwilk@gmail.com', 'mikecwilk@gmail.com', 'Subject: This is a test!') 	#sender, destination and message!
smtpObj.quit()
