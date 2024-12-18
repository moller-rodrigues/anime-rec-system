import sqlite3 # Imports the sqlite3 library which is an embedded relational database management system
import os

project_folder = os.getcwd()
DATA_FOLDER = project_folder+'/Data/'

with sqlite3.connect(DATA_FOLDER+"Accounts.db") as db: # Connects to the database, 'Accounts.db', if it doesn't exist then it is created
    cursor = db.cursor() # Creates a cursor object which is used to traverse the database
    
## Executes a sql query on the database which creates a table called 'user' with the fields: 'userID','username','firstname','surname' and 'password',
## if they do not already exist. 
cursor.execute( '''
CREATE TABLE IF NOT EXISTS user(
userID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
firstname VARCHAR(20) NOT NULL,
surname VARCHAR(20) NOT NULL,
password VARCHAR(20) NOT NULL,
highscore INTEGER,
favourites TEXT);
''')

db.commit() # Makes changes made to the database permanent

cursor.execute("SELECT * FROM user") # Selects all the data from the table 'user'

db.close() # Closes the connection to 'Accounts.db' so that it can be accesed by other processes; avoiding locking of the database.










