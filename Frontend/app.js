// Page-specific interactivity for index.html.
// DAY 1: wired to mock data (mock-data.js).
// DAY 2: once Student 1's real API is live, swap mockSessionStatus() -> fetchSessionStatus()
//        and mockCreateSession() -> createSession() below.

let currentSessionId = null;

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("startSessionBtn").addEventListener("click", handleStartSession);
  document.getElementById("exportBtn").addEventListener("click", handleExport);
});

async function handleStartSession() {
  hideError();
  const interval = document.getElementById("intervalPicker").value;

  // --- Day 1: mock. Day 2: replace with -> const result = await createSession(interval);
  const result = await mockCreateSession(interval);

  if (!result) return;

  currentSessionId = result.session_id;
  await refreshAttendanceStatus();
}

async function refreshAttendanceStatus() {
  if (!currentSessionId) return;

  // --- Day 1: mock. Day 2: replace with -> const data = await fetchSessionStatus(currentSessionId);
  const data = await mockSessionStatus();

  if (!data) return;

  renderStudentList(data.students);
  renderOverallAlert(data.students);
}

function renderStudentList(students) {
  const list = document.getElementById("studentList");
  list.innerHTML = "";

  students.forEach(student => {
    const li = document.createElement("li");
    li.textContent = student.name;

    const badge = document.createElement("span");
    badge.textContent = student.status;
    li.appendChild(badge);

    list.appendChild(li);
  });
}

// Maps backend rule-engine status to the visual alert box color.
// Thresholds per the rule engine: present (5-6), partial (3-4), absent (0-2).
function renderOverallAlert(students) {
  const box = document.getElementById("alertBox");
  box.className = "alert-box";

  const hasAbsent = students.some(s => s.status === "absent");
  const hasPartial = students.some(s => s.status === "partial");

  if (hasAbsent) {
    box.classList.add("alert-red");
    box.textContent = "Attention: one or more students marked absent.";
  } else if (hasPartial) {
    box.classList.add("alert-yellow");
    box.textContent = "Some students have partial attendance.";
  } else {
    box.classList.add("alert-green");
    box.textContent = "All students present.";
  }
}

async function handleExport() {
  hideError();

  if (!currentSessionId) {
    showError("Start a session before exporting.");
    return;
  }

  // Day 6+: real export call once Student 3's export endpoint exists
  await exportAttendance(currentSessionId);
}
