from datetime import datetime
from src.models.database import db
import json

class Role:
    def __init__(self, name, permissions=None):
        self.name = name
        self.permissions = permissions or []
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()

    def save(self):
        cursor = db.cursor()
        permissions_json = json.dumps(self.permissions)
        
        if hasattr(self, 'id'):
            # Update existing role
            cursor.execute('''
                UPDATE roles SET name=?, permissions=?, updated_at=?
                WHERE id=?
            ''', (self.name, permissions_json, datetime.utcnow().isoformat(), self.id))
        else:
            # Create new role
            cursor.execute('''
                INSERT INTO roles (name, permissions, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (self.name, permissions_json, self.created_at, self.updated_at))
            self.id = cursor.lastrowid
        
        db.commit()
        return self

    @staticmethod
    def find_by_id(role_id):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM roles WHERE id = ?', (role_id,))
        row = cursor.fetchone()
        
        if row:
            role = Role.__new__(Role)
            role.id = row['id']
            role.name = row['name']
            try:
                role.permissions = json.loads(row['permissions']) if row['permissions'] else []
            except json.JSONDecodeError:
                role.permissions = []
            role.created_at = row['created_at']
            role.updated_at = row['updated_at']
            return role
        return None

    @staticmethod
    def find_by_name(name):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM roles WHERE name = ?', (name,))
        row = cursor.fetchone()
        
        if row:
            role = Role.__new__(Role)
            role.id = row['id']
            role.name = row['name']
            try:
                role.permissions = json.loads(row['permissions']) if row['permissions'] else []
            except json.JSONDecodeError:
                role.permissions = []
            role.created_at = row['created_at']
            role.updated_at = row['updated_at']
            return role
        return None

    @staticmethod
    def find_all():
        cursor = db.cursor()
        cursor.execute('SELECT * FROM roles')
        rows = cursor.fetchall()
        
        roles = []
        for row in rows:
            role = Role.__new__(Role)
            role.id = row['id']
            role.name = row['name']
            try:
                role.permissions = json.loads(row['permissions']) if row['permissions'] else []
            except json.JSONDecodeError:
                role.permissions = []
            role.created_at = row['created_at']
            role.updated_at = row['updated_at']
            roles.append(role)
        return roles

    def delete(self):
        if hasattr(self, 'id'):
            cursor = db.cursor()
            cursor.execute('DELETE FROM roles WHERE id = ?', (self.id,))
            db.commit()
            return True
        return False

    def to_dict(self):
        return {
            'id': str(self.id) if hasattr(self, 'id') else None,
            'name': self.name,
            'permissions': self.permissions,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @staticmethod
    def initialize_default_roles():
        """Initialize default roles if they don't exist"""
        admin_role = Role.find_by_name('admin')
        if not admin_role:
            admin_role = Role('admin', [
                'create_website', 'read_website', 'update_website', 'delete_website',
                'create_user', 'read_user', 'update_user', 'delete_user',
                'create_role', 'read_role', 'update_role', 'delete_role',
                'assign_role'
            ])
            admin_role.save()

        editor_role = Role.find_by_name('editor')
        if not editor_role:
            editor_role = Role('editor', [
                'create_website', 'read_website', 'update_website', 'delete_website'
            ])
            editor_role.save()

        viewer_role = Role.find_by_name('viewer')
        if not viewer_role:
            viewer_role = Role('viewer', ['read_website'])
            viewer_role.save()

    def __repr__(self):
        return f'<Role {self.name}>'

