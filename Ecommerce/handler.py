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


@app.route('/placeOrder', methods = ['POST'])
def placeOrder():
   #print("buy button pressed")
   if 'username' in session:
      order = 10
      return render_template("orderPage.html", order = order)
   else:
      return render_template("loginPage.html")


if __name__ == '__main__':
   app.run()