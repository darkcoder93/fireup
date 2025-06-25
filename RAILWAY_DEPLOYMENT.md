# Railway Deployment Guide for FIRE Calculator

## Prerequisites
- GitHub account with your project pushed
- Railway account (free at railway.app)

## Step 1: Sign Up for Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Authorize Railway to access your repositories

## Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository: `finance_planning_tracking`
4. Select the branch (usually `main` or `master`)

## Step 3: Add PostgreSQL Database
1. In your Railway project dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a `DATABASE_URL` environment variable

## Step 4: Configure Environment Variables
In your Railway project dashboard, go to "Variables" tab and add:

```
DJANGO_SECRET_KEY=your-super-secret-key-here
DEBUG=False
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

**Generate a secret key:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 5: Configure Deployment Settings
Railway will automatically detect Django and use the `railway.json` configuration.

## Step 6: Deploy
1. Railway will automatically start building and deploying
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

## Troubleshooting

### Common Issues:
1. **Build fails**: Check that all requirements are in `requirements.txt`
2. **Database errors**: Ensure `DATABASE_URL` is set correctly
3. **Static files not loading**: Check that `collectstatic` ran successfully
4. **Email not working**: Verify Gmail app password is correct

### View Logs:
- Go to Railway dashboard → "Deployments" → Click on deployment → "Logs"

### Restart App:
- Go to Railway dashboard → "Settings" → "Restart"

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
- PostgreSQL database is included in free tier
- Pay only if you exceed free limits

## Security Notes
- Never commit `.env` files to git
- Use strong secret keys
- Enable HTTPS (automatic on Railway)
- Keep dependencies updated 