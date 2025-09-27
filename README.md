# BiographRenaissance - Modern BioGraph API

A modern, clean implementation of the BioGraph API with JWT authentication, social login, and RESTful endpoints.

## 🚀 Features

### Authentication
- **JWT Authentication** with SimpleJWT
- **User Registration** with email validation
- **User Login** with secure password handling
- **Token Refresh** for seamless user experience
- **Social Authentication** (Google, Apple) via Django Allauth
- **Password Change** functionality

### User Management
- **Custom User Model** with extended fields
- **User Profiles** with privacy settings
- **User Settings** (notifications, theme, etc.)
- **User Statistics** and activity tracking
- **Social Account Management**

### API Features
- **RESTful API** with Django REST Framework
- **Swagger Documentation** with drf-yasg
- **CORS Support** for frontend integration
- **Pagination** for large datasets
- **Search Functionality** for users

## 🏗️ Architecture

### Tech Stack
- **Django 4.2.7** - Web framework
- **Django REST Framework** - API framework
- **SimpleJWT** - JWT authentication
- **Django Allauth** - Social authentication
- **SQLite** - Database (development)
- **Cloudinary** - Image storage
- **Swagger** - API documentation

### Project Structure
```
BiographRenaissance/
├── BiographRenaissance/          # Project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI configuration
├── core/                    # Core app
│   ├── models.py           # User models
│   ├── views.py            # API views
│   ├── serializers.py      # Data serializers
│   ├── urls.py             # API endpoints
│   └── admin.py            # Admin interface
├── requirements.txt         # Dependencies
├── test_auth.py            # Authentication tests
└── README.md              # This file
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd BiographRenaissance
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python3 manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python3 manage.py runserver
   ```

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/v1/
```

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "bio": "",
    "profile_picture": "",
    "date_of_birth": null,
    "is_verified": false,
    "subscription_status": "free",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

#### Login User
```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### Refresh Token
```http
POST /api/v1/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### User Endpoints

#### Get Profile
```http
GET /api/v1/profile/
Authorization: Bearer <access_token>
```

#### Update Profile
```http
PUT /api/v1/profile/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith",
  "bio": "Updated bio",
  "phone_number": "+1987654321"
}
```

#### Change Password
```http
POST /api/v1/change-password/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "oldpassword123",
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```

#### Get User Stats
```http
GET /api/v1/stats/
Authorization: Bearer <access_token>
```

#### Search Users
```http
GET /api/v1/users/?search=john
Authorization: Bearer <access_token>
```

### User Settings Endpoints

#### Get Settings
```http
GET /api/v1/settings/
Authorization: Bearer <access_token>
```

#### Update Settings
```http
PUT /api/v1/settings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "profile_visibility": "friends",
  "email_notifications": true,
  "push_notifications": false,
  "theme": "dark"
}
```

## 🧪 Testing

### Run Authentication Tests
```bash
python3 test_auth.py
```

### Manual Testing with Swagger
1. Start the server: `python3 manage.py runserver`
2. Visit: http://127.0.0.1:8000/swagger/
3. Use the interactive API documentation

### Test with curl
```bash
# Register a user
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "testpassword123",
    "password_confirm": "testpassword123"
  }'

# Login
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/biographmodern

# Cloudinary (for image storage)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Social Authentication
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret
APPLE_CLIENT_ID=your-apple-client-id
```

### Social Authentication Setup

#### Google OAuth2
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth2 credentials
5. Add authorized redirect URIs:
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
   - `http://localhost:8000/accounts/google/login/callback/`

#### Apple Sign In
1. Go to [Apple Developer Console](https://developer.apple.com/)
2. Create a new App ID
3. Enable Sign In with Apple
4. Create a Service ID
5. Configure the service

## 🚀 Deployment

### Production Settings
Create `settings_production.py`:

```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biographmodern_prod',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files
STATIC_ROOT = '/path/to/static/files'
MEDIA_ROOT = '/path/to/media/files'

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000
CMD ["gunicorn", "BiographRenaissance.wsgi:application"]
```

## 📈 Next Steps

### Planned Features
- [ ] **Biograph Models** - Core content models
- [ ] **File Upload** - Audio/video/image handling
- [ ] **Social Features** - Friends, followers, likes
- [ ] **Search & Discovery** - Advanced search functionality
- [ ] **Push Notifications** - Real-time notifications
- [ ] **Analytics** - User engagement tracking
- [ ] **Admin Dashboard** - Enhanced admin interface

### Integration
- [ ] **iOS App Integration** - Connect with existing iOS app
- [ ] **Web Frontend** - React/Vue.js frontend
- [ ] **Mobile App** - React Native or Flutter app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Email: support@biograph.com
- Documentation: http://127.0.0.1:8000/swagger/

---

**BiographRenaissance** - Modern BioGraph API with JWT Authentication and Social Login
# Railway deployment test
