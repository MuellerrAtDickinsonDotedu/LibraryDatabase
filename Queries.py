import sqlite3
from datetime import *

#Allows an authorised user to add a book 
def LibrarianAddBook(token):
   if Verify(token,"LibrarianAddBook")==True:
       print("whats the ISBN of the book you would like to add?")
       ISBN=str(input())
       db=sqlite3.connect("Library.db")
       cursor=db.cursor()
       cursor.execute('Select ISBN from BOOKS where ISBN=?',(ISBN,))
       hasISBN=cursor.fetchall()
       if len(hasISBN)==0:
           if len(ISBN) == 13:
                   try:
                       this=int(ISBN)
                   except:
                       print("this is not an accepted ISBN")
           else:
               print("this is not an accepted ISBN")


           print("This is a book we have not seen before.")
           print("What is the title?")
           Title=input()
           print("Who's the Author?")
           Author=input()
           print("What is the Publication Year?")
           PublicationYear=input()
           print("What is the Catagory?")
           Catagory=input()
          
           cursor.execute('insert into BOOKS (ISBN, Title, Author, PublicationYear, Catagory) values (?,?,?,?,?)',(ISBN,Title,Author,PublicationYear,Catagory))


           print("How many copies are there?")
           numcopies=int(input())


           #find current maxBookID
           cursor.execute("select max(BookID) from copies")
           resp=cursor.fetchone()[0]
           BookID=int(resp)+1


           for x in range (0,numcopies):
               cursor.execute("insert into copies(BookID,ISBN,Availability) values (?, ?, 'yes')",(BookID,str(ISBN)))
               BookID=BookID+1
       else:
           print("How many copies are there?")
           numcopies=int(input())


           #find current maxBookID
           cursor.execute("select max(BookID) from copies")
           resp=cursor.fetchone()[0]
           BookID=int(resp)+1


           for x in range (0,numcopies):
               cursor.execute("insert into copies(BookID,ISBN,Availability) values (?, ?, 'yes')",(BookID,str(ISBN)))
               BookID=BookID+1
       db.commit()
       cursor.close()
       db.close()
   else:
       print("You are not authorized")

#Allows an authorised user to remove a book
def LibrarianRemoveBook(token):
   if Verify(token,"LibrarianRemoveBook")==True:
       db=sqlite3.connect("Library.db")
       cursor=db.cursor()
       print("What is the title of the book you want to remove?")
       title=str(input())
       print("what is the BookID of the book you want to remove?")
       BookID=int(input())
       cursor.execute("select bookID from copies where bookId=?",(BookID,))
       if len(cursor.fetchall())!=0:
           cursor.execute("Select ISBN from copies where bookID=? and ISBN in (select ISBN from BOOKS where title=?)",(BookID,title))
           if len(cursor.fetchall())!=0:
               cursor.execute("Select * from Books natural join copies where BookID=? and ISBN in (select ISBN from BOOKS where title=?)",(BookID,title))
               print("are you sure you want to deleate: (y/n)")
               resp=cursor.fetchall()
               print("ISBN: ",resp[0][0], " Title: ",resp[0][1]," Author: ",resp[0][2]," PublicationYear: ",resp[0][3], " Catagory: ",resp[0][4])
               ans=input()
               if ans=="y":
                   cursor.execute("delete from copies where bookid=? and ISBN in (select ISBN from BOOKS where title=?)",(BookID,title))
                   db.commit()
               else:
                   print("cancled")
           else:
               print("Title dosen't match bookID")
       else:
           print("invalid bookID")
   else:
       print("You are not authorized")

#Allows a user to check out a 
def CheckOutCoppie(token,title):
   if Verify(token,"CheckOutCoppie")==True:
       ##find sercher
       db=sqlite3.connect("Library.db")
       cursor=db.cursor()
       cursor.execute("select cred,ID from ACTIVE where token=?",(token,))
       ans=cursor.fetchone()
       SearcherTable=ans[0]
       ID=ans[1]
       ##find BookID
       cursor.execute("select BookID from copies where availability='yes' and ISBN in (Select ISBN from BOOKS where title=?)",(title,))
       ##get first available
       BookID=(cursor.fetchall())
       if str(BookID)!="[]":
           #update availability
           cursor.execute("update copies set availability='no' where bookID=?",(BookID[0][0],))
           #add to transactions
           #get new TransactionsID
           cursor.execute("Select max(transactionID) from Transactions")
           transactionID=cursor.fetchone()[0]+1
           #create quiery
           if SearcherTable == "stud":
               cursor.execute("insert into TRANSACTIONS (TransactionID, BookID, StudentID, BorrowDate) values (?,?,?,?)",(transactionID,BookID[0][0],ID,date.today()))
           elif SearcherTable == "fac":
               cursor.execute("insert into TRANSACTIONS (TransactionID, BookID, FacultyID, BorrowDate) values (?,?,?,?)",(transactionID,BookID[0][0],ID,date.today()))
           elif SearcherTable == "lib":
               cursor.execute("insert into TRANSACTIONS (TransactionID, BookID, LibrarianID, BorrowDate) values (?,?,?,?)",(transactionID,BookID[0][0],ID,date.today()))
           db.commit()
       else:
           print("This book can't be chekced out. There are either no copies available or we don't have this book")
       cursor.close()
       db.close()
   else:
       print("You are not authorized")

#Allows a user to return a book
def ReturnCopies(token):
   if Verify(token,"ReturnCopies")==True:
       #find UserGroup, ID
       db=sqlite3.connect("Library.db")
       cursor=db.cursor()
       cursor.execute("select cred,ID from ACTIVE where token=?",(token,))
       ans=cursor.fetchone()
       SearcherTable=ans[0]
       ID=ans[1]
       #Find pending transactions
       if SearcherTable == "stud":
           cursor.execute("Select TransactionID,BookID,BorrowDate from TRANSACTIONS where StudentID=? and ReturnDate is NULL",(ID,))
       elif SearcherTable == "fac":
           cursor.execute("Select TransactionID,BookID,BorrowDate from TRANSACTIONS where FacultyID=? and ReturnDate is NULL",(ID,))
       elif SearcherTable == "lib":
           cursor.execute("Select TransactionID,BookID,BorrowDate from TRANSACTIONS where LibrarianID=? and ReturnDate is NULL",(ID,))
       pending=cursor.fetchall()
       length=len(pending)
       Title=[]
       BorrowDate=[]
       for i in pending:
           BookID=i[1]
           cursor.execute("Select Title from copies Natural Join Books where BookID = ?",(BookID,))
           Title.append(cursor.fetchone()[0])
           BorrowDate.append(i[2])
       #prompt, which transaction to complete
       print("You have",length,"checked out Books")
       turnin=[]
       for i in range(length):
           print("Would You like to return",Title[i],"checked out on",BorrowDate[i],"(y/n)")
           ans=input()
           if ans=="y":
               turnin.append("y")
           else:
               turnin.append("n")
       #Update Transaction
       for i in range (length):
           if(turnin[i]=="y"):
               #return book
               print("Returning",Title[i],"checked out on",BorrowDate[i])
               cursor.execute("Update TRANSACTIONS set ReturnDate=? where TransactionID=?",(date.today(),pending[i][0]))
               #Update Copies
               cursor.execute("Update Copies set Availability='yes' where BookID=?",(pending[i][1],))
       db.commit()
       cursor.close()
       db.close()
   else:
       print("You are not authorized")      

#Allows a user to view their own borrowing history     
def viewBorrowingHistory(token):
   if Verify(token,"viewBorrowingHistory")==True:
       db=sqlite3.connect("Library.db")
       cursor=db.cursor()
       #find UserGroup, ID
       cursor.execute("select cred,ID from ACTIVE where token=?",(token,))
       ans=cursor.fetchone()
       SearcherTable=ans[0]
       ID=ans[1]
       #Find pending transactions
       if SearcherTable == "stud":
           cursor.execute("Select BookID,BorrowDate,ReturnDate from TRANSACTIONS where StudentID=?",(ID,))
       elif SearcherTable == "fac":
           cursor.execute("Select BookID,BorrowDate,ReturnDate from TRANSACTIONS where FacultyID=?",(ID,))
       elif SearcherTable == "lib":
           cursor.execute("Select BookID,BorrowDate,ReturnDate from TRANSACTIONS where LibrarianID=?",(ID,))
       history=cursor.fetchall()
       for i in history:
           BookID=i[0]
           cursor.execute("Select Title from Copies Natural Join Books where BookID = ?",(BookID,))      
           title=cursor.fetchall()[0][0]
           print("Title: %12s Borrow Date: %s Return Date: %s" % (title,i[1],i[2]))
       cursor.close()
       db.close()
   else:
       print("You are not authorized")

#Allows a user to search the database for all books with a certain title
def searchByTitle(token):
   if Verify(token,"Search")==True:
       db=sqlite3.connect("Library.db")
       cursor=db.cursor()
       print("What title are you looking for?")
       title = input()
       cursor = db.cursor()
       cursor.execute("SELECT * FROM BOOKS Where title=?",(title,))
       result = cursor.fetchall()
       isbn = result[0][0]
       cursor.execute("SELECT count(BookID) FROM COPIES where Availability=? AND ISBN=?",("yes",isbn))
       avail = cursor.fetchone()
       avail = str(avail)
       print("Title: "+result[0][1]+"\nISBN: "+isbn+"\nAuthor: "+result[0][2]+"\nPublication Year:"+str(result[0][3])+"\nCatagory: "+result[0][2]+"\nNumber of Copies Currently Available: "+avail[1])
       cursor.close()
       db.close()
   else:
       print("You are not authorized")

#Allows a user to see the BOOKS table joined with the COPIES table
def seeBooks(token):
   if Verify(token,"Search")==True:
       db=sqlite3.connect("Library.db")
       cursor=db.cursor()
       cursor = db.cursor()
       cursor.execute("SELECT * FROM BOOKS NATURAL JOIN COPIES")
       result = cursor.fetchall()
       for tuple in result:
        print(tuple)
       cursor.close()
       db.close()
   else:
       print("You are not authorized")

#Allows a user to search the database for all books with a certain author
def searchByAuthor(token):
   if Verify(token,"Search")==True:
       db=sqlite3.connect("Library.db")
       cursor=db.cursor()
       print("What author are you looking for?")
       author = input()
       cursor = db.cursor()
       cursor.execute("SELECT * FROM BOOKS Where Author=? Group by Title",(author,))
       result = cursor.fetchall()
       i = 0
       for tuple in result:
           isbn = result[i][0]
           cursor.execute("SELECT count(BookID) FROM COPIES where Availability=? AND ISBN=?",("yes",isbn))
           avail = cursor.fetchone()
           avail = str(avail)
           print("Title: "+result[i][1]+"\nISBN: "+isbn+"\nAuthor: "+result[i][2]+"\nPublication Year:"+str(result[i][3])+"\nCatagory: "+result[i][2]+"\nNumber of Copies Currently Available: "+avail[1]+"\n")
           i = i+1 
       cursor.close()
       db.close()
       if len(result)==0:
           print("No Author found")
   else:
       print("You are not authorized")

#Allows a user to search the database for books in a certain category
def searchByCatagory(token):
   if Verify(token,"Search")==True:
       db=sqlite3.connect("Library.db")
       cursor=db.cursor()
       print("What catagory are you looking for?")
       catagory = input()
       cursor = db.cursor()
       cursor.execute("SELECT * FROM BOOKS Where Catagory=? Group by Title",(catagory,))
       result = cursor.fetchall()
       i = 0
       for tuple in result:
           isbn = result[i][0]
           cursor.execute("SELECT count(BookID) FROM copies where Availability=? AND ISBN=?",("yes",isbn))
           avail = cursor.fetchone()
           avail = str(avail)
           print("Title: "+result[i][1]+"\nISBN: "+isbn+"\nAuthor: "+result[i][2]+"\nPublication Year:"+str(result[i][3])+"\nCatagory: "+result[i][2]+"\nNumber of Copies Currently Available: "+avail[1]+"\n")
           i = i+1 
       cursor.close()
       db.close()
   else:
       print("You are not authorized")

#returns true if a book is overdue and false if it is not
def overDue(transactionId):
   dueDate = (getDueDate(transactionId))
   curDate = date.today()

   db = sqlite3.connect('Library.db')
   cursor = db.cursor()
   cursor.execute("SELECT ReturnDate FROM TRANSACTIONS Where TransactionID =?", (transactionId,))
   result = cursor.fetchall()
   Rdate = result[0][0]

   if(dueDate<curDate and Rdate != None):
       return True
   else:
       return False

#returns the duedate pf a spesific book
def getDueDate(transactionId):
   db = sqlite3.connect('Library.db')
   cursor = db.cursor()
   cursor.execute("SELECT BorrowDate, StudentID FROM TRANSACTIONS Where TransactionID =?", (transactionId,))
   result= cursor.fetchall()
   theDate = date.fromisoformat(result[0][0])
   if(result[0][1] == None):
       dueDate = theDate + timedelta(365)
   else:
       dueDate = theDate + timedelta(90)
   cursor.close()
   return dueDate

#Allows an authorised user to add a sudent
def AddStudent(token):
    if Verify(token,"addUser")==True:
        db=sqlite3.connect('Library.db')
        cursor=db.cursor()
        print("Enter the ID")
        id = input()
        print("Enter the name")
        name = input()
        print("Enter the email")
        email = input()
        print("Enter the department")
        department = input()
        #Creates a new entry in the STUDENTS table with the inputed user data
        cursor.execute("insert into STUDENTS (ID, name, email, department) VALUES(?, ?, ?, ?)",(id,name,email,department))
        db.commit() 
        db.close() 
    else:
        print("You are not authorized")

#Allows an authorised user to add a faculty
def AddFaculty(token):
    if Verify(token,"addUser")==True:
        db=sqlite3.connect('Library.db')
        cursor=db.cursor()
        print("Enter the ID")
        id = input()
        print("Enter the name")
        name = input()
        print("Enter the email")
        email = input()
        print("Enter the department")
        department = input()
        cursor.execute("insert into FACULTY (ID, name, email, department) VALUES(?, ?, ?, ?)",(id,name,email,department))
        db.commit() 
        db.close()
    else:
        print("You are not authorized")

#Allows an authorised user to add a librarian
def AddLibrarian(token):
    if Verify(token,"addUser")==True:
        db=sqlite3.connect('Library.db')
        cursor=db.cursor()
        print("Enter the ID")
        id = input()
        print("Enter the name")
        name = input()
        print("Enter the email")
        email = input()
        cursor.execute("insert into LIBRARIANS (ID, name, email) VALUES(?, ?, ?)",(id,name,email))
        db.commit() 
        db.close() 
    else:
        print("You are not authorized") 

#Creates a csv file with the columns: title, bookID, available
def generateAvailabilityReport(token,fileName):
   if Verify(token,"GenerateReport")==True:
       db = sqlite3.connect('Library.db')
       file = open(fileName+".csv", 'x')
       file.write("Title,BookID,Available \n")
       cursor = db.cursor()
       cursor.execute("SELECT Title, BookID, Availability FROM BOOKS NATURAL JOIN COPIES")
       result = cursor.fetchall()
       i = 0
       for tuple in result:
           title = result[i][0]
           bookId = result[i][1]
           availability = result[i][2]
           i = i+1 
           row = title+","+str(bookId)+","+availability+"\n"
           file.write(row)
       file.close()
       cursor.close()
   else:
       print("You are not authorized")

#Creates a csv file with the columns: Title, BookID, DueDate
def generateOverdueBookReport(token,fileName):
   if Verify(token,"GenerateReport")==True:
       file = open(fileName+".csv", 'x')
       file.write("Title, BookID, DueDate")
       db = sqlite3.connect('Library.db')
       cursor = db.cursor()
    #Retreive the title, bookID, and transaction ID from the transactions, COPIES, and books tables
       cursor.execute("SELECT Title, TRANSACTIONS.BookID, TransactionID FROM TRANSACTIONS NATURAL JOIN COPIES NATURAL JOIN BOOKS")
       result = cursor.fetchall()
       i = 0
    #For each tuple, write the results to the file
       for tuple in result:
        title = result[i][0]
        bookId = result[i][1]
        transactionId = result[i][2]
        if(overDue(transactionId)):
          date = getDueDate(transactionId)
          row = title+","+str(bookId)+","+date.strftime("%x")+"\n"
          file.write(row)  
        i = i+1   
       file.close()
       cursor.close()
   else:
       print("You are not authorized")
  
#Creates a csv file with the columns:Most popular titles, most popular catagories, most popular authors
def generateTrendsReport(token,fileName):
   if Verify(token,"GenerateReport")==True:
       db = sqlite3.connect('Library.db')
       file = open(fileName+".csv", 'x')
       cursor = db.cursor()
       cursor.execute("SELECT Title, count(*) FROM TRANSACTIONS NATURAL JOIN COPIES NATURAL JOIN BOOKS group by ISBN ORDER by count(*) DESC LIMIT 3")
       titles = cursor.fetchall()
       cursor.execute("SELECT Author, count(*) FROM TRANSACTIONS NATURAL JOIN COPIES NATURAL JOIN BOOKS group by Author ORDER by count(*) DESC LIMIT 3")
       authors = cursor.fetchall()
       cursor.execute("SELECT Catagory, count(*) FROM TRANSACTIONS NATURAL JOIN COPIES NATURAL JOIN BOOKS group by Catagory ORDER by count(*) DESC LIMIT 3")
       catagories = cursor.fetchall()
       file.write("Popular Titles,Times Borrowed,Popular Authors, Popular Catagories \n")
       i = 0
       print(titles)
       while(i<3):
           title = titles[i][0]
           countT = titles[i][1]
           author = authors[i][0]
           catagory = catagories[i][0]
           i = i+1 
           row = title+","+str(countT)+","+author+","+catagory+","+"\n"
           file.write(row)
       file.close()
       cursor.close()
       db.close()
   else:
       print("You are not authorized")

#Checks the permissions of the token
def Verify(token,transaction):
   
   db=sqlite3.connect("Library.db")
   cursor=db.cursor()
   cursor.execute('Select cred from ACTIVE where token=?',(token,))
   cred=str(cursor.fetchall())[3:7]
   cursor.close()
   db.close()
   privledges=[]
   if cred=="stud":
       privledges=["CheckOutCoppie","ReturnCopies","Search","viewBorrowingHistory"] ##stud privledges
   if cred == "fac'":
       privledges=["CheckOutCoppie","ReturnCopies","Search","viewBorrowingHistory"] ##fac' privelges
   if cred =="lib'":
       privledges=["LibrarianAddBook","LibrarianRemoveBook","CheckOutCoppie","ReturnCopies","Search","viewBorrowingHistory","GenerateReport","addUser"] ##lib' privlges
   if transaction in privledges:
       return True
   else:
       return False
   
