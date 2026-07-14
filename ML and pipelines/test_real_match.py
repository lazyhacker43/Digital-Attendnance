import cv2
from real_face_encode import encode_face_from_frame
from real_face_match import match_face

# Get a real encoding from your captured photo
frame = cv2.imread("test_capture.jpg")
unknown_encoding = encode_face_from_frame(frame)

if not unknown_encoding:
    print("No face detected in test_capture.jpg — can't test matching")
else:
    # Simulate a "known students" database using your own real encoding
    # (so we can prove a correct match happens)
    known_students = {
        "student_101": unknown_encoding,          # same face -> should MATCH
        "student_102": [0.05] * 128,               # random/fake -> should NOT match
    }

    result = match_face(unknown_encoding, known_students)
    print("Match result:", result)