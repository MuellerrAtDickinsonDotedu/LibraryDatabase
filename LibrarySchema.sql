-- drop table TRANSACTIONS;
-- drop table LIBRARIANLogin;
-- drop table LIBRARIANS;
-- drop table FACULTYLogin;
-- drop table FACULTY;
-- drop table STUDENTLogin;
-- drop table STUDENTS;
-- drop table COPIES;
-- drop table BOOKS;
-- drop table ACTIVE;


create table COPIES (
  BookID int,
  ISBN varchar(13) REFERENCES BOOKS(ISBN),
  Availability varChar(3),
  primary key (BookID),
  check (Availability in ("yes","no"))
);


create table BOOKS (
  ISBN varChar(13),
  Title varChar(50),
  Author varChar (50),
  PublicationYear varChar(4),
  Catagory varChar(16),
  Check (ISBN like '_____________')
  primary key (ISBN)
);


create table STUDENTS (
  ID int,
  Name varChar(50),
  Email varChar(50),
  Department varChar(50),
  primary key (ID)
);


create table STUDENTLogin(
  Username varchar(50),
  Password varchar(50),
  ID REFERENCES Students(ID),
  primary key ( Username)
);


create table FACULTY (
  ID int,
  Name varChar(50),
  Email varChar(50),
  Department varChar(50),
  primary key (ID)
);


create table FACULTYLogin(
  Username varchar(50),
  Password varchar(50),
  ID REFERENCES faculty(ID),
  primary key (Username)
);


create table LIBRARIANS (
  ID int,
  Name varChar(50),
  Email varChar(50),
  primary key (ID)
);


create table LIBRARIANLogin(
  Username varchar(50),
  Password varchar(50),
  ID REFERENCES Librarians(ID),
  primary key (Username)
);


create table TRANSACTIONS (
  TransactionID int,
  BookID int REFERENCES COPIES(BookID),
  StudentID int REFERENCES STUDENTS(ID),
  FacultyID int REFERENCES FACULTY(ID),
  LibrarianID int REFERENCES LIBRARIANS(ID),
  BorrowDate varChar(10),
  ReturnDate varChar(10),
  primary key (TransactionID),
  check (BorrowDate like "____-__-__"),
  check (ReturnDate like "____-__-__")
);


create table ACTIVE (
  token int,
  cred varchar(3),
  ID int,
  timestamp,
  primary key (token)
  check (cred in ("stud","fac","lib"))
);


insert into BOOKS (ISBN, Title, Author, PublicationYear, Catagory)
VALUES
('0000000000012', 'Book0', 'Author0',1990,'science'),
('1111111111111', 'Book1', 'Author1',1991,'history'),
('2222222222222', 'Book2', 'Author2',1992,'fantasy'),
('3333333333333', 'Book3', 'Author3',1993,'fantasy'),
('4444444444444', 'Book4', 'Author4',1994,'mystery'),
('5555555555555', 'Book5', 'Author5',1995,'science'),
('6666666666666', 'Book6', 'Author6',1996,'mystery'),
('7777777777777', 'Book7', 'Author7',1997,'science'),
('8888888888888', 'Book8', 'Author8',1998,'science'),
('9999999999999', 'Book9', 'Author9',1999,'cooking');


insert into  COPIES(BookID, ISBN, Availability)
VALUES
(0,'0000000000012','yes'),
(1,'0000000000012','yes'),
(2,'0000000000012','no'),
(3,'0000000000012','no'),
(4,'1111111111111','yes'),
(5,'1111111111111','yes'),
(6,'1111111111111','no'),
(7,'2222222222222','yes'),
(8,'3333333333333','no'),
(9,'4444444444444','no'),
(10,'5555555555555','yes'),
(11,'6666666666666','no'),
(12,'7777777777777','yes'),
(13,'8888888888888','no'),
(14,'9999999999999','yes');


insert into FACULTY (ID, name, email, department)
VALUES
(0,'prof0','0@dickinson.edu','math'),
(1,'prof1','1@dickinson.edu','math'),
(2,'prof2','2@dickinson.edu','math');


insert into FACULTYLogin (Username, Password, ID)
VALUES
("prof0", "0", "0"),
("prof1", "1", "1"),
("prof2", "2", "2");


insert into STUDENTS (ID, name, email, department)
VALUES
(0,'Stud0','0@dickinson.edu','math'),
(1,'Stud1','1@dickinson.edu','math'),
(2,'Stud2','2@dickinson.edu','math');


insert into LIBRARIANS (ID, name, email)
VALUES
(0,"Librarian0","0@dickinson.edu"),
(1,"Librarian1","1@dickinson.edu"),
(2,"Librarian2","2@dickinson.edu");


Insert into transactions (TransactionID, BookID, StudentID, FacultyID, LibrarianID, BorrowDate, ReturnDate)
VALUES
(1,4,0,NULL,NULL,"2020-06-05",NULL),
(2,7,1,NULL,NULL,"2020-07-05","2020-05-06"),
(4,5,NULL,1,NULL,"2020-05-05","2020-05-06"),
(6,6,NULL,NULL,1,"2020-05-05",NULL),
(7,7,NULL,0,NULL,"2020-06-06","2020-06-07"),
(8,7,NULL,NULL,0,"2020-07-07","2020-07-08"),
(9,7,1,NULL,NULL,"2020-08-08","2020-08-09");


insert into STUDENTLogin (Username, Password, ID)
VALUES
("stud0", "0", "0"),
("stud1", "1", "1"),
("stud2", "2", "2");


insert into LIBRARIANLogin (Username, Password, ID)
VALUES
("lib0", "0", "0"),
("lib1", "1", "1"),
("lib2", "2", "2");


insert into ACTIVE (token,cred,id)
VALUES
(0,'stud',0),
(1,'fac',0),
(2,'lib',0);
