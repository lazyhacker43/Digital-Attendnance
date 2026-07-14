import face_recognition
import numpy as np

def encode_face_from_frame(frame):
    """
    Takes a webcam frame (as a numpy array/image) and returns
    a real 128-d face encoding, replacing mock_encode_face().
    """
    rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])

    face_locations = face_recognition.face_locations(rgb_frame)
    if not face_locations:
        return None

    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    if not face_encodings:
        return None

    return face_encodings[0].tolist()