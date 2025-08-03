from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src.models.website import Website
import json
import os

ai_bp = Blueprint('ai', __name__)

def check_permission(permission):
    """Decorator to check user permissions"""
    from functools import wraps
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

@ai_bp.route('/generate', methods=['POST'])
@check_permission('create_website')
def generate_website():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        business_type = data.get('business_type')
        industry = data.get('industry')
        company_name = data.get('company_name', 'Your Company')
        additional_info = data.get('additional_info', '')
        
        if not business_type or not industry:
            return jsonify({'error': 'Business type and industry are required'}), 400
        
        # Generate content using template-based approach (fallback for deployment)
        content = {
            "title": f"{company_name} - Professional {business_type}",
            "hero": f"Welcome to {company_name}, your trusted partner in {industry}. We provide exceptional {business_type.lower()} services tailored to your needs.",
            "about": f"At {company_name}, we are a leading {business_type.lower()} specializing in {industry.lower()} solutions. Our experienced team is dedicated to delivering innovative services that drive success for our clients.",
            "services": f"We offer comprehensive {industry.lower()} services including consultation, strategy development, implementation, and ongoing support. Our expertise in {business_type.lower()} ensures that we deliver results that exceed expectations.",
            "contact": f"Ready to get started? Contact {company_name} today to learn more about how our {industry.lower()} expertise can benefit your business. We're here to help you succeed."
        }
        
        # Add additional customization based on business type
        if 'restaurant' in business_type.lower() or 'food' in business_type.lower():
            content["services"] = f"We offer delicious {industry.lower()} cuisine with fresh ingredients and exceptional service. Our menu features carefully crafted dishes that celebrate the flavors of {industry.lower()} cooking."
        elif 'tech' in business_type.lower() or 'software' in business_type.lower():
            content["services"] = f"We provide cutting-edge {industry.lower()} technology solutions including software development, system integration, and digital transformation services."
        elif 'consulting' in business_type.lower():
            content["services"] = f"Our expert consultants provide strategic guidance and practical solutions in {industry.lower()}. We help businesses optimize operations and achieve their goals."
        
        # Create and save the website
        website = Website(
            title=content['title'],
            content=content,
            user_id=current_user_id,
            business_type=business_type,
            industry=industry
        )
        website.save()
        
        return jsonify({
            'message': 'Website generated successfully',
            'website': website.to_dict(),
            'note': 'Content generated using template-based system. For AI-powered generation, configure OpenAI API key.'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/regenerate/<website_id>', methods=['POST'])
@check_permission('update_website')
def regenerate_content(website_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        data = request.get_json() or {}
        
        website = Website.find_by_id(website_id)
        if not website:
            return jsonify({'error': 'Website not found'}), 404
        
        # Check if user can update this website
        if user.role != 'admin' and str(website.user_id) != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        section = data.get('section', 'all')  # Which section to regenerate
        
        # Create alternative content based on existing website data
        business_type = website.business_type or 'business'
        industry = website.industry or 'general'
        company_name = website.title.split(' - ')[0] if ' - ' in website.title else 'Your Company'
        
        if section == 'all':
            # Generate alternative full content
            new_content = {
                "title": f"{company_name} - Leading {business_type} Solutions",
                "hero": f"Discover excellence with {company_name}. We're your premier {business_type.lower()} provider in the {industry.lower()} sector, committed to delivering outstanding results.",
                "about": f"{company_name} stands at the forefront of {industry.lower()} innovation. As a trusted {business_type.lower()}, we combine expertise with passion to serve our clients with distinction.",
                "services": f"Our comprehensive {industry.lower()} services are designed to meet your unique needs. From initial consultation to final delivery, we ensure quality and satisfaction in every project.",
                "contact": f"Connect with {company_name} and experience the difference. Let us show you how our {industry.lower()} expertise can transform your business."
            }
            website.content = new_content
            website.title = new_content['title']
        else:
            # Generate alternative content for specific section
            alternatives = {
                'hero': f"Experience the difference with {company_name}. Our {business_type.lower()} expertise in {industry.lower()} delivers exceptional value and results.",
                'about': f"With years of experience in {industry.lower()}, {company_name} has established itself as a premier {business_type.lower()} known for quality and reliability.",
                'services': f"We specialize in {industry.lower()} solutions that drive growth and success. Our {business_type.lower()} services are tailored to exceed your expectations.",
                'contact': f"Take the next step with {company_name}. Contact us today to discover how our {industry.lower()} services can benefit you."
            }
            if section in alternatives:
                website.content[section] = alternatives[section]
        
        website.save()
        
        return jsonify({
            'message': f'Content regenerated successfully',
            'website': website.to_dict(),
            'note': 'Content regenerated using template variations. For AI-powered generation, configure OpenAI API key.'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

