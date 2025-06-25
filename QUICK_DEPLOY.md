# Quick PythonAnywhere Deployment

## 1. Sign Up
- Go to pythonanywhere.com
- Create free account
- Note your username (your domain will be `username.pythonanywhere.com`)

## 2. Upload Code
**Option A: Git (Recommended)**
```bash
# In PythonAnywhere Bash console
git clone https://github.com/yourusername/fire-calculator.git
cd fire-calculator
```

**Option B: File Upload**
- Go to Files tab
- Upload your project folder

## 3. Setup Environment
```bash
# Create virtual environment
python3 -m venv fire_calculator_env
source fire_calculator_env/bin/activate

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## 4. Configure Web App
1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.11**

## 5. Configure Settings
- **Source code**: `/home/yourusername/fire-calculator`
- **Working directory**: `/home/yourusername/fire-calculator`
- **Virtual environment**: `/home/yourusername/fire_calculator_env`

## 6. Edit WSGI File
Replace content with:
```python
import os
import sys
path = '/home/yourusername/fire-calculator'
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'fire_calculator.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 7. Configure Static Files
- **URL**: `/static/`
- **Directory**: `/home/yourusername/fire-calculator/staticfiles`

## 8. Update Settings
Edit `fire_calculator/settings.py`:
```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost', '127.0.0.1']
DEBUG = False
```

## 9. Reload & Test
1. Click **Reload** in Web tab
2. Visit `yourusername.pythonanywhere.com`
3. Test all features

## Troubleshooting
- Check error logs in Web tab
- Verify all paths are correct
- Make sure virtual environment is activated
- Run `python manage.py migrate` if database errors occur

Your app will be live at: `https://yourusername.pythonanywhere.com` 