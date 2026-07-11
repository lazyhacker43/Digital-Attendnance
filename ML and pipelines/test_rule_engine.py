import pytest
from rule_engine import classify_attendance
from mock_face_match import mock_match_face


def test_full_attendance_is_present():
    assert classify_attendance(6) == "present"


def test_five_intervals_is_present():
    assert classify_attendance(5) == "present"


def test_four_intervals_is_partial():
    assert classify_attendance(4) == "partial"


def test_three_intervals_is_partial():
    assert classify_attendance(3) == "partial"


def test_two_intervals_is_absent():
    assert classify_attendance(2) == "absent"


def test_zero_intervals_is_absent():
    assert classify_attendance(0) == "absent"


def test_negative_intervals_raises_error():
    with pytest.raises(ValueError):
        classify_attendance(-1)


def test_over_max_intervals_raises_error():
    with pytest.raises(ValueError):
        classify_attendance(7)


def test_mock_match_returns_expected_shape():
    known = {"student_101": [0.1] * 128}
    result = mock_match_face([0.0] * 128, known)
    assert "matched" in result
    assert "student_id" in result
    assert "confidence" in result


def test_mock_match_with_no_known_students():
    result = mock_match_face([0.0] * 128, {})
    assert result["matched"] is False
    assert result["student_id"] is None
