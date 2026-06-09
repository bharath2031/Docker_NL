import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "data/dashboard.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database with required schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create prompt_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_prompt TEXT NOT NULL,
                generated_action TEXT,
                execution_result TEXT,
                execution_time_ms REAL
            )
        """)
        
        # Create container_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS container_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                container_id TEXT NOT NULL,
                container_name TEXT NOT NULL,
                status TEXT NOT NULL,
                cpu_usage REAL,
                memory_usage REAL
            )
        """)
        
        # Create audit_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_prompt(self, user_prompt: str, generated_action: str, 
                   execution_result: str, execution_time_ms: float):
        """Log prompt to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO prompt_logs 
            (timestamp, user_prompt, generated_action, execution_result, execution_time_ms)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, user_prompt, generated_action, execution_result, execution_time_ms))
        
        conn.commit()
        conn.close()
    
    def log_container_history(self, container_id: str, container_name: str, 
                              status: str, cpu_usage: float = 0.0, 
                              memory_usage: float = 0.0):
        """Log container state to history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO container_history 
            (timestamp, container_id, container_name, status, cpu_usage, memory_usage)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, container_id, container_name, status, cpu_usage, memory_usage))
        
        conn.commit()
        conn.close()
    
    def log_audit(self, action: str, status: str, details: str = ""):
        """Log audit event"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO audit_logs 
            (timestamp, action, status, details)
            VALUES (?, ?, ?, ?)
        """, (timestamp, action, status, details))
        
        conn.commit()
        conn.close()
    
    def get_prompt_logs(self, limit: int = 100) -> List[Dict]:
        """Retrieve recent prompt logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, user_prompt, generated_action, 
                   execution_result, execution_time_ms
            FROM prompt_logs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "timestamp": row[1],
                "user_prompt": row[2],
                "generated_action": row[3],
                "execution_result": row[4],
                "execution_time_ms": row[5]
            }
            for row in rows
        ]
    
    def get_container_history(self, limit: int = 1000) -> List[Dict]:
        """Retrieve container history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, container_id, container_name, 
                   status, cpu_usage, memory_usage
            FROM container_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "timestamp": row[1],
                "container_id": row[2],
                "container_name": row[3],
                "status": row[4],
                "cpu_usage": row[5],
                "memory_usage": row[6]
            }
            for row in rows
        ]
    
    def get_audit_logs(self, limit: int = 100) -> List[Dict]:
        """Retrieve audit logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, action, status, details
            FROM audit_logs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "timestamp": row[1],
                "action": row[2],
                "status": row[3],
                "details": row[4]
            }
            for row in rows
        ]
    
    def get_container_stats_summary(self) -> Dict:
        """Get summary statistics of containers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get latest status for each container
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM (
                SELECT container_id, status
                FROM container_history
                WHERE id IN (
                    SELECT MAX(id)
                    FROM container_history
                    GROUP BY container_id
                )
            )
            GROUP BY status
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        stats = {row[0]: row[1] for row in rows}
        return stats
