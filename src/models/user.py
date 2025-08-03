from datetime import datetime
from src.models.database import db
import hashlib
import secrets

class User:
    def __init__(self, email, password, role='editor', username=None):
        self.email = email
        self.password_hash = self._hash_password(password)
        self.role = role
        self.username = username or email.split('@')[0]
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()

    def _hash_password(self, password):
        # Use a simple salt + hash approach for deployment compatibility
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode())
        return salt + hash_obj.hexdigest()

    def check_password(self, password):
        if len(self.password_hash) < 32:
            return False
        salt = self.password_hash[:32]
        stored_hash = self.password_hash[32:]
        hash_obj = hashlib.sha256((password + salt).encode())
        return hash_obj.hexdigest() == stored_hash

    def save(self):
        cursor = db.cursor()
        if hasattr(self, 'id'):
            # Update existing user
            cursor.execute('''
                UPDATE users SET email=?, username=?, password_hash=?, role=?, updated_at=?
                WHERE id=?
            ''', (self.email, self.username, self.password_hash, self.role, 
                  datetime.utcnow().isoformat(), self.id))
        else:
            # Create new user
            cursor.execute('''
                INSERT INTO users (email, username, password_hash, role, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.email, self.username, self.password_hash, self.role, 
                  self.created_at, self.updated_at))
            self.id = cursor.lastrowid
        
        db.commit()
        return self

    @staticmethod
    def find_by_email(email):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        
        if row:
            user = User.__new__(User)
            user.id = row['id']
            user.email = row['email']
            user.username = row['username']
            user.password_hash = row['password_hash']
            user.role = row['role']
            user.created_at = row['created_at']
            user.updated_at = row['updated_at']
            return user
        return None

    @staticmethod
    def find_by_id(user_id):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row:
            user = User.__new__(User)
            user.id = row['id']
            user.email = row['email']
            user.username = row['username']
            user.password_hash = row['password_hash']
            user.role = row['role']
            user.created_at = row['created_at']
            user.updated_at = row['updated_at']
            return user
        return None

    @staticmethod
    def find_all():
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        
        users = []
        for row in rows:
            user = User.__new__(User)
            user.id = row['id']
            user.email = row['email']
            user.username = row['username']
            user.password_hash = row['password_hash']
            user.role = row['role']
            user.created_at = row['created_at']
            user.updated_at = row['updated_at']
            users.append(user)
        return users

    def delete(self):
        if hasattr(self, 'id'):
            cursor = db.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (self.id,))
            db.commit()
            return True
        return False

    def to_dict(self):
        return {
            'id': str(self.id) if hasattr(self, 'id') else None,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'<User {self.username}>'

