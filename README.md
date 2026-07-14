# Snapshot Attendance Tracker

## Project Overview
Snapshot Attendance Tracker is a modern frontend prototype for an AI-assisted attendance monitoring experience. The interface is designed for administrators, teachers, and students with a polished dashboard experience built in plain HTML, CSS, and JavaScript.

## Features
- Responsive authentication flow
- Role-based navigation for admin, teacher, and student views
- Modular JavaScript with reusable API functions
- Mock API layer using the Fetch API and local storage
- Clean dashboard styling with cards, tables, and responsive layout

## Folder Structure
```text
Snapshot-Attendance-Tracker/
├── index.html
├── admin.html
├── teacher.html
├── student.html
├── css/
│   └── style.css
├── js/
│   ├── api.js
│   └── app.js
├── images/
│   └── logo.svg
└── README.md
```

## Installation
1. Clone or download this project folder.
2. Open the root folder in your preferred editor.
3. Start a simple static server from the project root.

## Run Project
Use any lightweight local server, for example:

```bash
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Deployment
The project is static and can be deployed to any hosting service such as GitHub Pages, Netlify, or Vercel.

## Future Improvements
- Add real authentication and backend integration
- Build live charts for attendance analytics
- Add dark mode and improved accessibility enhancements
- Introduce real-time session capture updates
