import numpy as np
from real_face_match import match_face

# Simulate a small "known students" database with distinct fake encodings
known_students = {
    "student_101": [0.1] * 128,
    "student_102": [0.5] * 128,
    "student_103": [-0.3] * 128,
}

# Test 1: exact match — should MATCH student_101 with confidence 1.0
print("Test 1 (exact match):")
result1 = match_face([0.1] * 128, known_students)
print(result1)

# Test 2: close to student_102 but not exact — should likely still MATCH
print("\nTest 2 (close match):")
result2 = match_face([0.49] * 128, known_students)
print(result2)

# Test 3: completely different encoding — should NOT match anyone (unknown face)
print("\nTest 3 (unknown/unregistered face):")
result3 = match_face([5.0] * 128, known_students)
print(result3)

# Test 4: empty known_students — edge case, no one registered yet
print("\nTest 4 (no known students registered):")
result4 = match_face([0.1] * 128, {})
print(result4)