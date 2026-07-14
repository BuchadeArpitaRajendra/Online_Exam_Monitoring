import cv2

# Open the default webcam
camera = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not camera.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

print("Press 'Q' to close the webcam.")

while True:

    # Read a frame from the webcam
    success, frame = camera.read()

    # If frame is not captured
    if not success:
        print("Failed to capture frame.")
        break

    # Display the frame
    cv2.imshow("Online Exam Monitoring - Webcam", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam
camera.release()

# Close all OpenCV windows
cv2.destroyAllWindows()

print("Webcam closed successfully.")