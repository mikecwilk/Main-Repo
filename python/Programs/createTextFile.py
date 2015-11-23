#!/usr/bin/python

import time as t
from os import path
import os



def createFile(dest):
	'''
	The script creates a text file at the past location
	names file based on date
	'''
	
	date = t.localtime(t.time())
	name = '%d_%d_%d_1.txt'%(date[1],date[2],(date[0]%100))
	
	if not(path.isfile(destination + name)):
		for x in range(1,6):
			name = '%d_%d_%d_%d.txt'%(date[1],date[2],(date[0]%100),x)
			f=open(destination + name  ,'w')
			f.write('\n'*30)
			f.close()
			print("\n")
			print("created " + name + " in destination " + destination)
			print("\n")
		
	else:
		
		print("files already created")
		os.system("mkdir dump2")

		
	
if __name__ =='__main__':

	destination = 'C:\\cygwin\\home\\wilkm\\Scripts\\python\dump\\'
	createFile("destination")
	
	input("done!!!")
	
