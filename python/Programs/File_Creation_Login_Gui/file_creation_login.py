#!/usr/bin/python

import tkinter as tk
from tkinter import *
from os import path
import sys
import os
from PIL import Image

dest = 'C:\\cygwin\\home\\wilkm\\python\dump1\\'

def exitLogin():
    global exit_var
    exit_var = 'true'
    root.destroy()
   
def exitGUI():
    root.destroy()

def dest1():
	global dest
	
	dest = 'C:\\cygwin\\home\\wilkm\\python\dump1\\'
	button5 = tk.Button(text="dump1", bg="red", command = dest1)
	button5.grid(row = 4, column = 0)
	button6 = tk.Button(text="dump2", bg="grey", command = dest2)
	button6.grid(row = 4, column = 1)
	label6["text"] = ("Command: SELECT dump1" )

	print(dest)
	return();

def dest2():
	global dest
	
	dest = 'C:\\cygwin\\home\\wilkm\\python\dump2\\'
	button5 = tk.Button(text="dump1", bg="grey", command = dest1)
	button5.grid(row = 4, column = 0)
	button6 = tk.Button(text="dump2", bg="red", command = dest2)
	button6.grid(row = 4, column = 1)
	label6["text"] = ("Command: SELECT dump2" )
	print(dest)
	return();

def createFile():
	label6["text"] = ("Command: FILL " + dest)
	


	if not(path.isfile(dest + name.get() + '1')):
		for x in range(1,6):
			v = (name.get())
			x = str(x)
			v = (v + x)
			print ("created " + v + " in " + dest)
			f=open(dest + v  ,'w')
			f.write('\n'*30)
			f.close()



			#print("created " + username + " in destination " + destination)


	else:

		label6["text"] = ("Files Already Created ")

def clearName():
	label6["text"] = ("Command: CLEAR " + dest)
	for x in range(1,6):
		p = (name.get())
		x = str(x)
		p = (p + x)
		os.system("rm " + dest + p)
		print("clearing " + p + " " + dest)

def printName():
	print(name.get())
	label6["text"] = (name.get())

def checkNamePass():
    if ((login.get()) == "login"):
        root.destroy()

def enterLogin(*ignore):
    if ((login.get()) == "login"):
        root.destroy()
    else:
        print("try again")
    

######################################################################
#
#Main Entry Point
#
######################################################################

root = tk.Tk()
root.title("Welcome")
name = tk.StringVar()
login = tk.StringVar()
exit_var = 'false'

label_login1 = tk.Label(text = "Username : ")
label_login2 = tk.Label(text = "Login : ")
ent = tk.Entry(root,textvariable = name)
ent2 = tk.Entry(root,textvariable = login)
btn1 = tk.Button(root, text="Login", command=checkNamePass)

label_login1.grid(sticky = W, row = 0, column =0)
ent.grid(sticky = W, row = 0, column =1)
label_login2.grid(sticky = W, row = 1, column =0)
ent2.grid(sticky = W, row = 1, column =1)
btn1.grid(row=3, column = 1)

root.protocol('WM_DELETE_WINDOW', exitLogin)  # root is your root window
loop = 'true'
root.bind('<Return>', enterLogin)

root.mainloop()

if (exit_var == 'true'):
    root.destroy()

root = tk.Tk()
root.title("File Sorter")
root.geometry("400x160")

label1 = tk.Label(text = "make a selection")
label1.grid(row = 0, column =0)
label2 = tk.Label(text = "                      ")
label2.grid(sticky = W, row = 0, column = 1)
label3 = tk.Label(text = "                       ")
label3.grid(sticky = W, row = 0, column = 2)
label4 = tk.Label(text = "                ")
label4.grid(sticky = W, row = 0, column = 3)
label4 = tk.Label(text = "                ")
label4.grid(sticky = W, row = 1, column = 0)
label5 = tk.Label(text = "                ")
label5.grid(sticky = W, row = 3, column = 0)
label7 = tk.Label(text = "                ")
label7.grid(sticky = W, row = 5, column = 0)
label6 = tk.Label(text = "Command: ")
label6.grid(sticky = W, columnspan = 1000, row = 6, column = 0)

button2 = tk.Button(text="Fill", fg="black", command = createFile)
button3 = tk.Button(text="Clear", fg="black", command = clearName)
button4 = tk.Button(text="Exit", fg="black", command = exitGUI)
button5 = tk.Button(text="dump1", fg="black", bg="red", command = dest1)
button6 = tk.Button(text="dump2", fg="black", command = dest2)
button7 = tk.Button(text="Username?", fg="red", command = printName)

button2.grid(row = 2, column = 0)
button3.grid(row = 2, column = 1)
button4.grid(row = 2, column = 3)
button5.grid(row = 4, column = 0)
button6.grid(row = 4, column = 1)
button7.grid(row = 2, column = 2)

root.mainloop()








