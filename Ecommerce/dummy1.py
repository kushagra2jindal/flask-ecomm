import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

def showData(conn):
    conn.row_factory = sqlite3.Row
   
    cur = conn.cursor()
    cur.execute("select * from item_ecom")
    
    rows = cur.fetchall()
    for row in rows:
        print (row['id'])

showData(conn)