import sqlite3
from datetime import *
from Queries import *
# db=sqlite3.connect("Library.db")
# cursor=db.cursor()

#Verifies that a user has made an account already in the appropriate Login table
def verifyLogin (role, username, password):
   role = role+"Login"
   db=sqlite3.connect("Library.db")
   cursor=db.cursor()
   cursor.execute("SELECT ID FROM "+role+" Where Username=? AND Password=?",(username, password))
   result=cursor.fetchone()[0]
   print(result)
   cursor.close()
   db.close()
   if(result):
       token=createActive(role, result)
       return token
   else:
       return False

#Adds a user to the Active table 
def createActive(role,ID):
   if role=="STUDENTLogin":
       role="stud"
   elif role=="FACULTYLogin":
       role="fac"
   elif role=="LIBRARIANLogin":
       role="lib"
   db=sqlite3.connect("Library.db")
   cursor=db.cursor()
   token=CreateToken()
   cursor.execute("Insert into Active (token,cred,ID,timestamp) values (?,?,?,?)",(token,role,ID,date.today()))
   db.commit()
   cursor.close()
   db.close()
   return token

#Creates a token to be used to identify a what actions a user can take
def CreateToken(): #Future improvment: More secure tokens
   db=sqlite3.connect("Library.db")
   cursor=db.cursor()
   cursor.execute("Select max(token) from active")
   token=int(cursor.fetchone()[0])+1
   cursor.close()
   db.close()
   return token

#Verifies that a user is elligible to create an account
#by checking that the are in the appropriate potential user table
def verifyUser(role, name, id):
   if (role=="LIBRARIAN" or role=="STUDENT"):
       role=role+"S"
   db=sqlite3.connect("Library.db")
   role = role.upper()
   cursor=db.cursor()
   cursor.execute("SELECT ID FROM "+role+" Where Name=? OR ID=?",(name, id))
   result=cursor.fetchone()
   if(result[0]):
       return True
   else:
       return False
 
#Creates an account for a new user
def signIn(role):
   print("Enter your name")
   name =  input()
   print("Enter your "+role+" id")
   res =  input()
   id = int(res)
   if(verifyUser(role, name, id)):
       print("Enter your new username")
       userName =  input()
       print("Enter your new password")
       password1 = input()
       db=sqlite3.connect("Library.db")
       cursor=db.cursor()
       querry = "insert into STUDENTLogin (Username, Password, ID) VALUES(?, ?, ?)"
       cursor.execute(querry,(userName, password1, id))
       db.commit()
       db.close()
       login(role)
   else:
       print("You are not an approved user of the library")

#Logs into the database
def login(role):
 
   print("Enter your user name")
   userName = input()
   print("Enter your password")
   password = input()
   token=verifyLogin(role, userName, password)
   if(token!=False):
       database(token)
   else:
       login(role)

#Logs out of the database
def LogOut(token):
   db = sqlite3.connect('Library.db')
   cursor = db.cursor()
   cursor.execute("delete from ACTIVE where token=?",(token,))
   db.commit()
   cursor.close()
   db.close()

#Runs the user interface for the database
def database(token):
   #get Name
   db=sqlite3.connect("Library.db")
   cursor=db.cursor()
   cursor.execute("select cred,ID from ACTIVE where token=?",(token,))
   ans=cursor.fetchone()
   SearcherTable=ans[0]
   ID=ans[1]
   if SearcherTable == "stud":
       cursor.execute("select name from students where ID=?",(ID,))
   elif SearcherTable == "fac":
       cursor.execute("select name from Faculty where ID=?",(ID,))
   elif SearcherTable == "lib":
       cursor.execute("select name from LIBRARIANS where ID=?",(ID,))
   name=cursor.fetchone()[0]
   #set functions
   functions=["Search","Add Book (Librarian only)", "Remove Book (Librarian only)", "Check Out Book", "Return Book","View Borrowing History","Generate Report (Librarian only)","Add User (Librarian only)","View Books"]
   #print functions
   print("Welcome ",name,"would you like to:")
   loggedin=True
   while loggedin==True:
       for i in range (len(functions)):
           print(i,functions[i])
       resp=input()
       if (resp=="0"):
           print("Search by Title(1), Author(2), or Catagory(3)?")
           search=input()
           if search=="1":
               searchByTitle(token)
           elif search=="2":
               searchByAuthor(token)
           elif search=="3":
               searchByCatagory(token)
       elif (resp=="1"):
           LibrarianAddBook(token)
       elif(resp=="2"):
           LibrarianRemoveBook(token)
       elif (resp=="3"):
           print("what is the title of the book?")
           ans=input()
           CheckOutCoppie(token,ans)
       elif (resp=="4"):
           ReturnCopies(token)
       elif (resp=="5"):
           viewBorrowingHistory(token)
       elif (resp=="6"):
           print("Generate Availability Report(1), Overdue Report(2), or Trend Report(3)")
           report=input()
           print("write the filename")
           filename=input()
           if report=="1":
               generateAvailabilityReport(token,filename)
           elif report=="2":
               generateOverdueBookReport(token,filename)
           elif report=="3":
               generateTrendsReport(token,filename)
       elif (resp=="7"):
           print("Which roll? Student(1), Faculty(2), or Librarian(3)")
           add=input()
           if add=="1":
                AddStudent(token)
           elif add=="2":
                AddFaculty(token)
           elif add=="3":
                AddLibrarian(token)
       elif (resp=="8"):
           seeBooks(token)
       elif (resp=="9"):
           cursor.close()
           db.close()
           LogOut(token)
           loggedin=False
   start()

#Starts the program
def start():
   print("Are you a STUDENT, FACULTY, or LIBRARIAN?")
   role = input()
   role = role.upper()
   if(role=="STUDENT" or role=="FACULTY" or role=="LIBRARIAN"):
       print("Do you already have an account? (yes or no)")
       account = input()
       if(account == "yes"):
           login(role)
       elif(account == "no"):
           signIn(role)
       else: start()
   else:
       start()

start()