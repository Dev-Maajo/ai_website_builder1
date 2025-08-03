import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

# Import models to initialize database connection
from src.models.database import db
from src.models.role import Role

# Import routes
from src.routes.auth import auth_bp
from src.routes.website import website_bp
from src.routes.role import role_bp
from src.routes.ai import ai_bp
from src.routes.user import user_bp

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-super-secret-jwt-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-super-secret-jwt-key-change-in-production')

# Initialize extensions
jwt = JWTManager(app)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(website_bp, url_prefix='/api/websites')
app.register_blueprint(role_bp, url_prefix='/api/roles')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(user_bp, url_prefix='/api')

# Initialize default roles
with app.app_context():
    Role.initialize_default_roles()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/preview/<website_id>')
def preview_website(website_id):
    """Route for live preview of websites"""
    from src.models.website import Website
    from flask import render_template_string
    
    website = Website.find_by_id(website_id)
    if not website:
        return "Website not found", 404
    
    # Basic HTML template for preview
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ title }}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
            .hero { background: #f4f4f4; padding: 40px; text-align: center; }
            .section { margin: 40px 0; }
            .container { max-width: 1200px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>{{ title }}</h1>
                <p>{{ content.hero or 'Welcome to our website' }}</p>
            </div>
            <div class="section">
                <h2>About Us</h2>
                <p>{{ content.about or 'Learn more about our company and mission.' }}</p>
            </div>
            <div class="section">
                <h2>Services</h2>
                <p>{{ content.services or 'Discover our range of services and offerings.' }}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(template, title=website.title, content=website.content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

