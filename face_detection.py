import cv2
import os
from datetime import datetime

# Load the Haar Cascade classifier
face_cascade = cv2.CascadeClassifier(
    
"haarcascade\haarcascade_frontalface_default.xml"
)

photo_folder = "photos1"

if not os.path.exists(photo_folder):
    os.makedirs(photo_folder)

# Open the webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Unable to access webcam.")
    exit()

print("Press 'Q' to exit.")

while True:

    # Capture frame
    success, frame = camera.read()

    if not success:
        print("Failed to capture frame.")
        break

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

        # Display status
        cv2.putText(
            frame,
            "Face Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Draw rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

    else:

        # Display status when no face is found
        cv2.putText(
            frame,
            "Face Not Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

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
    elif key == ord('q'):
        break
    

camera.release()
cv2.destroyAllWindows()