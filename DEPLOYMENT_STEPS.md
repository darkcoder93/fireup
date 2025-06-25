# PythonAnywhere Deployment Guide - Step by Step

## Step 1: Sign Up for PythonAnywhere

1. Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Click "Create a Beginner account" (free)
3. Choose a username (this will be your domain: `yourusername.pythonanywhere.com`)
4. Enter your email and password
5. Verify your email address

## Step 2: Prepare Your Code for Upload

### Option A: Using Git (Recommended)
1. Push your code to GitHub/GitLab if not already done
2. Make sure your repository is public (for free accounts)

### Option B: Using File Upload
1. Zip your entire `fire_calculator` folder
2. Keep the folder structure intact

## Step 3: Upload Your Code to PythonAnywhere

### If using Git:
1. Go to the **Consoles** tab in PythonAnywhere
2. Click **Bash** to open a new console
3. Run these commands:
   ```bash
   git clone https://github.com/yourusername/fire-calculator.git
   cd fire-calculator
   ls  # Verify files are there
   ```

### If using File Upload:
1. Go to the **Files** tab in PythonAnywhere
2. Create a new directory called `fire-calculator`
3. Upload your zipped file and extract it
4. Or upload files individually

## Step 4: Set Up Virtual Environment

In the Bash console, run:
```bash
# Create virtual environment
python3 -m venv fire_calculator_env

# Activate it
source fire_calculator_env/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Step 5: Configure Django Settings

1. Go to the **Files** tab
2. Navigate to `fire-calculator/fire_calculator/settings.py`
3. Click on the file to edit it
4. Update the `ALLOWED_HOSTS` line:
   ```python
   ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost', '127.0.0.1']
   ```
   (Replace `yourusername` with your actual PythonAnywhere username)

5. Make sure `DEBUG = False` for production

## Step 6: Set Up Database

In the Bash console (with virtual environment activated):
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 8: Configure Web App

1. Go to the **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Choose **Manual configuration** (not Django)
4. Select **Python 3.11** (or latest available)
5. Click **Next**

## Step 9: Configure Source Code and Working Directory

In the Web app configuration:
1. **Source code**: `/home/yourusername/fire-calculator`
2. **Working directory**: `/home/yourusername/fire-calculator`
3. **WSGI configuration file**: Click the link to edit it

## Step 10: Edit WSGI File

Replace the entire content of the WSGI file with:
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

**Important**: Replace `yourusername` with your actual PythonAnywhere username!

## Step 11: Configure Virtual Environment

In the Web app configuration:
1. **Virtual environment**: `/home/yourusername/fire_calculator_env`
2. **Python version**: 3.11 (or your chosen version)

## Step 12: Configure Static Files

In the **Static files** section:
1. **URL**: `/static/`
2. **Directory**: `/home/yourusername/fire-calculator/staticfiles`

## Step 13: Reload Your Web App

1. Click the **Reload** button
2. Wait for the green checkmark
3. Your app should now be live!

## Step 14: Test Your Application

1. Visit `yourusername.pythonanywhere.com`
2. Test all functionality:
   - User registration/login
   - Dashboard
   - Monthly tracking
   - Goals
   - Analytics
   - FIRE calculator

## Troubleshooting

### Common Issues:

**1. Import Errors**
- Make sure virtual environment is activated
- Check that all requirements are installed
- Verify the WSGI file path is correct

**2. Static Files Not Loading**
- Check static files configuration in Web tab
- Verify `collectstatic` was run
- Check file permissions

**3. Database Errors**
- Run migrations again: `python manage.py migrate`
- Check database configuration

**4. 500 Server Error**
- Check error logs in the Web tab
- Temporarily set `DEBUG = True` to see detailed errors
- Check the WSGI file syntax

### Debug Mode (Temporary)
If you need to debug, edit `settings.py`:
```python
DEBUG = True
```
Then reload the web app.

### Check Logs
- Go to Web tab
- Click on "Error log" to see detailed error messages

## Security Notes

- Keep `DEBUG = False` in production
- Use strong passwords for admin accounts
- Regularly update dependencies
- Monitor error logs

## Your App URL
Your FIRE Calculator will be live at:
`https://yourusername.pythonanywhere.com`

## Next Steps After Deployment

1. **Test all features** thoroughly
2. **Create admin account** and test admin panel
3. **Set up regular backups** of your database
4. **Monitor performance** and error logs
5. **Consider upgrading** to paid plan for custom domain

## Need Help?

- Check PythonAnywhere's documentation
- Look at error logs in the Web tab
- Test locally first with `DEBUG = False`
- Make sure all file paths are correct

Your FIRE Calculator should now be live and accessible to users worldwide! 🚀 