import sys
import os
import glob
import sqlite3

#DATABASE MANAGEMENT
#------------------#

class DATABASE:
	"""Class for Database Existence Checking.
		Meant to check if a given database exists or not.
		use the corresponding system cmd to create the DB"""

	def __init__(self):

		self.enum = glob.glob("*.db") # Listing available databases
		self.exist = 0 #0 for non-existence and 1 for existence

	def existence(self,name:str) -> int:
		if name in self.enum: #checking if given name is an existing database or not
			self.exist=1 #Existence
		else:
			self.exist=0 #Non-existence

		return self.exist

	def creation(self,name:str) -> sqlite3.Cursor:
		name = name+'.db' #Adding the suffix .db to specify it's a DB
		db_exist = self.existence(name) #Verifying the existence of the given DB

		if db_exist!=1: #If DB is not found

			command = f"touch {name}" #Available in Linux and Mac OS
			os.system(command) #Creating file 'name.db'
			self.enum += [name] #Incrementing the list of the available DBs

		#Establishing Connection with the DB
		connection = sqlite3.connect(name)
		cursor = sqlite3.Cursor(connection)
		return (cursor,connection,self.enum)

class DB_MANAGE:
	"""Important Class for the management of some SQL commands"""
	def __init__(self,name):
		self.DB = DATABASE()
		self.DB_CURSOR,self.MAIN_DB,self.enum = self.DB.creation(name)

	def manage(self,command):
		#Conditions for some usual commands
		if "SELECT" in command:
			value = self.DB_CURSOR.execute(command).fetchall()
			return value
		else:
			self.DB_CURSOR.execute(command)
			self.MAIN_DB.commit()
			return 0
	def course_verify(self,tr,course):
		command = f"INSERT INTO trimestre_{tr} VALUES('{course}','','','');"
		courses = self.manage(f"SELECT * FROM trimestre_{tr} WHERE Cours='{course}'")
		try:
			if course in courses[0]:
				return courses[0]
			else:
				self.manage(command)
				return courses[0]
		except:
			self.manage(command)
			return (f"{course}",'','','')

#Additional Features

def f_total(manager,tr,course):
	notes = manager.course_verify(tr,course)[1]
	actual = [eval(i.split('/')[0]) for i in notes.strip().split()]
	maxima = [eval(i.split('/')[1]) for i in notes.strip().split()]
	print(f"{course} Total: {sum(actual)}/{sum(maxima)}")
	return f"{sum(actual)}/{sum(maxima)}"
	
def f_percent(total):
	clean = [eval(i) for i in total.strip().split('/')]
	try:
		percent = clean[0]*100/clean[1]
	except:
		return '0.0'
	print("Pourcentage: %.2f"%percent)
	return ("%.2f"%percent)

#--------------------------------------------#

if __name__=="__main__":
	print('module')
	sys.exit(0)
