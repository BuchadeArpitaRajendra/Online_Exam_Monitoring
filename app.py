from flask import Flask,render_template,request
import sqlite3

app= Flask(__name__)
#home route
@app.route("/")
def home():
    return "Welcome to Online Exam Monitoring System"

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method =="GET":
        return render_template("register.html")
    candidate_id=request.form["candidate_id"]
    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]
    connection=sqlite3.connect("exam.db")
    cursor=connection.cursor()
    cursor.execute("""
    INSERT INTO candidate(candidate_id,name,email,password) VALUES (?,?,?,?)
    """,(candidate_id,name,email,password))
    connection.commit()
    connection.close()
    return "Registration successful"
#run application
if __name__== "__main__":
    app.run(debug=True)