from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from pathlib import Path
from datetime import date

app = Flask(__name__)
app.secret_key = "smart-notes-mini-project-key"
DB_PATH = Path(__file__).with_name("study_platform.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT DEFAULT 'General',
            due_date TEXT,
            priority TEXT DEFAULT 'Medium',
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)
        count = db.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        if count == 0:
            db.execute("INSERT INTO notes(title, subject, content) VALUES(?,?,?)",
                       ("Welcome to Smart Notes", "Getting Started",
                        "Use this platform to save class notes, organise subjects and track your study tasks."))
            db.execute("INSERT INTO tasks(title, subject, due_date, priority) VALUES(?,?,?,?)",
                       ("Explore your study dashboard", "General", date.today().isoformat(), "Low"))

@app.route("/")
def index():
    with get_db() as db:
        notes = db.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
        tasks = db.execute("SELECT * FROM tasks ORDER BY completed ASC, due_date IS NULL, due_date ASC, id DESC").fetchall()
        total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        completed = db.execute("SELECT COUNT(*) FROM tasks WHERE completed=1").fetchone()[0]
        note_count = db.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        subjects = db.execute("""
            SELECT subject FROM notes UNION SELECT subject FROM tasks ORDER BY subject
        """).fetchall()
    progress = round((completed / total) * 100) if total else 0
    return render_template("index.html", notes=notes, tasks=tasks, total=total,
                           completed=completed, pending=total-completed,
                           note_count=note_count, progress=progress,
                           subjects=[s["subject"] for s in subjects])

@app.route("/notes/add", methods=["POST"])
def add_note():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    content = request.form.get("content", "").strip()
    if not all([title, subject, content]):
        flash("Please fill in all note fields.", "error")
    else:
        with get_db() as db:
            db.execute("INSERT INTO notes(title, subject, content) VALUES(?,?,?)",
                       (title, subject, content))
        flash("Note saved successfully!", "success")
    return redirect(url_for("index") + "#notes")

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    with get_db() as db:
        db.execute("DELETE FROM notes WHERE id=?", (note_id,))
    flash("Note deleted.", "success")
    return redirect(url_for("index") + "#notes")

@app.route("/tasks/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip() or "General"
    due_date = request.form.get("due_date") or None
    priority = request.form.get("priority", "Medium")
    if not title:
        flash("Task title cannot be empty.", "error")
    else:
        with get_db() as db:
            db.execute("INSERT INTO tasks(title, subject, due_date, priority) VALUES(?,?,?,?)",
                       (title, subject, due_date, priority))
        flash("Study task added!", "success")
    return redirect(url_for("index") + "#tasks")

@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    with get_db() as db:
        db.execute("UPDATE tasks SET completed = CASE completed WHEN 1 THEN 0 ELSE 1 END WHERE id=?",
                   (task_id,))
    return redirect(url_for("index") + "#tasks")

@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    with get_db() as db:
        db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    flash("Task deleted.", "success")
    return redirect(url_for("index") + "#tasks")

@app.route("/api/stats")
def stats():
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        completed = db.execute("SELECT COUNT(*) FROM tasks WHERE completed=1").fetchone()[0]
        notes = db.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    return jsonify({"total_tasks": total, "completed": completed,
                    "pending": total-completed, "notes": notes})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
