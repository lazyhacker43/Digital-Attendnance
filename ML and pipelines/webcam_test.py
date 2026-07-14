import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Could not open webcam")
else:
    print("Webcam opened successfully")
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("test_capture.jpg", frame)
        print("Captured a test frame — check test_capture.jpg")
cap.release()