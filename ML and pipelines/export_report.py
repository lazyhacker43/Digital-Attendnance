import pandas as pd

def export_session_report(session_data, filename="attendance_report.xlsx"):
    """
    session_data: dict like {"student_101": "present", "student_102": "partial", ...}
    Writes a simple attendance report to an .xlsx file.
    """
    rows = []
    for student_id, status in session_data.items():
        percentage = {"present": 100, "partial": 60, "absent": 0}.get(status, 0)
        rows.append({
            "Student ID": student_id,
            "Status": status,
            "Attendance %": percentage
        })

    df = pd.DataFrame(rows)
    df.to_excel(filename, index=False)
    print(f"Report saved to {filename}")
    return df