"""
Mock face-matching module.
Returns data in the SAME SHAPE the real pipeline will eventually return,
so Student 1 (backend) and Student 2 (frontend) can build against this
immediately instead of waiting for real ML.

Swap calls to this module for the real one once Day 2's real encoding is live.
"""

import random


def mock_encode_face(image_bytes=None):
    """Pretend to turn a camera frame into a 128-d face embedding."""
    return [round(random.uniform(-1, 1), 4) for _ in range(128)]


def mock_match_face(embedding, known_embeddings, threshold=0.6):
    """
    Pretend to compare an embedding against known students.
    Returns a fake match result in the real pipeline's expected shape.
    """
    if not known_embeddings:
        return {"matched": False, "student_id": None, "confidence": 0.0}

    matched_student = random.choice(list(known_embeddings.keys()))
    fake_confidence = round(random.uniform(threshold, 1.0), 3)

    return {
        "matched": True,
        "student_id": matched_student,
        "confidence": fake_confidence
    }


if __name__ == "__main__":
    known = {"student_101": [0.1] * 128, "student_102": [0.2] * 128}
    fake_embedding = mock_encode_face()
    result = mock_match_face(fake_embedding, known)
    print("Encoded embedding (first 5 values):", fake_embedding[:5])
    print("Match result:", result)
