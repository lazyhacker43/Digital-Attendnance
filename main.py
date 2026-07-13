# main.py
# This is the entry point of your backend. Run it with:  uvicorn main:app --reload
#
# Comments below are tagged [DAY 1], [DAY 2] etc. to match your sprint plan —
# you don't have to build all of this at once. Start with [DAY 1] only.

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
import random
import json

from database import init_db, get_db, User, BiometricEmbedding, ClassSession, RawTimestamp, SessionAttendanceStatus
from auth import hash_password, verify_password, create_access_token, decode_access_token
from logic import calculate_intervals, determine_attendance_status

app = FastAPI(title="Snapshot Attendance Tracker API")

# Runs once when the server starts — creates attendance.db and its tables if
# they don't exist yet.
init_db()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ---------- [DAY 1] Health check + stub vector endpoint ----------
# These two endpoints are enough to (a) prove the server works and (b) let
# your frontend teammate start building the registration flow WITHOUT
# waiting for the real face-recognition code from Student 3.

@app.get("/health")
def health_check():
    return {"status": "ok"}


class StubVectorResponse(BaseModel):
    vector: list[float]

@app.post("/stub-vector", response_model=StubVectorResponse)
def get_stub_vector():
    """
    Fake 128-number face 'fingerprint'. Student 3 will replace the *caller*
    of this logic with real face_recognition output later — your other
    endpoints (registration, approval) don't need to change at all.
    """
    fake_vector = [round(random.uniform(-1, 1), 4) for _ in range(128)]
    return {"vector": fake_vector}


# ---------- [DAY 2] Auth ----------

class SignupRequest(BaseModel):
    full_name: str
    email: str
    password: str
    role: str  # "Admin", "Teacher", or "Student"

@app.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user_id": new_user.user_id, "role": new_user.role}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm expects "username" — we treat email as username.
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(user_id=user.user_id, role=user.role)
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Any endpoint that needs to know "who is calling this?" depends on this
    function. FastAPI reads the Authorization header automatically.
    """
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_role(*allowed_roles: str):
    """Small helper so endpoints can say: only Admins allowed, etc."""
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not authorized for this action")
        return user
    return checker


# ---------- [DAY 2] Registration + Approval ----------

class RegisterFaceRequest(BaseModel):
    student_id: int
    vector: list[float]

@app.post("/register-face")
def register_face(payload: RegisterFaceRequest, db: Session = Depends(get_db)):
    embedding = BiometricEmbedding(
        student_id=payload.student_id,
        vector_data=json.dumps(payload.vector),
        verification_state="Pending",
    )
    db.add(embedding)
    db.commit()
    db.refresh(embedding)
    return {"embedding_id": embedding.embedding_id, "state": embedding.verification_state}


@app.get("/pending-registrations")
def list_pending(db: Session = Depends(get_db), admin: User = Depends(require_role("Admin"))):
    pending = db.query(BiometricEmbedding).filter(BiometricEmbedding.verification_state == "Pending").all()
    return pending


@app.post("/approve-registration/{embedding_id}")
def approve_registration(embedding_id: int, db: Session = Depends(get_db), admin: User = Depends(require_role("Admin"))):
    embedding = db.query(BiometricEmbedding).filter(BiometricEmbedding.embedding_id == embedding_id).first()
    if not embedding:
        raise HTTPException(status_code=404, detail="Not found")
    embedding.verification_state = "Approved"
    db.commit()
    return {"embedding_id": embedding_id, "state": "Approved"}


# ---------- [DAY 3] Session creation + interval logic ----------

class CreateSessionRequest(BaseModel):
    session_duration_minutes: int

@app.post("/sessions")
def create_session(payload: CreateSessionRequest, db: Session = Depends(get_db), teacher: User = Depends(require_role("Teacher"))):
    snapshot_count, interval_minutes = calculate_intervals(payload.session_duration_minutes)

    new_session = ClassSession(
        teacher_id=teacher.user_id,
        session_duration_minutes=payload.session_duration_minutes,
        snapshot_count=snapshot_count,
        interval_minutes=int(interval_minutes),  # keep the DB column simple; use logic.py's precise value in the UI
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {
        "session_id": new_session.session_id,
        "snapshot_count": snapshot_count,
        "interval_minutes": interval_minutes,
    }


# ---------- [DAY 4] Live matching endpoint (stub for now) ----------

class ScanResultRequest(BaseModel):
    session_id: int
    student_id: int
    scan_number: int

@app.post("/scan-result")
def record_scan_result(payload: ScanResultRequest, db: Session = Depends(get_db)):
    """
    Student 3's matching code decides WHICH student_id matched a frame.
    This endpoint just records that match — it doesn't do any face logic
    itself, which keeps backend and ML code cleanly separated.
    """
    timestamp = RawTimestamp(
        session_id=payload.session_id,
        student_id=payload.student_id,
        scan_number=payload.scan_number,
    )
    db.add(timestamp)
    db.commit()
    return {"recorded": True}


# ---------- [DAY 5] Rule engine ----------

@app.post("/sessions/{session_id}/finalize-attendance")
def finalize_attendance(session_id: int, db: Session = Depends(get_db), teacher: User = Depends(require_role("Teacher"))):
    """
    Counts how many times each student was matched during this session,
    then applies the rule engine thresholds to decide Present/Pending/Absent.
    """
    timestamps = db.query(RawTimestamp).filter(RawTimestamp.session_id == session_id).all()

    counts_by_student = {}
    for t in timestamps:
        counts_by_student[t.student_id] = counts_by_student.get(t.student_id, 0) + 1

    results = []
    for student_id, count in counts_by_student.items():
        status_value = determine_attendance_status(count)
        record = SessionAttendanceStatus(
            session_id=session_id,
            student_id=student_id,
            timestamp_count=count,
            status=status_value,
        )
        db.add(record)
        results.append({"student_id": student_id, "matches": count, "status": status_value})

    db.commit()
    return {"session_id": session_id, "results": results}


# ---------- [DAY 6] Minimal export endpoint ----------


@app.get("/sessions/{session_id}/export")
def export_session_attendance(session_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    records = db.query(SessionAttendanceStatus).filter(SessionAttendanceStatus.session_id == session_id).all()
    if user.role == "Student":
        records = [r for r in records if r.student_id == user.user_id]
    return [{"student_id": r.student_id, "status": r.status, "matches": r.timestamp_count} for r in records]