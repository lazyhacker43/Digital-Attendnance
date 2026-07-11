"""
Reference implementation of the attendance rule engine.
Thresholds (out of a max of 6 scan intervals per session):
  5-6 intervals matched -> "present"
  3-4 intervals matched -> "partial"
  0-2 intervals matched -> "absent"

This is Student 3's standalone copy for early QA testing before
Student 1's real backend rule engine endpoint is live (Day 5).
Once the real endpoint exists, add integration tests that call it
directly instead of relying solely on this local copy.
"""


def classify_attendance(intervals_present: int, total_intervals: int = 6) -> str:
    if intervals_present < 0 or intervals_present > total_intervals:
        raise ValueError(f"intervals_present must be between 0 and {total_intervals}")

    if intervals_present >= 5:
        return "present"
    elif intervals_present >= 3:
        return "partial"
    else:
        return "absent"
