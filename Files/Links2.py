'''
This module contains many key components. First it iterates over website links and scrapes relevant information, 
then inserts this information into the previously established database. Within the same for loop, the images, if any, 
are then iterated over and saved to a specific folder. I insert ImageRef into the database - this has the same name 
as the saved image file, and so will allow it to match up correctly.  
'''

import csv
import requests
import urllib2 
import sqlite3
import sys
from bs4 import BeautifulSoup
import time
import os

try: buffer = buffer
except NameError:
    buffer = lambda x: x 
    
pn2=os.path.abspath('../Files')
path2 = os.path.join(pn2, 'static')
path3 = os.path.join(path2, 'images')

def U(literal_string):
    if hasattr(literal_string, 'decode'):
        return literal_string.decode('utf-8') 
        # source code encoding
    return literal_string

con = sqlite3.connect('Finds.db')
con.text_factory = str
#You get the cursor, which allows you access to the db and tables within
cur = con.cursor()  
   
ObjectDescription=[]
urls=[]

for i in range(5):      # Number of pages plus one 
    #This iterates over the first five pages of search results from finds.org.uk - each page has 20 results, giving 100 in total
    url = 'https://finds.org.uk/database/search/results/page/{}'.format(i)
    r = requests.get(url)
    #This opens the main url, then finds all links related to an object i.e. the search results
    soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")

    links = soup.findAll('div',attrs={"typeof":"crm:E22_Man-Made_Object"})
    #This prints the links, to check it is working correctly
    for link in links:
        theLink=link["about"]  
        print(theLink)
        urls.append(theLink)
        
for url in urls:
    soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
    #get the main topic, which should be the object in this link
    obj= soup.find('h1').getText()
    print (obj)
    #now get the pas description about the object
    text=soup.find("div",attrs={"property":"pas:description"})

    #get rid of the html tags and just get the one between <p>
    try:
        finalText=text.find('p').getText()
    #in case of exceptions, code will still run
    except:
        pass
    #The following two lines check the values can be considered by SQLITE
    mystring=finalText.encode('utf8')
    string=str(mystring)
    #print the final result
    print(finalText)
    #These two, title and span, are different ways of getting the unique record ID. This was to differentiate each image; initially i was just using the object, however two coin images for example overwrote each other.
    spans = soup.find('span', attrs={"class" :"fourfigure"})
    title= soup.find('title').getText()
    stitle= str(title)
    #print(title)
    #finalText2=spans.find('div').getText()
    #print(finalText2)
    sspans=str(spans)
    ObjectDescription.append(mystring)
    cur.execute("INSERT INTO Finds (Object, ObjectID) VALUES (?, ?);", (string, sspans ))
    #The commands given are executed
    con.commit()
    timestamp = time.asctime() 
    #finds image links
    links = soup.findAll('img')
    for link in links:
    
        #get the current time - not actually used in my code in the end, but I felt it very useful to call upon initially
        timestamp = time.asctime() 
    
        #get the link that is in src (i.e., an image from html)
        link = link["src"].split("src=")[-1]
        if "https://finds.org.uk/images/" not in link:
            continue
        if "thumbnails" in link:
            continue
        
    
        #print the link (i.e., should be the correct image link)
        print(link)   

        #now get the data using the urllib2 library 
        download_img = urllib2.urlopen(link)
        #Filename for jpg file created  - this is the record id for each image
        filename='%s.jpg' % stitle
        sfilename=str(filename)
        #this directs the image stream to a particular path
        filepath=os.path.join(path3, filename)
        
        txt = open(filepath, "wb")
    
        #write the binary data
        txt.write(download_img.read())
        #this inserts the image reference (same name as image file) into the database, allowing it to load with the correct description
        cur.execute("UPDATE Finds SET ImageRef=? Where ObjectID=?;", (sfilename, sspans, ))
        con.commit()
        txt.close()
        txt.close()
