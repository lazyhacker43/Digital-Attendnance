import requests
from real_face_encode import encode_face_from_frame
from real_face_match import match_face
import cv2

frame = cv2.imread("test_capture.jpg")
encoding = encode_face_from_frame(frame)

if not encoding:
    print("No face detected in test_capture.jpg — cannot proceed")
else:
    known_students = {2: encoding}  # student_id=2 is your real test student
    result = match_face(encoding, known_students)
    print("Match result:", result)

    if result["matched"]:
        response = requests.post("http://127.0.0.1:8000/scan-result", json={
            "session_id": 1,
            "student_id": result["student_id"],
            "scan_number": 1
        })
        print("Backend response:", response.status_code, response.json())
    else:
        print("No match — nothing sent to backend")