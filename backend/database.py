import sqlite3
import os
from datetime import datetime

def init_db(db_path="data/code_quality.db"):
    """Initialize SQLite database with all tables"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Main quality metrics table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS code_quality (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            submission_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            overall_score INTEGER DEFAULT 0,
            bugs_count INTEGER DEFAULT 0,
            security_issues INTEGER DEFAULT 0,
            style_issues INTEGER DEFAULT 0,
            complexity_score REAL DEFAULT 0.0,
            duplication_percent REAL DEFAULT 0.0,
            total_issues INTEGER DEFAULT 0,
            sarif_path TEXT
        )
    ''')
    
    # Detailed issues table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quality_id INTEGER,
            line_number INTEGER,
            file_path TEXT,
            rule_id TEXT,
            severity TEXT,
            message TEXT,
            fix_suggestion TEXT,
            FOREIGN KEY(quality_id) REFERENCES code_quality(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {db_path}")

def store_quality_results(student_id, score, issues, sarif_path=None, db_path="data/code_quality.db"):
    """Store CodeQL results"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    bugs = len([i for i in issues if i.get('severity') == 'error'])
    security = len([i for i in issues if 'security' in i.get('rule_id', '').lower()])
    style = len([i for i in issues if i.get('severity') == 'warning'])
    
    cur.execute('''
        INSERT INTO code_quality (student_id, overall_score, bugs_count, security_issues, style_issues, 
                                 complexity_score, duplication_percent, total_issues, sarif_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_id, score, bugs, security, style, 3.8, 2.0, len(issues), sarif_path))
    
    quality_id = cur.lastrowid
    
    for issue in issues:
        cur.execute('''
            INSERT INTO issues (quality_id, line_number, file_path, rule_id, severity, message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (quality_id, issue.get('line', 0), issue.get('file', 'unknown'), 
              issue.get('rule_id'), issue.get('severity'), issue.get('message')))
    
    conn.commit()
    conn.close()
    return quality_id

def calculate_score(issues):
    """Calculate quality score 0-100"""
    total = len(issues)
    critical = len([i for i in issues if i.get('severity') == 'error'])
    score = max(0, 100 - (critical * 15) - (total * 3))
    return min(100, int(score))

def get_student_latest(student_id, db_path="data/code_quality.db"):
    """Get latest analysis"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
        SELECT overall_score, bugs_count, security_issues, style_issues, total_issues
        FROM code_quality WHERE student_id = ? ORDER BY id DESC LIMIT 1
    ''', (student_id,))
    result = cur.fetchone()
    conn.close()
    return result if result else (0, 0, 0, 0, 0)
