import sqlite3

connection=sqlite3.connect("exam.db")

curser= connection.cursor()

candidate_table="""
CREATE TABLE IF NOT EXISTS candidate(
    candidate_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    photo_path TEXT  
)
"""


session_table="""
CREATE TABLE IF NOT EXISTS session(
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id TEXT NOT NULL,
    start_time TEXT,
    end_time TEXT,
    status TEXT ,
    FOREIGN KEY (candidate_id) REFERENCES candidate(candidate_id)
)
"""
curser.execute(candidate_table)
curser.execute(session_table)
connection.commit()
connection.close()
print("Database and tables created successfully.")