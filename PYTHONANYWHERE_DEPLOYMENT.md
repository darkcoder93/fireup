# PythonAnywhere Deployment Guide for FIRE Calculator

## Prerequisites
- PythonAnywhere account (free tier is sufficient)
- Git repository with your code (GitHub, GitLab, etc.)

## Step 1: Sign up for PythonAnywhere
1. Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Click "Create a Beginner account" (free)
3. Choose a username and password
4. Verify your email

## Step 2: Upload Your Code

### Option A: Using Git (Recommended)
1. Open a Bash console in PythonAnywhere
2. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/fire-calculator.git
   cd fire-calculator
   ```

### Option B: Using Upload
1. Go to Files tab in PythonAnywhere
2. Create a new directory for your project
3. Upload your project files

## Step 3: Set Up Virtual Environment
```bash
# Create virtual environment
python3 -m venv fire_calculator_env

# Activate virtual environment
source fire_calculator_env/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Step 4: Configure Django Settings
1. Edit `fire_calculator/settings.py`
2. Update `ALLOWED_HOSTS` with your PythonAnywhere domain:
   ```python
   ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost', '127.0.0.1']
   ```
3. Make sure `DEBUG = False` for production

## Step 5: Set Up Database
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Step 6: Collect Static Files
```bash
python manage.py collectstatic
```

## Step 7: Configure Web App
1. Go to Web tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python version (3.11)
5. Set source code directory to your project folder
6. Set working directory to your project folder

## Step 8: Configure WSGI File
1. Click on the WSGI configuration file link
2. Replace the content with:
   ```python
   import os
   import sys
   
   # Add your project directory to the sys.path
   path = '/home/yourusername/fire-calculator'
   if path not in sys.path:
       sys.path.append(path)
   
   # Set environment variable
   os.environ['DJANGO_SETTINGS_MODULE'] = 'fire_calculator.settings'
   
   # Import Django WSGI application
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

## Step 9: Configure Static Files
1. In the Web tab, go to "Static files" section
2. Add static file mappings:
   - URL: `/static/`
   - Directory: `/home/yourusername/fire-calculator/staticfiles`

## Step 10: Reload Web App
1. Click "Reload" button in the Web tab
2. Your app should now be live at `yourusername.pythonanywhere.com`

## Step 11: Test Your Application
1. Visit your domain
2. Test all functionality:
   - User registration/login
   - Dashboard
   - Monthly tracking
   - Goals
   - Analytics
   - FIRE calculator

## Troubleshooting

### Common Issues:
1. **Import errors**: Make sure virtual environment is activated
2. **Static files not loading**: Check static files configuration
3. **Database errors**: Run migrations again
4. **Permission errors**: Check file permissions

### Debug Mode (Temporary)
If you need to debug, temporarily set `DEBUG = True` in settings.py

### Logs
Check error logs in the Web tab for debugging information

## Security Notes
- Keep `DEBUG = False` in production
- Use strong passwords for admin accounts
- Regularly update dependencies
- Monitor error logs

## Custom Domain (Paid Feature)
If you want a custom domain:
1. Upgrade to paid plan
2. Configure DNS settings
3. Update `ALLOWED_HOSTS` in settings.py

## Backup Strategy
- Regularly backup your database
- Keep your code in version control
- Export important data periodically

## Performance Tips
- Use PythonAnywhere's MySQL database for better performance
- Optimize static files
- Monitor resource usage

Your FIRE Calculator should now be live and accessible to users worldwide! 