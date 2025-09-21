#!/usr/bin/env python3
"""
Railway Deployment Helper for BiographRenaissance
================================================

This script helps prepare your BiographRenaissance app for Railway deployment.
It will:
1. Export current SQLite data
2. Generate environment variables
3. Create deployment checklist
4. Test local configuration

Usage:
    python3 deploy_to_railway.py
"""

import os
import json
import subprocess
import sys
from datetime import datetime

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def export_sqlite_data():
    """Export data from SQLite database"""
    print("\n📊 Exporting SQLite data...")
    
    # Check if SQLite database exists
    if not os.path.exists('db.sqlite3'):
        print("⚠️  No SQLite database found. Skipping data export.")
        return True
    
    # Export data
    success = run_command(
        "python3 manage.py dumpdata --natural-foreign --natural-primary --indent=2 > railway_data_export.json",
        "Exporting SQLite data to JSON"
    )
    
    if success:
        print("📁 Data exported to: railway_data_export.json")
        print("💡 You can import this data to Railway PostgreSQL after deployment")
    
    return success

def generate_env_template():
    """Generate environment variables template"""
    print("\n🔧 Generating environment variables template...")
    
    env_template = """# BiographRenaissance Environment Variables for Railway
# Copy these to your Railway project environment variables

# Railway automatically provides these:
# DATABASE_URL=postgresql://user:pass@host:port/dbname
# RAILWAY_ENVIRONMENT=production

# Django Settings
SECRET_KEY=your-secret-key-here-replace-with-random-string
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app,localhost,127.0.0.1

# API Settings
CORS_ALLOWED_ORIGINS=https://your-app-name.railway.app,http://localhost:3000

# Cloudinary (for file storage)
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-cloudinary-key
CLOUDINARY_API_SECRET=your-cloudinary-secret

# Twilio (for SMS)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
"""
    
    with open('railway_env_template.txt', 'w') as f:
        f.write(env_template)
    
    print("📁 Environment template created: railway_env_template.txt")
    print("💡 Copy these variables to your Railway project settings")

def create_deployment_checklist():
    """Create deployment checklist"""
    print("\n📋 Creating deployment checklist...")
    
    checklist = """# 🚂 Railway Deployment Checklist for BiographRenaissance

## Pre-Deployment
- [ ] Railway account created
- [ ] GitHub repository connected to Railway
- [ ] PostgreSQL database added to Railway project
- [ ] Environment variables configured in Railway
- [ ] Secret key generated (use: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

## Deployment Steps
- [ ] Push code to GitHub repository
- [ ] Railway automatically deploys
- [ ] Check deployment logs in Railway dashboard
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Import data: `python manage.py loaddata railway_data_export.json`

## Post-Deployment Testing
- [ ] Test API root: https://your-app.railway.app/
- [ ] Test admin: https://your-app.railway.app/admin/
- [ ] Test Swagger: https://your-app.railway.app/swagger/
- [ ] Test phone authentication endpoints
- [ ] Test user migration from MongoDB clone

## Cost Verification
- [ ] PostgreSQL: $5/month
- [ ] Web Service: $5/month
- [ ] Total: $10/month (vs MongoDB Atlas $57/month)
- [ ] Savings: $47/month ($564/year)

## Next Steps
- [ ] Set up custom domain (optional)
- [ ] Configure monitoring alerts
- [ ] Set up automated backups
- [ ] Migrate remaining users from MongoDB clone
- [ ] Migrate biograph content
- [ ] Set up file storage migration (S3 → Cloudinary)

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open('railway_deployment_checklist.md', 'w') as f:
        f.write(checklist)
    
    print("📁 Deployment checklist created: railway_deployment_checklist.md")

def test_local_configuration():
    """Test local configuration"""
    print("\n🧪 Testing local configuration...")
    
    tests = [
        ("python3 manage.py check", "Django configuration check"),
        ("python3 manage.py showmigrations", "Migration status check"),
        ("python3 -c \"from BiographRenaissance.settings import DATABASES; print('Database:', DATABASES['default']['ENGINE'])\"", "Database configuration check"),
    ]
    
    all_passed = True
    for command, description in tests:
        if not run_command(command, description):
            all_passed = False
    
    return all_passed

def main():
    """Main deployment preparation function"""
    print("🚂 BiographRenaissance Railway Deployment Preparation")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Please run this script from the BiographRenaissance directory")
        sys.exit(1)
    
    # Run all preparation steps
    steps = [
        ("Testing local configuration", test_local_configuration),
        ("Exporting SQLite data", export_sqlite_data),
        ("Generating environment template", generate_env_template),
        ("Creating deployment checklist", create_deployment_checklist),
    ]
    
    all_success = True
    for step_name, step_function in steps:
        print(f"\n📋 {step_name}...")
        if not step_function():
            all_success = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT PREPARATION SUMMARY")
    print("=" * 60)
    
    if all_success:
        print("✅ All preparation steps completed successfully!")
        print("\n🚀 Ready for Railway deployment!")
        print("\n📁 Generated files:")
        print("   • railway_data_export.json - Your SQLite data")
        print("   • railway_env_template.txt - Environment variables")
        print("   • railway_deployment_checklist.md - Step-by-step guide")
        print("\n💰 Cost savings: $47/month ($564/year) vs MongoDB Atlas")
        print("\n🎯 Next step: Follow the checklist in railway_deployment_checklist.md")
    else:
        print("❌ Some preparation steps failed. Please check the errors above.")
        print("💡 You can still proceed with deployment, but some features may not work.")
    
    print("\n🌐 Railway Dashboard: https://railway.app/dashboard")
    print("📚 Railway Docs: https://docs.railway.app")

if __name__ == '__main__':
    main()
