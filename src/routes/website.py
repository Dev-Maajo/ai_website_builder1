from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src.models.website import Website
from functools import wraps

website_bp = Blueprint('website', __name__)

def check_permission(permission):
    """Decorator to check user permissions"""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.find_by_id(current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Admin has all permissions
            if user.role == 'admin':
                return f(*args, **kwargs)
            
            # Check specific permissions based on role
            role_permissions = {
                'editor': ['create_website', 'read_website', 'update_website', 'delete_website'],
                'viewer': ['read_website']
            }
            
            if permission not in role_permissions.get(user.role, []):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@website_bp.route('', methods=['POST'])
@check_permission('create_website')
def create_website():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        title = data.get('title')
        content = data.get('content', {})
        business_type = data.get('business_type')
        industry = data.get('industry')
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        # Create new website
        website = Website(
            title=title,
            content=content,
            user_id=current_user_id,
            business_type=business_type,
            industry=industry
        )
        website.save()
        
        return jsonify({
            'message': 'Website created successfully',
            'website': website.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@website_bp.route('/<website_id>', methods=['GET'])
@check_permission('read_website')
def get_website(website_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        website = Website.find_by_id(website_id)
        if not website:
            return jsonify({'error': 'Website not found'}), 404
        
        # Check if user can access this website
        if user.role != 'admin' and str(website.user_id) != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'website': website.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@website_bp.route('', methods=['GET'])
@check_permission('read_website')
def get_websites():
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if user.role == 'admin':
            # Admin can see all websites
            websites = Website.find_all()
        else:
            # Users can only see their own websites
            websites = Website.find_by_user_id(current_user_id)
        
        return jsonify({
            'websites': [website.to_dict() for website in websites]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@website_bp.route('/<website_id>', methods=['PUT'])
@check_permission('update_website')
def update_website(website_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        website = Website.find_by_id(website_id)
        if not website:
            return jsonify({'error': 'Website not found'}), 404
        
        # Check if user can update this website
        if user.role != 'admin' and str(website.user_id) != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Update website fields
        if 'title' in data:
            website.title = data['title']
        if 'content' in data:
            website.content = data['content']
        if 'business_type' in data:
            website.business_type = data['business_type']
        if 'industry' in data:
            website.industry = data['industry']
        
        website.save()
        
        return jsonify({
            'message': 'Website updated successfully',
            'website': website.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@website_bp.route('/<website_id>', methods=['DELETE'])
@check_permission('delete_website')
def delete_website(website_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        website = Website.find_by_id(website_id)
        if not website:
            return jsonify({'error': 'Website not found'}), 404
        
        # Check if user can delete this website
        if user.role != 'admin' and str(website.user_id) != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        website.delete()
        
        return jsonify({'message': 'Website deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

