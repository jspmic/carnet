from function import *

while True:
	db_name = input("Name: ").capitalize()
	db_table = input("Quarter: ")
	if (db_name=='' or db_table==''):
		print("Please fill these fields correctly")
	else: break

manager = DB_MANAGE(db_name)

try:
	cmd = f"CREATE TABLE trimestre_{db_table} (Cours TEXT, Notes TEXT, Total TEXT, Pourcentage TEXT)"
	manager.manage(cmd)
except:
	print("DB already exists!")

print("Successful Connection!")
print("Available DBs: ",*(manager.enum))

while True:
	course = input("Course: ")
	if course=='quit': break
	notes = manager.course_verify(db_table,course)[1] #/**/
	print("Previous grades: ",notes)
	print("Succeeded!")
	append = input("Append(y/n): ")

	if (append=="y" and course!=''):
		i=1
		while True:
			n = input(f"Note {i}: ")
			if n=='quit': break
			notes+=(n+" ")
			i+=1
	else:
		cmd = f"SELECT * FROM trimestre_{db_table} WHERE COURS='{course}'"
		grades = manager.manage(cmd)
		print("\n{2} Total: {0}\nPourcentage: {1}\n".format(grades[0][2],grades[0][3],course))
		continue

	cmd = f"UPDATE trimestre_{db_table} SET Notes='{notes}' WHERE Cours='{course}'"
	value = manager.manage(cmd)
	if value==0:
		print("Updated Successfully!")
		total = f_total(manager,db_table,course)
		percent = f_percent(total)
		manager.manage(f"UPDATE trimestre_{db_table} SET Total='{total}' WHERE Cours='{course}'")
		manager.manage(f"UPDATE trimestre_{db_table} SET Pourcentage='{percent}' WHERE Cours='{course}'")

#Calculating General Total From TABLE
cmd = f"SELECT * FROM trimestre_{db_table}"
grades_total = []
maxima_total = []

for i in manager.manage(cmd):
	if i[0]=='Total' or i[0]=='Pourcentage':
		break
	grades,maxima = [eval(i) for i in i[2].split('/')]
	grades_total.append(grades)
	maxima_total.append(maxima)

general_total = f"{sum(grades_total)}/{sum(maxima_total)}"
general_percentage = "%.2f"%(sum(grades_total)*100/sum(maxima_total))
manager.manage(f"UPDATE trimestre_{db_table} SET Total='{general_total}' WHERE Cours='Total'")
manager.manage(f"UPDATE trimestre_{db_table} SET Pourcentage='{general_percentage}' WHERE Cours='Total'")
print("\nGeneral Total: ",general_total)
print("General Percentage: ",general_percentage,'\n')

#End
print("Closing Connection...")
manager.MAIN_DB.close()
