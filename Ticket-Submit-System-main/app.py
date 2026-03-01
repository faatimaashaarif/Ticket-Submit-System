from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DB_FILE = "tickets.db"

# ----- Database Setup ----- #
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            email TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            priority TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Open',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            due_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ----- Helper Functions ----- #
def add_ticket(user_name, email, issue_type, priority, description):
    due_date = datetime.now() + timedelta(days=2)  # default SLA 2 days
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tickets (user_name, email, issue_type, priority, description, due_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_name, email, issue_type, priority, description, due_date.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def get_all_tickets():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    tickets = []
    for row in rows:
        tickets.append({
            "id": row[0],
            "user_name": row[1],
            "email": row[2],
            "issue_type": row[3],
            "priority": row[4],
            "description": row[5],
            "status": row[6],
            "created_at": row[7],
            "due_at": row[8]
        })
    return tickets

def update_ticket_status(ticket_id, status):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status = ? WHERE id = ?", (status, ticket_id))
    conn.commit()
    conn.close()

# ----- Routes ----- #
@app.route('/')
def index():
    tickets = get_all_tickets()
    return render_template('index.html', tickets=tickets)

@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    data = request.form
    add_ticket(
        user_name=data.get('user_name'),
        email=data.get('email'),
        issue_type=data.get('issue_type'),
        priority=data.get('priority'),
        description=data.get('description')
    )
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    tickets = get_all_tickets()
    return render_template('admin.html', tickets=tickets)

@app.route('/update_status/<int:ticket_id>/<status>')
def update_status(ticket_id, status):
    update_ticket_status(ticket_id, status)
    return redirect(url_for('admin'))

@app.route('/export_json')
def export_json():
    tickets = get_all_tickets()
    return jsonify(tickets)

# ----- Main ----- #
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
