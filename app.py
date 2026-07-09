from flask import Flask,render_template,request
import sqlite3
import re

app= Flask(__name__)
#home route
@app.route("/")
def home():
    print("Welcome to Online Exam Monitoring System")
    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method =="GET":
        return render_template("register.html")
    candidate_id=request.form["candidate_id"]
    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]

    #validation
    errors = []

    if candidate_id == "":
        errors.append("Candidate ID is required.")

    if name == "":
        errors.append("Name is required.")

    if email == "":
        errors.append("Email is required.")

    if password == "":
        errors.append("Password is required.")

    #Email Validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if email != "" and re.match(pattern, email) is None:
        errors.append("Invalid email format.")

    if errors:
        return render_template("register.html", errors=errors)

    connection=sqlite3.connect("exam.db")
    cursor=connection.cursor()

    #Duplicate Email Check
    cursor.execute("SELECT * FROM candidate WHERE email=?",(email,))
    user=cursor.fetchone()

    if user:
        
        return render_template("register.html", message="Email Already Registered")

    cursor.execute("""
    INSERT INTO candidate(candidate_id,name,email,password) VALUES (?,?,?,?)
    """,(candidate_id,name,email,password))
    connection.commit()
    connection.close()
    return render_template("login.html")


@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="GET":
        return render_template("login.html")


    email=request.form["email"]
    password=request.form["password"]


    connection=sqlite3.connect("exam.db")
    cursor=connection.cursor()

    cursor.execute("""
    SELECT name,email
    FROM candidate
    WHERE email=? AND password=?
    """,(email,password))

    user=cursor.fetchone()

    connection.close()

    if user:

        return render_template("dashboard.html", name=user[0])

    else:

        return render_template("login.html",message="Invalid Email or Password")

#run application
if __name__== "__main__":
    app.run(debug=True)