# logic.py
# Pure functions with no database or FastAPI dependency — this is what makes
# them easy to unit-test (Day 3 deliverable: "unit-tested same day").

def calculate_intervals(session_duration_minutes: int, max_snapshots: int = 6, min_gap_minutes: int = 5):
    """
    Given a session length, decide how many snapshots to take (capped at 6)
    and how many minutes apart they should be.

    Matches the worked examples from the architecture blueprint:
      - 50-minute session -> 6 snapshots, ~8.33 min apart
      - 90-minute session -> 6 snapshots, 15 min apart
      - 20-minute session -> reduced to 4 snapshots, 5 min apart
        (because 6 snapshots would mean scanning less than min_gap_minutes apart)
    """
    snapshot_count = max_snapshots
    interval_minutes = session_duration_minutes / snapshot_count

    while interval_minutes < min_gap_minutes and snapshot_count > 1:
        snapshot_count -= 1
        interval_minutes = session_duration_minutes / snapshot_count

    return snapshot_count, round(interval_minutes, 2)


def determine_attendance_status(scan_matches: int) -> str:
    """
    The rule engine: turn a raw count of successful face-matches during a
    session into an attendance status.

      5-6 matches -> Present
      3-4 matches -> Pending_Review (teacher must confirm)
      0-2 matches -> Absent
    """
    if scan_matches >= 5:
        return "Present"
    elif scan_matches >= 3:
        return "Pending_Review"
    else:
        return "Absent"


# --- Quick manual test you can run directly: python logic.py ---
if __name__ == "__main__":
    print("Interval tests:")
    print(" 50 min ->", calculate_intervals(50))   # expect (6, 8.33)
    print(" 90 min ->", calculate_intervals(90))   # expect (6, 15.0)
    print(" 20 min ->", calculate_intervals(20))   # expect (4, 5.0)

    print("\nRule engine tests:")
    for count in [6, 5, 4, 3, 2, 0]:
        print(f" {count} matches ->", determine_attendance_status(count))
