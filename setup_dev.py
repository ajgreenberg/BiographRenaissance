#!/usr/bin/env python
"""
Setup script for BiographRenaissance development environment
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_environment():
    """Set up the development environment"""
    
    # Add the project directory to Python path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_dir)
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BiographRenaissance.settings')
    
    # Setup Django
    django.setup()
    
    print("✅ Django environment setup complete!")

def run_migrations():
    """Run database migrations"""
    print("🔄 Running migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    print("✅ Migrations complete!")

def create_superuser():
    """Create a superuser for admin access"""
    print("👤 Creating superuser...")
    try:
        execute_from_command_line(['manage.py', 'createsuperuser'])
        print("✅ Superuser created!")
    except Exception as e:
        print(f"⚠️  Superuser creation failed: {e}")

def main():
    """Main setup function"""
    print("🚀 Setting up BiographRenaissance development environment...")
    
    try:
        setup_environment()
        run_migrations()
        create_superuser()
        
        print("\n🎉 Setup complete! You can now:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000/swagger/")
        print("3. Admin: http://127.0.0.1:8000/admin/")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
