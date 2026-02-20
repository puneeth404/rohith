import sqlite3
from contextlib import contextmanager
import os
import json
from datetime import datetime

DB_PATH = "reports_history.db"

# FIX: Database connection leak fix using context manager
@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                report_content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                pdf_path TEXT,
                approved_by TEXT,
                approved_date TIMESTAMP,
                report_version INTEGER DEFAULT 1
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compliance_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER,
                action TEXT,
                performed_by TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(report_id) REFERENCES reports(id)
            )
        ''')
        # Indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_client_id ON reports(client_id)')
        conn.commit()

def save_report(client_id: str, report_content: str, pdf_path: str = None) -> int:
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO reports (client_id, report_content, pdf_path) VALUES (?, ?, ?)''',
            (client_id, report_content, pdf_path)
        )
        conn.commit()
        return cursor.lastrowid

def approve_report(report_id: int, approved_by: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        now = datetime.utcnow().isoformat()
        cursor.execute(
            '''UPDATE reports SET approved_by = ?, approved_date = ? WHERE id = ?''',
            (approved_by, now, report_id)
        )
        cursor.execute(
            '''INSERT INTO compliance_log (report_id, action, performed_by) VALUES (?, ?, ?)''',
            (report_id, "APPROVED", approved_by)
        )
        conn.commit()

def get_client_history(client_id: str):
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports WHERE client_id = ? ORDER BY created_at DESC", (client_id,))
        return [dict(row) for row in cursor.fetchall()]
