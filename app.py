from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3
import re
import cv2
import os
from datetime import datetime
import subprocess
import sys 


app= Flask(__name__)
app.secret_key = "exam_secret_key"
face_process=None

#home route
@app.route("/")
def home():
    print("Welcome to Online Exam Monitoring System")
    return render_template("login.html")

def capture_photo(candidate_id):

    camera = cv2.VideoCapture(0)

    while True:

        success, frame = camera.read()

        if not success:
            break

        cv2.imshow("Press C to Capture Photo", frame)

        key = cv2.waitKey(1)

        if key == ord('c'):
            break

    if not os.path.exists("photos"):
        os.makedirs("photos")

    photo_path = f"photos/{candidate_id}.jpg"

    cv2.imwrite(photo_path, frame)

    camera.release()

    cv2.destroyAllWindows()

    return photo_path





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
    
    photo_path = capture_photo(candidate_id)


    cursor.execute("""
    INSERT INTO candidate
    (candidate_id,name,email,password,photo_path)
    VALUES(?,?,?,?,?)
    """,
    (candidate_id,name,email,password,photo_path))

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
    SELECT candidate_id,name
    FROM candidate
    WHERE email=? AND password=?
    """,(email,password))

    user=cursor.fetchone()

    connection.close()

    if user:
        session["candidate_id"] = user[0]
        session["name"] = user[1]

        return render_template("dashboard.html", name=user[1])

    else:

        return render_template("login.html",message="Invalid Email or Password")
    
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
    
@app.route("/start_exam")
def start_exam():
    # subprocess.Popen(["python","face_detection.py"])
    # global face_process
    BASE_DIR = os.getcwd()
    STOP_FILE = os.path.join(BASE_DIR, "stop_exam.txt")

    # Delete old stop file
    if os.path.exists(STOP_FILE):
        os.remove(STOP_FILE)
        print("Old stop file removed")

    candidate_id = session["candidate_id"]

    subprocess.Popen([
        sys.executable,
        "face_detection.py",
        str(candidate_id)
    ])
    
    connection = sqlite3.connect("exam.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status
        FROM session
        WHERE session_id=(
            SELECT MAX(session_id)
            FROM session
            WHERE candidate_id=?
        )
    """,(candidate_id,))

    result = cursor.fetchone()

    if result:

        if result[0] in ["Started","Running","Paused"]:

            connection.close()

            return """
            <h2>Exam already started.</h2>

            <a href='/dashboard'>
            <button>Back to Dashboard</button>
            </a>
            """

    start_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""

        INSERT INTO session

        (candidate_id,start_time,status)

        VALUES(?,?,?)

    """,(candidate_id,start_time,"Running"))

    connection.commit()

    connection.close()

    return """
    <h2>Exam Started Successfully</h2>

    <a href='/dashboard'>
    <button>Back to Dashboard</button>
    </a>
    """
   


@app.route("/pause_exam")
def pause_exam():

    candidate_id=session["candidate_id"]

    connection=sqlite3.connect("exam.db")
    cursor=connection.cursor()

    cursor.execute("""

    SELECT session_id,status

    FROM session

    WHERE session_id=(

    SELECT MAX(session_id)

    FROM session

    WHERE candidate_id=?

    )

    """,(candidate_id,))

    result=cursor.fetchone()

    if result is None:

        connection.close()

        return """
        <h2>Please start the exam first.</h2>

        <a href='/dashboard'>
        <button>Back to Dashboard</button>
        </a>
        """

    if result[1]=="Paused":

        connection.close()

        return """
        <h2>Exam is already paused.</h2>

        <a href='/dashboard'>
        <button>Back to Dashboard</button>
        </a>
        """

    if result[1]=="Completed":

        connection.close()

        return """
        <h2>Exam has already ended.</h2>

        <a href='/dashboard'>
        <button>Back to Dashboard</button>
        </a>
        """

    cursor.execute("""

    UPDATE session

    SET status=?

    WHERE session_id=?

    """,("Paused",result[0]))

    connection.commit()

    connection.close()

    return """
    <h2>Exam Paused Successfully</h2>

    <a href='/dashboard'>
    <button>Back to Dashboard</button>
    </a>
    """

@app.route("/resume_exam")
def resume_exam():

    candidate_id=session["candidate_id"]

    connection=sqlite3.connect("exam.db")
    cursor=connection.cursor()

    cursor.execute("""

    SELECT session_id,status

    FROM session

    WHERE session_id=(

    SELECT MAX(session_id)

    FROM session

    WHERE candidate_id=?

    )

    """,(candidate_id,))

    result=cursor.fetchone()

    if result is None:

        connection.close()

        return """
        <h2>Please start the exam first.</h2>

        <a href='/dashboard'>
        <button>Back to Dashboard</button>
        </a>
        """

    if result[1]!="Paused":

        connection.close()

        return """
        <h2>Exam is not paused.</h2>

        <a href='/dashboard'>
        <button>Back to Dashboard</button>
        </a>
        """

    cursor.execute("""

    UPDATE session

    SET status=?

    WHERE session_id=?

    """,("Running",result[0]))

    connection.commit()

    connection.close()

    return """
    <h2>Exam Resumed Successfully</h2>

    <a href='/dashboard'>
    <button>Back to Dashboard</button>
    </a>
    """


@app.route("/end_exam")
def end_exam():
    with open("stop_exam.txt", "w") as f:
        f.write("stop")

    # global face_process

    # if face_process is not None:
    #     face_process.terminate()      # Stop face_detection.py
    #     face_process.wait()           # Wait until it exits
    #     face_process = None

    candidate_id=session["candidate_id"]

    connection=sqlite3.connect("exam.db")
    cursor=connection.cursor()

    cursor.execute("""

    SELECT session_id,status

    FROM session

    WHERE session_id=(

    SELECT MAX(session_id)

    FROM session

    WHERE candidate_id=?

    )

    """,(candidate_id,))

    result=cursor.fetchone()

    if result is None:

        connection.close()

        return """
        <h2>Please start the exam first.</h2>

        <a href='/dashboard'>
        <button>Back to Dashboard</button>
        </a>
        """

    if result[1]=="Completed":

        connection.close()

        return """
        <h2>Exam already completed.</h2>

        <a href='/dashboard'>
        <button>Back to Dashboard</button>
        </a>
        """

    end_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""

    UPDATE session

    SET

    end_time=?,

    status=?

    WHERE session_id=?

    """,(end_time,"Completed",result[0]))

    connection.commit()

    connection.close()

    return """
    <h2>Exam Completed Successfully</h2>

    <a href='/dashboard'>
    <button>Back to Dashboard</button>
    </a>
    """

@app.route("/browser_event", methods=["POST"])
def browser_event():

    data = request.get_json()

    event_type = data["event_type"]
    remarks = data["remarks"]

    candidate_id = session.get("candidate_id")     # Candidate logged in

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = sqlite3.connect("exam.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO event_log
        (candidate_id, event_type, timestamp, remarks)
        VALUES (?, ?, ?, ?)
    """, (
        candidate_id,
        event_type,
        timestamp,
        remarks
    ))

    connection.commit()
    connection.close()

    return {"message": "Event Logged"}


#run application
if __name__== "__main__":
    app.run(debug=True)