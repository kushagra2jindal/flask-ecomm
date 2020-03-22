import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")


def deleteTables(conn):
    try:
        conn.execute('drop table item_ecom')
        conn.execute('drop table Order_ecom')
        conn.execute('drop table customer_ecom')
        print ("tables are dropped")
    except:
        print("all tables are not able to dropped")


def createTables(conn):
    try:
        conn.execute('CREATE TABLE item_ecom (id INT, name TEXT, quantity INT, price INT)')
        print ("item Table created successfully")
    except:
        print ("item table already exists")


    try:
        conn.execute('CREATE TABLE Order_ecom (id INT, username TEXT, quantity INT, amount INT)')
        print ("order Table created successfully")
    except:
        print ("order table already exists")

    try:
        conn.execute('CREATE TABLE customer_ecom (username TEXT, pass TEXT, name TEXT, email TEXT, phno INT, address TEXT)')
        print ("customer Table created successfully")
    except:
        print ("customer table already exists")


def insertData(conn):
    # inserting dummy data in the tables.
    cur = conn.cursor()

    # inserting dummy data in item table        
    cur.execute("INSERT INTO item_ecom (id,name,quantity,price) VALUES (?,?,?,?)",(1,"apple",10,250) )
    cur.execute("INSERT INTO item_ecom (id,name,quantity,price) VALUES (?,?,?,?)",(2,"Orange",5,100) )
    print ("dummy data inserted in item table")

    # inserting dummy data in order table 
    # Not needed       

    # inserting dummy data in customer table        
    cur.execute("INSERT INTO customer_ecom (username,pass,name,email,phno,address) VALUES (?,?,?,?,?,?)",("kushagra2jindal","1234","kushagra","kushagra2jindal@gmail.com",1234567890,"park road,dehradun") )
    print ("dummy data inserted in customer table")


def showData(conn):
    conn.row_factory = sqlite3.Row
   
    cur = conn.cursor()
    cur.execute("select * from item_ecom")
    
    rows = cur.fetchall()
    for row in rows:
        print (row['id'])
    



deleteTables(conn)
createTables(conn)
insertData(conn)
showData(conn)


conn.commit()
conn.close