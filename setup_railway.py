#!/usr/bin/env python3
"""
Helper script to generate secure settings for Railway deployment
"""

import os
from django.core.management.utils import get_random_secret_key

def generate_secret_key():
    """Generate a secure Django secret key"""
    return get_random_secret_key()

def main():
    print("🚂 Railway Deployment Helper")
    print("=" * 40)
    
    # Generate secret key
    secret_key = generate_secret_key()
    print(f"\n🔑 Generated Secret Key:")
    print(f"DJANGO_SECRET_KEY={secret_key}")
    
    print(f"\n📋 Environment Variables to set in Railway:")
    print(f"DJANGO_SECRET_KEY={secret_key}")
    print(f"DEBUG=False")
    print(f"EMAIL_HOST_USER=your-email@gmail.com")
    print(f"EMAIL_HOST_PASSWORD=your-gmail-app-password")
    
    print(f"\n💡 Notes:")
    print(f"- DATABASE_URL will be automatically set by Railway")
    print(f"- Make sure your GitHub repo is connected to Railway")
    print(f"- Check the RAILWAY_DEPLOYMENT.md file for detailed steps")
    
    print(f"\n✅ Your app is ready for Railway deployment!")

if __name__ == "__main__":
    main() 