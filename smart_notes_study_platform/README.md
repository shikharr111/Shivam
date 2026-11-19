# StudySpace — Smart Notes & Study Management Platform

A beginner-friendly second-year web development mini project built with **Python Flask, SQLite, HTML, CSS and JavaScript**.

## Features
- Add and delete subject-wise notes
- Add, complete/undo and delete study tasks
- Set task subject, due date and priority
- Dashboard cards for saved notes, total tasks, pending tasks and completion percentage
- Responsive layout for laptop, tablet and mobile
- SQLite database stores information locally, even after closing the browser

## Requirements
- Python 3.9 or newer
- VS Code (recommended)
- Internet connection only for loading Google Fonts; the app itself runs locally

## Run the project in VS Code

1. Extract the ZIP file.
2. Open the extracted `smart_notes_study_platform` folder in VS Code.
3. Open Terminal → New Terminal.
4. (Recommended) Create a virtual environment:

   **Windows**
   ```bash
   python -m venv venv
   venv\\Scripts\\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. Install Flask:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the application:
   ```bash
   python app.py
   ```
7. Open the local address shown in the terminal, usually `http://127.0.0.1:5000`.

The SQLite database file `study_platform.db` is created automatically on the first run.

## Project structure

```text
smart_notes_study_platform/
│
├── app.py                  # Flask routes and SQLite database logic
├── requirements.txt        # Python dependencies
├── README.md               # Setup and project guide
├── study_platform.db       # Created automatically when app runs
│
├── templates/
│   └── index.html          # Main dashboard page
│
└── static/
    ├── style.css           # Styling and responsive design
    └── script.js           # Small browser-side interactions
```

## Technologies used
- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **Editor:** Visual Studio Code

## Mini-project explanation
StudySpace helps students store class notes and organise their academic work in one place. The frontend sends form data to Flask routes. Flask validates the input and stores or updates records in the SQLite database. The dashboard reads the saved records and calculates task progress.

## Possible future improvements
- User login and separate accounts
- Edit existing notes
- Search and filter notes by subject
- Calendar view and reminder notifications
- Export notes as PDF
