#!/bin/bash
# Automated Deployment Script for Egy360
# This deploys the Django project to Railway and configures 360egy.com

set -e  # Exit on error

echo "🚀 Starting Egy360 Deployment..."

# Navigate to project directory
cd "$(dirname "$0")"

echo "✅ Step 1: Verifying Git status..."
git status

echo "✅ Step 2: Ensuring all changes are committed..."
if [[ -n $(git status -s) ]]; then
    echo "Uncommitted changes found, committing..."
    git add -A
    git commit -m "Auto-commit before deployment"
    git push origin master
fi

echo "✅ Step 3: Logging into Railway..."
railway login

echo "✅ Step 4: Linking to project..."
railway link

echo "✅ Step 5: Deploying to Railway..."
railway up --detach

echo "✅ Step 6: Waiting for deployment..."
sleep 30

echo "✅ Step 7: Running migrations..."
railway run python manage.py migrate --noinput

echo "✅ Step 8: Collecting static files..."
railway run python manage.py collectstatic --noinput

echo "✅ Step 9: Populating database..."
railway run python manage.py populate_comprehensive_data

echo "✅ Step 10: Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'enzo.alihussien90@gmail.com', 'admin123'); print('Admin user ready')" | railway run python manage.py shell

echo "✅ Step 11: Generating domain..."
railway domain

echo "🎉 DEPLOYMENT COMPLETE!"
echo "Your site is live!"
railway status
