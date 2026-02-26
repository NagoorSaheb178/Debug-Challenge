import sqlite3
import json
from datetime import datetime
import os

DB_PATH = "analysis_results.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id TEXT PRIMARY KEY,
            query TEXT,
            filename TEXT,
            status TEXT,
            result TEXT,
            created_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_result(task_id, query, filename, status, result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO analysis_results (id, query, filename, status, result, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (task_id, query, filename, status, result, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_result(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM analysis_results WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "query": row[1],
            "filename": row[2],
            "status": row[3],
            "result": row[4],
            "created_at": row[5]
        }
    return None

def update_status(task_id, status, result=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if result:
        cursor.execute('UPDATE analysis_results SET status = ?, result = ? WHERE id = ?', (status, result, task_id))
    else:
        cursor.execute('UPDATE analysis_results SET status = ? WHERE id = ?', (status, task_id))
    conn.commit()
    conn.close()

# Initialize the database on import
init_db()
