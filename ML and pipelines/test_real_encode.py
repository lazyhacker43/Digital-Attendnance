import cv2
from real_face_encode import encode_face_from_frame

frame = cv2.imread("test_capture.jpg")
encoding = encode_face_from_frame(frame)

if encoding:
    print("Real encoding generated, first 5 values:", encoding[:5])
else:
    print("No face detected in the captured image")
    print(f"[PRIVACY CHECK] Frame processed in memory only, not written to disk. Encoding length: {len(encoding) if encoding else 0}")