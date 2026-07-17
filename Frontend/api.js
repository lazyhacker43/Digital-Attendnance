// All calls to Student 1's FastAPI backend live here.
// Swap API_BASE for the deployed Render/Railway URL on Day 6-7.
const API_BASE = "https://snap-in.onrender.com/";

async function fetchSessionStatus(sessionId) {
  try {
    const response = await fetch(`${API_BASE}/sessions/${sessionId}/status`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token") || ""}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error(`Server responded with ${response.status}`);
    }

    return await response.json();

  } catch (error) {
    showError("Could not load session data. Please try again.");
    console.error(error);
    return null;
  }
}

async function createSession(intervalMinutes) {
  try {
    const response = await fetch(`${API_BASE}/sessions`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token") || ""}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ interval_minutes: intervalMinutes })
    });
    return await response.json();
  } catch (error) {
    showError("Could not start session. Check your connection and try again.");
    console.error(error);
    return null;
  }
}

async function exportAttendance(sessionId) {
  try {
    const response = await fetch(`${API_BASE}/sessions/${sessionId}/export`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token") || ""}`
      }
    });

    if (!response.ok) {
      throw new Error(`Server responded with ${response.status}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `attendance_session_${sessionId}.xlsx`;
    a.click();
    window.URL.revokeObjectURL(url);

  } catch (error) {
    showError("Export failed. Please try again.");
    console.error(error);
  }
}

function showError(message) {
  const errorBox = document.getElementById("errorBox");
  if (!errorBox) return;
  errorBox.textContent = message;
  errorBox.style.display = "block";
}

function hideError() {
  const errorBox = document.getElementById("errorBox");
  if (!errorBox) return;
  errorBox.style.display = "none";
}
