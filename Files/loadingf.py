'''
This loads the database in conjunction with a html template 
'''
from flask import Flask, render_template, request
import sqlite3 as sql
import sys
reload(sys)
  
app = Flask(__name__)
@app.route('/')
@app.route('/list')
def list():
    con = sql.connect('Finds.db')
    #selects rows
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from Finds limit 10")
    #cur.execute("Select Object, Image from Finds")
    rows = cur.fetchall();
    #connects to established template
    return render_template("template.html",rows = rows)

if __name__ == '__main__':
    app.run(debug = True)