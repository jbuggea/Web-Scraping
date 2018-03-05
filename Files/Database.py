'''
This code creates the sqlite database that I will populate with data scraped from finds.org.uk 
'''

import sqlite3
import sys
import os
#I find it helpful to check the current working directory, as I am only just about getting confident with the manipulation of directory paths
retval = os.getcwd()
print(retval)

try:
    
    #First, connect to the database. It will create it if it does not exist
    con = sqlite3.connect('Finds.db')
    con.text_factory = str
    #You get the cursor, which allows you access to the database and tables within
    cur = con.cursor()  
   
    #This is the first SQL set of commands. First, the Drop command is run then CREATE. This creates four columns, a mixture of Blob and Text
    cur.executescript("""
        DROP TABLE IF EXISTS Finds;
        CREATE TABLE Finds (ObjectID Text, Object Text, Image BLOB, ImageRef Text
        );
        """)
    #this commits the changes to the table
    con.commit()
    rows = cur.fetchall()
finally:
    
    if con:
        con.close() 
            