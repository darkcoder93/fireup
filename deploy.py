#!/usr/bin/env python3
"""
Deployment helper script for FIRE Calculator
Run this script to validate your setup before deploying to PythonAnywhere
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    print("Checking requirements...")
    try:
        import django
        print(f"✅ Django {django.get_version()} installed")
    except ImportError:
        print("❌ Django not installed")
        return False
    
    try:
        import whitenoise
        print("✅ WhiteNoise installed")
    except ImportError:
        print("❌ WhiteNoise not installed")
        return False
    
    return True

def check_settings():
    """Check if settings are properly configured"""
    print("\nChecking settings...")
    
    # Check if settings file exists
    settings_file = Path("fire_calculator/settings.py")
    if not settings_file.exists():
        print("❌ settings.py not found")
        return False
    
    print("✅ settings.py found")
    
    # Check for required settings
    with open(settings_file, 'r') as f:
        content = f.read()
        
    required_settings = [
        'ALLOWED_HOSTS',
        'STATIC_ROOT',
        'DEBUG',
        'SECRET_KEY'
    ]
    
    for setting in required_settings:
        if setting in content:
            print(f"✅ {setting} configured")
        else:
            print(f"❌ {setting} not found")
            return False
    
    return True

def check_static_files():
    """Check if static files are properly configured"""
    print("\nChecking static files...")
    
    static_dir = Path("static")
    if static_dir.exists():
        print("✅ static directory found")
    else:
        print("⚠️  static directory not found (will be created)")
    
    return True

def check_database():
    """Check database configuration"""
    print("\nChecking database...")
    
    db_file = Path("db.sqlite3")
    if db_file.exists():
        print("✅ Database file exists")
    else:
        print("⚠️  Database file not found (will be created during migration)")
    
    return True

def main():
    """Main deployment check"""
    print("🚀 FIRE Calculator Deployment Check")
    print("=" * 40)
    
    checks = [
        check_requirements,
        check_settings,
        check_static_files,
        check_database
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✅ All checks passed! Your app is ready for deployment.")
        print("\nNext steps:")
        print("1. Sign up at pythonanywhere.com")
        print("2. Follow the QUICK_DEPLOY.md guide")
        print("3. Upload your code and configure the web app")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Check your settings.py file")
        print("- Make sure all files are in the correct locations")

if __name__ == "__main__":
    main() 