# Git Workflow: Dev and Prod Branches

## Branch Strategy
- **`dev`** - Development branch for new features and fixes
- **`prod`** - Production branch (equivalent to master/main)

## Initial Setup

### 1. Create and Switch to Dev Branch
```bash
# Create and switch to dev branch
git checkout -b dev

# Push dev branch to remote
git push -u origin dev
```

### 2. Create Prod Branch from Dev
```bash
# Create prod branch from dev
git checkout -b prod

# Push prod branch to remote
git push -u origin prod
```

### 3. Set Prod as Default Branch (Optional)
```bash
# On GitHub/GitLab, go to repository settings
# Set 'prod' as the default branch instead of 'main' or 'master'
```

## Daily Workflow

### Development Workflow
```bash
# Always start from dev branch
git checkout dev
git pull origin dev

# Create feature branch (optional)
git checkout -b feature/new-feature

# Make your changes
# ... code changes ...

# Commit changes
git add .
git commit -m "Add new feature"

# Push to dev
git push origin dev
# or if using feature branch:
git push origin feature/new-feature
# Then merge to dev via PR
```

### Production Deployment
```bash
# When ready to deploy to production
git checkout prod
git pull origin prod

# Merge dev into prod
git merge dev

# Push to prod
git push origin prod

# Railway will automatically deploy from prod branch
```

## Railway Configuration

Railway is now configured to deploy from the `prod` branch:
- `railway.json` specifies `"branch": "prod"` for production
- Every push to `prod` will trigger a deployment

## Best Practices

### 1. Never Work Directly on Prod
- Always develop on `dev` branch
- Only merge `dev` → `prod` when ready for production

### 2. Use Pull Requests (Recommended)
- Create PR from `dev` to `prod`
- Review changes before merging
- Use GitHub/GitLab PR interface

### 3. Commit Messages
- Use clear, descriptive commit messages
- Prefix with type: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`

### 4. Testing
- Test thoroughly on `dev` before merging to `prod`
- Use staging environment if possible

## Commands Summary

```bash
# Development
git checkout dev
git pull origin dev
# ... make changes ...
git add .
git commit -m "feat: add new feature"
git push origin dev

# Production deployment
git checkout prod
git pull origin prod
git merge dev
git push origin prod
```

## Branch Protection (Recommended)

On GitHub/GitLab, set up branch protection for `prod`:
- Require pull request reviews
- Require status checks to pass
- Restrict direct pushes to `prod`
- Only allow merges via PR

## Emergency Fixes

For urgent production fixes:
```bash
# Create hotfix branch from prod
git checkout prod
git checkout -b hotfix/urgent-fix

# Make minimal fix
# ... fix code ...

# Commit and push
git add .
git commit -m "fix: urgent production fix"
git push origin hotfix/urgent-fix

# Merge to both prod and dev
git checkout prod
git merge hotfix/urgent-fix
git push origin prod

git checkout dev
git merge hotfix/urgent-fix
git push origin dev

# Delete hotfix branch
git branch -d hotfix/urgent-fix
git push origin --delete hotfix/urgent-fix
``` 