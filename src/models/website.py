from datetime import datetime
from src.models.database import db
import json

class Website:
    def __init__(self, title, content, user_id, business_type=None, industry=None):
        self.title = title
        self.content = content
        self.user_id = int(user_id) if isinstance(user_id, str) else user_id
        self.business_type = business_type
        self.industry = industry
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()

    def save(self):
        cursor = db.cursor()
        content_json = json.dumps(self.content) if isinstance(self.content, dict) else self.content
        
        if hasattr(self, 'id'):
            # Update existing website
            cursor.execute('''
                UPDATE websites SET title=?, content=?, business_type=?, industry=?, updated_at=?
                WHERE id=?
            ''', (self.title, content_json, self.business_type, self.industry,
                  datetime.utcnow().isoformat(), self.id))
        else:
            # Create new website
            cursor.execute('''
                INSERT INTO websites (title, content, user_id, business_type, industry, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.title, content_json, self.user_id, self.business_type, 
                  self.industry, self.created_at, self.updated_at))
            self.id = cursor.lastrowid
        
        db.commit()
        return self

    @staticmethod
    def find_by_id(website_id):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM websites WHERE id = ?', (website_id,))
        row = cursor.fetchone()
        
        if row:
            website = Website.__new__(Website)
            website.id = row['id']
            website.title = row['title']
            try:
                website.content = json.loads(row['content']) if row['content'] else {}
            except json.JSONDecodeError:
                website.content = row['content']
            website.user_id = row['user_id']
            website.business_type = row['business_type']
            website.industry = row['industry']
            website.created_at = row['created_at']
            website.updated_at = row['updated_at']
            return website
        return None

    @staticmethod
    def find_by_user_id(user_id):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM websites WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        
        websites = []
        for row in rows:
            website = Website.__new__(Website)
            website.id = row['id']
            website.title = row['title']
            try:
                website.content = json.loads(row['content']) if row['content'] else {}
            except json.JSONDecodeError:
                website.content = row['content']
            website.user_id = row['user_id']
            website.business_type = row['business_type']
            website.industry = row['industry']
            website.created_at = row['created_at']
            website.updated_at = row['updated_at']
            websites.append(website)
        return websites

    @staticmethod
    def find_all():
        cursor = db.cursor()
        cursor.execute('SELECT * FROM websites')
        rows = cursor.fetchall()
        
        websites = []
        for row in rows:
            website = Website.__new__(Website)
            website.id = row['id']
            website.title = row['title']
            try:
                website.content = json.loads(row['content']) if row['content'] else {}
            except json.JSONDecodeError:
                website.content = row['content']
            website.user_id = row['user_id']
            website.business_type = row['business_type']
            website.industry = row['industry']
            website.created_at = row['created_at']
            website.updated_at = row['updated_at']
            websites.append(website)
        return websites

    def delete(self):
        if hasattr(self, 'id'):
            cursor = db.cursor()
            cursor.execute('DELETE FROM websites WHERE id = ?', (self.id,))
            db.commit()
            return True
        return False

    def to_dict(self):
        return {
            'id': str(self.id) if hasattr(self, 'id') else None,
            'title': self.title,
            'content': self.content,
            'user_id': str(self.user_id),
            'business_type': self.business_type,
            'industry': self.industry,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'<Website {self.title}>'

