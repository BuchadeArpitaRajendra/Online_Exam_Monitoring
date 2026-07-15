import cv2
import os
import sqlite3
import time
from datetime import datetime

# Load the Haar Cascade classifier
face_cascade = cv2.CascadeClassifier(
    
"haarcascade\haarcascade_frontalface_default.xml"
)

photo_folder = "photos1"

if not os.path.exists(photo_folder):
    os.makedirs(photo_folder)

# candidate_id=session["candidate_id"]
candidate_id="C1003"
# Open the webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Unable to access webcam.")
    exit()

print("Press 'Q' to exit.")

def log_event(candidate_id, event_type, remarks):

    connection = sqlite3.connect("exam.db")
    cursor = connection.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

face_missing_logged = False
absence_start_time = None
absence_duration = 0
total_absence_duration = 0


while True:

    # Capture frame
    success, frame = camera.read()

    if not success:
        print("Failed to capture frame.")
        break
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    # If faces are detected
    if len(faces) > 0:

        # Face detected
        face_missing_logged = False
        if absence_start_time is not None:
            total_absence_duration += int(time.time() - absence_start_time)
        absence_start_time = None
        absence_duration = 0

        cv2.putText(
            frame,
            "Face Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Absence Duration: 0 sec",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Time: {current_time}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

    else:

        cv2.putText(
            frame,
            "Face Not Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        # Start timer only once
        if absence_start_time is None:
            absence_start_time = time.time()

        # Calculate absence duration
        absence_duration = int(time.time() - absence_start_time)

        cv2.putText(
            frame,
            f"Absence Duration: {absence_duration} sec",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Time: {current_time}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        # Log only once for each absence
        if not face_missing_logged:

            log_event(
                candidate_id,
                "Face Not Detected",
                "Candidate face not visible"
            )

            face_missing_logged = True




    # Show webcam feed
    cv2.imshow("Face Detection", frame)

    # Exit when Q is pressed
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break
    # Wait for key press
    key = cv2.waitKey(1) & 0xFF

    # Press 'c' to capture image
    if key == ord('c'):

        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

        filepath = os.path.join(photo_folder, filename)

        cv2.imwrite(filepath, frame)

        print("Image Saved Successfully!")
        print("Location:", filepath)

    # Press 'q' to quit
    if key == ord('q'):

        # If the face is still absent when quitting
        if absence_start_time is not None:
            total_absence_duration += int(time.time() - absence_start_time)

        print("\n===== Monitoring Summary =====")
        print("Total Face Absence Duration:", total_absence_duration, "seconds")

        break
    

camera.release()
cv2.destroyAllWindows()