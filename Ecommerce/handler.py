from flask import Flask,render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret key"


@app.route('/')
def showInput():
   conn = sqlite3.connect('database.db')
   print ("Opened database successfully")
   conn.row_factory = sqlite3.Row
   
   cur = conn.cursor()
   cur.execute("select * from item_ecom")
    
   rows = cur.fetchall()
   conn.close

   username = ""
   if 'username' in session:
      username = session['username']

   return render_template("home.html",rows = rows, username = username)


@app.route('/loginPage')
def loginPageLoad():
   return render_template("loginPage.html")


@app.route('/logoutPage')
def logoutPageLoad():
   session.pop('username', None)
   return render_template("logoutPage.html")


@app.route('/login',methods = ['POST'])
def login():
   user = request.form['username']
   password = request.form['password']
   success = 0

   conn = sqlite3.connect('database.db')
   print ("Opened database successfully")
   conn.row_factory = sqlite3.Row
   
   cur = conn.cursor()
   cur.execute("select username,pass from customer_ecom")
    
   rows = cur.fetchall()

   for row in rows:
      if (row["username"] == user) and (row["pass"] == password):
         print ("Login is successfull")
         success = 1
         break

   conn.close

   if(success == 1):
      session['username'] = user
      #return "logined"
      return redirect(url_for('showInput'))
   else:
      #return " not logined"
      return redirect(url_for('registerPageLoad'))


@app.route('/registerPage')
def registerPageLoad():
   return render_template("registrationPage.html")


@app.route('/register',methods = ['POST'])
def register():

   try:
      user = request.form['username']
      password = request.form['password']
      name = request.form['name']
      email = request.form['email']
      phno = request.form['phno']
      add = request.form['add']

      conn = sqlite3.connect('database.db')
      print ("Opened database successfully")
      
      cur = conn.cursor()

      cur.execute("INSERT INTO customer_ecom (username,pass,name,email,phno,address) VALUES (?,?,?,?,?,?)",(user,password,name,email,phno,add))
      conn.row_factory = sqlite3.Row
      conn.commit()
      return redirect(url_for('loginPageLoad'))
   
   except:
      conn.rollback()
      return redirect(url_for('registerPageLoad'))

   finally:
      conn.close


@app.route('/orderPage')
def loginOrderLoad():
   return render_template("orderPage.html")


@app.route('/placeOrder')
def placeOrder():
   #print("buy button pressed")
   if 'username' in session:
      conn = sqlite3.connect('database.db')
      conn.row_factory = sqlite3.Row
   
      cur = conn.cursor()

      cur.execute("select * from cart_ecom")
      rows = cur.fetchall()
      
      amount = 0
      quantity = 0

      for row in rows:
         if(row['username'] == session['username']):
            amount = amount + (row['price']*row['quantity'])
            quantity = quantity + 1

      # why do we needed an extra comma here?
      cur.execute("delete from cart_ecom where username=?",(session['username'],))
      conn.row_factory = sqlite3.Row
      conn.commit()

      cur.execute("select * from order_ecom")
      rows = cur.fetchall()
      order = 0

      for row in rows:
         order = row['id']
         print (order)

      order = order + 1

      cur.execute("INSERT INTO order_ecom (id,username,quantity,amount) VALUES (?,?,?,?)",(order,session['username'],quantity,amount))
      conn.row_factory = sqlite3.Row

      conn.commit()

      conn.close

      #print (order)
      return render_template("orderPage.html", order = order, amount = amount)

   else:
      return render_template("loginPage.html")

@app.route('/addToCart')
def addTOCart():

   if 'username' in session:

      itemId = request.args.get('itemId')
      #print (itemId)

      conn = sqlite3.connect('database.db')
      conn.row_factory = sqlite3.Row
      cur = conn.cursor()
      cur.execute("select * from item_ecom")
      
      rows = cur.fetchall()

      for row in rows:
         id = row['id']
         itemId = int(itemId)
         if(id == itemId):
            amount = row['price']
            quantity = row['quantity'] - 1
            name = row['name']
            cur.execute("update item_ecom set quantity=? where id=?",(quantity,row['id']))
            conn.commit()
            break
         
      cur.execute("select * from cart_ecom where username = ? and id = ?", (session['username'],itemId))
      rows = cur.fetchall()
      quantity = 0
      for row in rows:
         quantity = row['quantity']
      #print (len(rows))

      quantity = quantity + 1
      if(len(rows) > 0):
         cur.execute("update cart_ecom set quantity = ? where username = ? and id = ?", (quantity,session['username'],itemId))
      else:
         cur.execute("INSERT INTO cart_ecom (username,id,name,quantity,price) VALUES (?,?,?,?,?)",(session['username'],itemId,name,1,amount) )
      
      conn.commit()
      
      conn.close

      return redirect(url_for("showInput"))

   else:
      return render_template("loginPage.html")


@app.route('/showCart')
def showCart():
   conn = sqlite3.connect('database.db')
   conn.row_factory = sqlite3.Row
   cur = conn.cursor()
   cur.execute("select * from cart_ecom")

   username = session['username']

   rows = cur.fetchall()
   #print (len(rows))

   return render_template("Cart.html",username = username,rows = rows,count = len(rows))


if __name__ == '__main__':
   app.run()