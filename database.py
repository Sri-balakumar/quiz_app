import sqlite3
from datetime import datetime

class QuizDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('quiz.db')
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
        ''')
        
        # Create scores table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        )
        ''')
        
        self.conn.commit()
    
    def create_user(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                         (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def verify_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result and result[0] == password:
            return True
        return False
    
    def save_score(self, username, score, total):
        percentage = (score / total) * 100
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO scores (username, score, total, percentage, date)
        VALUES (?, ?, ?, ?, ?)
        ''', (username, score, total, percentage, datetime.now()))
        self.conn.commit()
    
    def get_top_scores(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT username, score, total, percentage, date
        FROM scores
        ORDER BY percentage DESC, date DESC
        LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
    
    def get_player_history(self, username, limit=5):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT score, total, percentage, date
        FROM scores
        WHERE username = ?
        ORDER BY date DESC
        LIMIT ?
        ''', (username, limit))
        return cursor.fetchall()
    
    def clear_leaderboard(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM scores')
        self.conn.commit()
    
    def close(self):
        self.conn.close()