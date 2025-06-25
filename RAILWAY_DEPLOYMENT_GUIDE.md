# Railway Deployment Guide with MySQL

## Prerequisites
- GitHub account with your project pushed
- Railway account (free at railway.app)
- Git workflow with `dev` and `prod` branches

## Step 1: Sign Up for Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Authorize Railway to access your repositories

## Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository: `finance_planning_tracking`
4. **Important:** Select the `prod` branch (not main/master)
5. Railway will automatically deploy from the `prod` branch

## Step 3: Add MySQL Database
1. In your Railway project dashboard, click "New"
2. Select "Database" → "MySQL"
3. Railway will automatically create a `DATABASE_URL` environment variable
4. **Note:** The URL will look like: `mysql://user:password@host:port/database`

## Step 4: Configure Environment Variables
In your Railway project dashboard, go to "Variables" tab and add:

```
DJANGO_SECRET_KEY=your-super-secret-key-here
DEBUG=False
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

**Generate a secret key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 5: Configure Deployment Settings
Railway will automatically detect Django and use the `railway.json` configuration.

## Step 6: Deploy
1. Railway will automatically start building and deploying from the `prod` branch
2. Monitor the build logs for any errors
3. Once deployed, you'll get a URL like: `https://your-app-name.railway.app`

## Step 7: Create Superuser (Optional)
1. Go to Railway dashboard → "Deployments" tab
2. Click on your latest deployment
3. Open the terminal and run:
```bash
python manage.py createsuperuser
```

## Step 8: Test Your App
1. Visit your Railway URL
2. Test all features: registration, login, FIRE calculations, etc.
3. Check that static files are loading correctly

## MySQL Configuration Details

### Database URL Format
Railway provides a MySQL URL in this format:
```
mysql://username:password@host:port/database_name
```

### Django Settings
Your `settings.py` is configured to automatically use the `DATABASE_URL` environment variable.

### Migrations
After deployment, run migrations:
```bash
python manage.py migrate
```

## Troubleshooting

### Common Issues:

1. **CSRF Error (403 Forbidden)**
   - Solution: Added `CSRF_TRUSTED_ORIGINS` in settings.py
   - Make sure your Railway domain is in the trusted origins list

2. **Database Connection Error**
   - Check that `DATABASE_URL` is set correctly
   - Ensure MySQL service is running
   - Verify database credentials

3. **Static Files Not Loading**
   - Check that `collectstatic` ran successfully
   - Verify WhiteNoise configuration

4. **Build Fails**
   - Check Railway build logs
   - Ensure all requirements are in `requirements.txt`
   - Verify `railway.json` syntax

### View Logs:
- Go to Railway dashboard → "Deployments" → Click on deployment → "Logs"

### Restart App:
- Go to Railway dashboard → "Settings" → "Restart"

## Development Workflow

```bash
# 1. Work on dev branch
git checkout dev
git pull origin dev
# ... make changes ...
git add .
git commit -m "feat: add new feature"
git push origin dev

# 2. When ready for production
git checkout prod
git pull origin prod
git merge dev
git push origin prod
# Railway automatically deploys from prod branch
```

## Custom Domain (Optional)
1. Go to Railway dashboard → "Settings" → "Domains"
2. Add your custom domain
3. Update DNS settings as instructed

## Monitoring
- Railway provides basic monitoring in the dashboard
- Check "Metrics" tab for performance data
- Monitor "Deployments" for deployment history

## Cost
- Railway has a generous free tier
- You get $5 credit monthly
- MySQL database is included in free tier
- Pay only if you exceed free limits

## Security Notes
- Never commit `.env` files to git
- Use strong secret keys
- Enable HTTPS (automatic on Railway)
- Keep dependencies updated
- Use branch protection on GitHub for `prod` branch

## Git Workflow Summary
- **Development**: Work on `dev` branch
- **Production**: Merge `dev` → `prod`, Railway auto-deploys
- **Emergency fixes**: Create hotfix branch from `prod`
- **Never work directly on `prod`** - always go through `dev` 