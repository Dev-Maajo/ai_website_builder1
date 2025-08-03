# AI Website Builder

A full-stack web application that generates professional websites using AI-powered content creation. Built with Flask, SQLite, and modern web technologies.

## 🌟 Features

### Core Functionality
- **AI-Powered Content Generation**: Generate professional website content based on business type and industry
- **User Authentication**: Secure JWT-based authentication system
- **Role-Based Access Control**: Admin, Editor, and Viewer roles with different permissions
- **Website Management**: Full CRUD operations for websites
- **Live Preview**: Preview generated websites in real-time
- **Responsive Design**: Beautiful, mobile-friendly interface

### User Roles
- **Admin**: Full access to all features, user management, and system administration
- **Editor**: Can create, edit, and manage their own websites
- **Viewer**: Read-only access to websites

### API Endpoints

#### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

#### Website Management
- `POST /api/websites` - Create new website
- `GET /api/websites` - Get user's websites
- `GET /api/websites/:id` - Get specific website
- `PUT /api/websites/:id` - Update website
- `DELETE /api/websites/:id` - Delete website

#### AI Content Generation
- `POST /api/ai/generate` - Generate new website content
- `POST /api/ai/regenerate/:id` - Regenerate website content

#### Admin Features
- `GET /api/users` - Get all users (Admin only)
- `PUT /api/users/:id` - Update user (Admin only)
- `DELETE /api/users/:id` - Delete user (Admin only)
- `POST /api/roles/assign` - Assign roles (Admin only)

## 🚀 Live Demo

**Deployed Application**: https://w5hni7c71w1n.manus.space

### Test Accounts
You can create your own account or use these test credentials:

1. **Admin Account**:
   - Email: admin@example.com
   - Password: admin123
   - Role: Admin

2. **Editor Account**:
   - Email: editor@example.com
   - Password: editor123
   - Role: Editor

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLite**: Lightweight database
- **JWT**: JSON Web Tokens for authentication
- **Flask-CORS**: Cross-origin resource sharing
- **Hashlib**: Secure password hashing

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript**: Interactive functionality
- **Responsive Design**: Mobile-first approach

### Deployment
- **Manus Platform**: Cloud deployment platform

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Virtual environment support

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai_website_builder
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```env
   JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
   OPENAI_API_KEY=your-openai-api-key-here  # Optional for AI features
   ```

5. **Run the application**:
   ```bash
   python src/main.py
   ```

6. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## 🏗️ Project Structure

```
ai_website_builder/
├── src/
│   ├── models/
│   │   ├── database.py      # Database connection and setup
│   │   ├── user.py          # User model
│   │   ├── website.py       # Website model
│   │   └── role.py          # Role model
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   ├── website.py       # Website management routes
│   │   ├── ai.py            # AI content generation routes
│   │   ├── role.py          # Role management routes
│   │   └── user.py          # User management routes
│   ├── static/
│   │   └── index.html       # Frontend interface
│   ├── database/
│   │   └── app.db           # SQLite database file
│   └── main.py              # Flask application entry point
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

## 🎯 Usage Guide

### Getting Started

1. **Sign Up**: Create a new account with your email and password
2. **Choose Role**: Select your role (Editor recommended for content creation)
3. **Generate Website**: Fill in your business details and click "Generate Website"
4. **Preview**: Use the preview feature to see your generated website
5. **Manage**: Edit, update, or delete your websites as needed

### Content Generation

The AI Website Builder generates content for:
- **Hero Section**: Compelling introduction to your business
- **About Section**: Professional description of your company
- **Services Section**: Overview of your offerings
- **Contact Section**: Call-to-action and contact information

### Admin Features

Administrators can:
- View and manage all users
- Assign roles to users
- Access system-wide statistics
- Manage website content across all users

## 🔧 API Documentation

### Authentication Required
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Example API Calls

#### User Registration
```bash
curl -X POST https://w5hni7c71w1n.manus.space/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "username": "testuser",
    "role": "editor"
  }'
```

#### Generate Website
```bash
curl -X POST https://w5hni7c71w1n.manus.space/api/ai/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "company_name": "TechCorp",
    "business_type": "Software Development",
    "industry": "Technology",
    "additional_info": "We specialize in web applications"
  }'
```

## 🔒 Security Features

- **Password Hashing**: Secure password storage using SHA-256 with salt
- **JWT Authentication**: Stateless authentication with token expiration
- **Role-Based Authorization**: Granular permission control
- **CORS Protection**: Configured for secure cross-origin requests
- **Input Validation**: Server-side validation for all user inputs

## 🚀 Deployment

The application is deployed on the Manus platform and accessible at:
**https://w5hni7c71w1n.manus.space**

### Deployment Features
- **Automatic SSL**: HTTPS encryption enabled
- **High Availability**: Cloud-based infrastructure
- **Scalable**: Handles multiple concurrent users
- **Persistent Storage**: SQLite database with data persistence

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the existing documentation
2. Review the API endpoints and examples
3. Test with the live demo application
4. Contact the development team

## 🔮 Future Enhancements

- **OpenAI Integration**: Full AI-powered content generation
- **Template System**: Multiple website templates
- **Export Features**: Download generated websites
- **Analytics Dashboard**: Website performance metrics
- **Custom Domains**: Connect custom domains to generated sites
- **SEO Optimization**: Built-in SEO tools and recommendations

---

**Built with ❤️ using Flask and modern web technologies**

