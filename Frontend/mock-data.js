// Fake backend responses so you can build UI before the real API exists.
// Use these on Day 1. Delete this file (and swap function calls in app.js)
// once Student 1's real endpoints are live on Day 2.

function mockSessionStatus() {
  return Promise.resolve({
    session_id: 1,
    students: [
      { name: "Asha K.", status: "present" },
      { name: "Rohan T.", status: "partial" },
      { name: "Priya S.", status: "absent" }
    ]
  });
}

function mockCreateSession(intervalMinutes) {
  return Promise.resolve({ session_id: 1, interval_minutes: intervalMinutes, status: "started" });
}
