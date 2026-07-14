from export_report import export_session_report

mock_session = {
    "student_101": "present",
    "student_102": "partial",
    "student_103": "absent",
}

df = export_session_report(mock_session)
print("\n--- Generated report contents ---")
print(df)