import face_recognition
import numpy as np

def match_face(unknown_encoding, known_encodings_dict, threshold=0.6):
    """
    Compares one face encoding against a dict of {student_id: encoding}.
    Uses face_recognition's built-in Euclidean distance comparison.
    threshold=0.6 is the library's default — don't tune it this week,
    just flag it as a known limitation per your sprint plan.
    """
    if not known_encodings_dict:
        return {"matched": False, "student_id": None, "confidence": 0.0}

    student_ids = list(known_encodings_dict.keys())
    known_encodings = [np.array(enc) for enc in known_encodings_dict.values()]
    unknown_encoding = np.array(unknown_encoding)

    distances = face_recognition.face_distance(known_encodings, unknown_encoding)
    best_match_index = distances.argmin()
    best_distance = distances[best_match_index]

    if best_distance <= threshold:
        confidence = round(1 - best_distance, 3)
        return {
            "matched": True,
            "student_id": student_ids[best_match_index],
            "confidence": confidence
        }
    else:
        return {"matched": False, "student_id": None, "confidence": 0.0}