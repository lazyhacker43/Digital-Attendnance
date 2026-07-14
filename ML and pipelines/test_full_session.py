from real_face_match import match_face
from rule_engine import classify_attendance

# Simulated known students (same style as Day 4's test)
known_students = {
    "student_101": [0.1] * 128,
    "student_102": [0.5] * 128,
    "student_103": [-0.3] * 128,
}

# Simulate a mock session: each student was "seen" a different number of
# times across 6 scan intervals (mimicking real webcam scans over a class)
mock_session_data = {
    "student_101": 6,  # seen every interval -> should be "present"
    "student_102": 4,  # seen half the time -> should be "partial"
    "student_103": 1,  # barely seen -> should be "absent"
}

print("=== Full Mock Session Results ===\n")
for student_id, intervals_present in mock_session_data.items():
    status = classify_attendance(intervals_present)
    print(f"{student_id}: seen in {intervals_present}/6 intervals -> {status}")

print("\n=== Face Matching Spot-Check ===\n")
# Confirm matching still correctly identifies each student's own encoding
for student_id, encoding in known_students.items():
    result = match_face(encoding, known_students)
    match_ok = "OK" if result["student_id"] == student_id else "MISMATCH — LOG THIS"
    print(f"{student_id} self-match: {result} [{match_ok}]")