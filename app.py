from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

# database
with get_db_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            conn.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "Pending"))
            conn.commit()
        conn.close()
        return redirect(url_for("index"))

    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/complete/<int:task_id>")
def complete(task_id):
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", ("Completed", task_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
