from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src.models.role import Role
from src.models.database import db
from functools import wraps

role_bp = Blueprint('role', __name__)

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@role_bp.route('', methods=['POST'])
@admin_required
def create_role():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        permissions = data.get('permissions', [])
        
        if not name:
            return jsonify({'error': 'Role name is required'}), 400
        
        # Check if role already exists
        existing_role = Role.find_by_name(name)
        if existing_role:
            return jsonify({'error': 'Role with this name already exists'}), 409
        
        # Create new role
        role = Role(name=name, permissions=permissions)
        role.save()
        
        return jsonify({
            'message': 'Role created successfully',
            'role': role.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@role_bp.route('', methods=['GET'])
@admin_required
def get_roles():
    try:
        roles = Role.find_all()
        return jsonify({
            'roles': [role.to_dict() for role in roles]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@role_bp.route('/<role_id>', methods=['PUT'])
@admin_required
def update_role(role_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        role = Role.find_by_id(role_id)
        if not role:
            return jsonify({'error': 'Role not found'}), 404
        
        # Update role fields
        if 'name' in data:
            # Check if new name already exists
            existing_role = Role.find_by_name(data['name'])
            if existing_role and str(existing_role.id) != role_id:
                return jsonify({'error': 'Role with this name already exists'}), 409
            role.name = data['name']
        
        if 'permissions' in data:
            role.permissions = data['permissions']
        
        role.save()
        
        return jsonify({
            'message': 'Role updated successfully',
            'role': role.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@role_bp.route('/<role_id>', methods=['DELETE'])
@admin_required
def delete_role(role_id):
    try:
        role = Role.find_by_id(role_id)
        if not role:
            return jsonify({'error': 'Role not found'}), 404
        
        # Don't allow deletion of default roles
        if role.name in ['admin', 'editor', 'viewer']:
            return jsonify({'error': 'Cannot delete default roles'}), 400
        
        role.delete()
        
        return jsonify({'message': 'Role deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@role_bp.route('/assign', methods=['POST'])
@admin_required
def assign_role():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = data.get('user_id')
        role_name = data.get('role')
        
        if not user_id or not role_name:
            return jsonify({'error': 'User ID and role are required'}), 400
        
        # Find user
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Validate role
        valid_roles = ['admin', 'editor', 'viewer']
        if role_name not in valid_roles:
            return jsonify({'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'}), 400
        
        # Update user role
        user.role = role_name
        user.save()
        
        return jsonify({
            'message': 'Role assigned successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

