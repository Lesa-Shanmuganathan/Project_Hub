# Deploying College Project Hub to Render

This guide walks you through deploying your College Project Hub Django application to Render, a modern platform for deploying web applications.

## 📋 Prerequisites

1. **GitHub Account** - Push your code to GitHub (Render deploys from Git)
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Cloudinary Account** (optional) - For image storage (sign up at [cloudinary.com](https://cloudinary.com))

## 🚀 Step-by-Step Deployment Guide

### Step 1: Prepare Your Local Repository

```bash
cd "c:\Users\Lesa Shan\Documents\Projectss\Django project\college_project_hub"

# Initialize git if not already done
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: College Project Hub"
```

### Step 2: Push to GitHub

1. Go to [github.com/new](https://github.com/new) and create a new repository
2. Name it `college-project-hub` (or your preferred name)
3. **Do NOT** initialize with README (you already have one)
4. Copy the commands shown and run them:

```bash
git remote add origin https://github.com/YOUR_USERNAME/college-project-hub.git
git branch -M main
git push -u origin main
```

### Step 3: Sign Up on Render

1. Visit [render.com](https://render.com)
2. Click "Sign up"
3. Choose GitHub as your sign-up method
4. Authorize Render to access your GitHub account

### Step 4: Create a New Web Service

1. In Render Dashboard, click **New +** → **Web Service**
2. Select **GitHub** and authorize if needed
3. Find and select your `college-project-hub` repository
4. Configure settings:

| Setting | Value |
|---------|-------|
| **Name** | `college-project-hub` |
| **Environment** | `Python` |
| **Region** | Choose closest to your users (e.g., Oregon, Virginia) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `gunicorn college_project_hub.wsgi:application` |
| **Plan** | Free (or Starter/Pro as needed) |

### Step 5: Set Environment Variables

1. In the Web Service settings, scroll to **Environment**
2. Add the following variables:

```
DEBUG = false
ALLOWED_HOSTS = your-app-name.onrender.com
SECRET_KEY = [Render will generate this automatically]
DATABASE_URL = [Render will link from PostgreSQL service]
```

For Cloudinary (if using):
```
CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = your_api_key
CLOUDINARY_API_SECRET = your_api_secret
```

### Step 6: Create PostgreSQL Database

1. In Render Dashboard, click **New +** → **PostgreSQL**
2. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `college-hub-db` |
| **Database** | `collegedb` |
| **User** | `postgres` |
| **Region** | Same as your Web Service |
| **Plan** | Free |

3. Once created, the `DATABASE_URL` will be auto-linked to your Web Service

### Step 7: Deploy

1. Click **Deploy** button
2. Watch the build logs - deployment typically takes 2-5 minutes
3. Once complete, you'll see "Live" status and a URL like `https://college-project-hub.onrender.com`

### Step 8: Initialize Database

After first deployment:

1. Go to your app URL and check if it loads
2. To create admin user via Render console:
   - Click your service name in Render
   - Go to **Shell** tab
   - Run: `python manage.py createsuperuser`
   - Enter username, email, and password

Or use the seed command:
```bash
python manage.py setup_initial_data
```

3. Visit `https://your-app.onrender.com/admin/` and login

## 📊 Database Migration from SQLite to PostgreSQL

When deploying, Render automatically uses PostgreSQL (via `DATABASE_URL`).

To migrate existing data:

1. **Export local SQLite data:**
   ```bash
   python manage.py dumpdata > data.json
   ```

2. **After deploying to Render:**
   - Push `data.json` to your GitHub repo
   - From Render Shell, run:
     ```bash
     python manage.py loaddata data.json
     ```

## 🔑 Environment Variables

Key variables needed on Render:

```
# Django Settings
DEBUG = false
SECRET_KEY = [Auto-generated]
ALLOWED_HOSTS = your-app-name.onrender.com,www.your-app-name.onrender.com

# Database
DATABASE_URL = [Auto-linked from PostgreSQL]

# URLs and Domains
CSRF_TRUSTED_ORIGINS = https://your-app-name.onrender.com

# Optional: File Storage
CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = your_api_key
CLOUDINARY_API_SECRET = your_api_secret
```

## 📁 File Structure for Deployment

Your deployment files are already set up:

```
├── render.yaml           # ✅ Render configuration
├── build.sh             # ✅ Build script
├── requirements.txt     # ✅ Python dependencies
├── Procfile             # Optional: redundant with render.yaml
├── college_project_hub/
│   ├── settings.py      # ✅ Updated for environment variables
│   ├── wsgi.py
│   └── ...
└── manage.py
```

## 🚨 Troubleshooting Deployment

### "Service could not be started"
- Check build logs for error messages
- Ensure all environment variables are set
- Run migrations manually from Shell tab

### "Database connection error"
- Verify `DATABASE_URL` is set
- Wait 1-2 minutes for Postgres service to be available
- Restart the service from Render dashboard

### "Static files not loading"
- Ensure `STATIC_ROOT` and `STATIC_URL` are configured
- Run: `python manage.py collectstatic --noinput`
- Clear Render's build cache: **Settings** → **Clear Build Cache** → **Redeploy**

### "502 Bad Gateway"
- Check application logs in Render
- Ensure Gunicorn is starting correctly
- Verify `ALLOWED_HOSTS` includes your Render domain

### "Admin panel returns 404"
- Ensure migrations ran: `python manage.py migrate` in Shell
- Create superuser: `python manage.py createsuperuser`

## 📈 Upgrading Your Plan

Free tier limitations:
- Spins down after 15 minutes of inactivity
- Limited database connections
- 0.5 GB disk space

For production:
1. Upgrade to **Starter** ($7/month) - always active
2. Consider dedicated database plan
3. Enable auto-deploy on git push

**Upgrade Steps:**
1. Go to service **Settings**
2. Scroll to **Plan**
3. Select desired plan and confirm

## 🔄 Continuous Deployment

Render auto-deploys when you push to main:

```bash
# Make changes locally
git add .
git commit -m "Update features"
git push origin main

# Automatically deploys within 1-2 minutes!
```

To disable auto-deploy:
- Service **Settings** → **Auto-Deploy** → Toggle OFF

## 📱 Custom Domain (Optional)

To use your own domain:

1. Purchase domain (Namecheap, GoDaddy, etc.)
2. In Render Service Settings → **Custom Domains** → **Add Custom Domain**
3. Update DNS records with the CNAME provided by Render
4. Wait 24-48 hours for DNS propagation

Example DNS record:
```
Type: CNAME
Name: www
Value: college-project-hub.onrender.com
```

## 🔐 Security Best Practices

✅ **Already configured:**
- HTTPS/SSL enabled automatically
- `SECRET_KEY` auto-generated
- Database credentials secured
- WhiteNoise for static files

📋 **Additional recommendations:**
1. Keep dependencies updated: `pip list --outdated`
2. Use strong database passwords
3. Never commit `.env` files to GitHub
4. Enable two-factor authentication on Render
5. Regularly backup database (Render's free plan doesn't auto-backup)

## 📊 Monitoring Your App

In Render Dashboard:

- **Logs** - Real-time application logs
- **Metrics** - CPU, Memory, Disk usage
- **Health** - Service status and uptime
- **Events** - Deployment history

## 🆘 Getting Help

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Django Docs**: [docs.djangoproject.com](https://docs.djangoproject.com)
- **GitHub Discussions**: Issues and solutions
- **Render Support**: support@render.com

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web Service created with correct settings
- [ ] Environment variables configured
- [ ] PostgreSQL database created
- [ ] Build completed without errors
- [ ] Application accessible at Render URL
- [ ] Database migrations completed
- [ ] Admin user created
- [ ] Sample data loaded
- [ ] Static files loading correctly
- [ ] Admin panel accessible

---

**Congratulations!** Your College Project Hub is now live and accessible to the world! 🎉

**App URL:** `https://your-app-name.onrender.com`  
**Admin Panel:** `https://your-app-name.onrender.com/admin/`  
**Student Directory:** `https://your-app-name.onrender.com/accounts/students/`  
**Projects:** `https://your-app-name.onrender.com/projects/`
