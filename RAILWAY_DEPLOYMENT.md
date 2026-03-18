# Deploying College Project Hub to Railway

Railway is a modern deployment platform that makes it easy to go from local development to production. Here's the complete step-by-step guide.

## 📋 Prerequisites

✅ Code pushed to GitHub  
✅ settings.py configured for Railway (ALLOWED_HOSTS support)  
✅ .env file created locally (not committed)  

## 🚀 Step-by-Step Deployment

### Step 1: Sign Up on Railway

1. Go to [railway.app](https://railway.app)
2. Click **Create Account**
3. Sign up with **GitHub** (easiest option)
4. Authorize Railway to access your GitHub account

### Step 2: Create a New Project

1. In Railway dashboard, click **New Project**
2. Select **Deploy from GitHub repo**
3. Find and select `college-project-hub` repository
4. Click **Deploy**

Railway will:
- Auto-detect Python project
- Install dependencies from `requirements.txt`
- Run build command
- Start the application

### Step 3: Add PostgreSQL Database

1. In your Railway project, click **+ Add Service**
2. Select **PostgreSQL** from the database options
3. Click **Deploy**

Railway will:
- Create PostgreSQL database
- Auto-generate DATABASE_URL
- Link it to your web service

### Step 4: Configure Environment Variables

1. Click on your **web service** (college-project-hub)
2. Go to **Variables** tab
3. Add these variables:

| Variable Name | Value |
|-----------|--------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate a strong key (see below) |
| `ALLOWED_HOSTS` | Your Railway domain (will auto-populate) |

**Generate a strong SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then copy-paste the output into Railway's `SECRET_KEY` variable.

### Step 5: Get Your Railway Domain

1. In your web service, go to **Settings** tab
2. Look for **Public URL** or **Domain**
3. You'll see something like: `web-production-93ba0.up.railway.app`
4. Copy this domain and update `ALLOWED_HOSTS` variable:
   ```
   ALLOWED_HOSTS = web-production-93ba0.up.railway.app,localhost,127.0.0.1
   ```

### Step 6: Deploy

Railway auto-deploys when you add variables. Watch the **Deployments** tab:
- 🟡 **Building** - Installing dependencies, running migrations
- 🟢 **Success** - App is live!
- 🔴 **Failed** - Check logs for errors

### Step 7: Run Initial Database Setup

Once deployment is successful:

1. Click on your **web service**
2. Go to **Shell** tab at the top
3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```
   - Username: `admin` (or your choice)
   - Email: your_email@example.com
   - Password: Create a strong password

5. (Optional) Seed example data:
   ```bash
   python manage.py setup_initial_data
   ```

6. Exit shell (type `exit`)

### Step 8: Test Your Live App

1. Go back to your web service
2. Click the **Public URL** link
3. Your app should be live! 🎉

### Step 9: Access Admin Panel

Visit: `https://your-domain.railway.app/admin/`
- Login with the admin credentials you created

---

## 🔧 Railway Configuration Details

### What Railway Automatically Does

✅ Reads `requirements.txt`  
✅ Installs Python 3.11+ (Django compatible)  
✅ Runs `python manage.py migrate` (if configured)  
✅ Serves static files via WhiteNoise  
✅ Provides PostgreSQL database  
✅ Handles SSL/HTTPS automatically  
✅ Auto-redeploys on git push  

### Build Command (In Railway)

Railway uses this default build command:
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
```

If migrations don't run automatically, go to **Settings** → **Start Command** and add:
```bash
python manage.py migrate && gunicorn college_project_hub.wsgi:application
```

---

## 🚨 Common Errors & Fixes

### Error: "DisallowedHost: Invalid HTTP_HOST header"
✅ **Fixed** - We added Railway domain support in settings.py

**If still happening:**
1. Go to web service → **Variables**
2. Verify `ALLOWED_HOSTS` includes your Railway domain
3. Redeploy by going to **Deployments** → **Redeploy latest**

### Error: "ModuleNotFoundError: No module named 'django'"
**Fix:**
```bash
pip install -r requirements.txt
```
(Usually automatic, but check requirements.txt is in root directory)

### Error: "Database connection error"
**Fix:**
1. Check PostgreSQL service is running (should say "Success")
2. Wait 1-2 minutes for database to initialize
3. Verify `DATABASE_URL` is visible in Variables
4. Restart web service: **Settings** → **Restart**

### Error: 502 Bad Gateway / Service Unavailable
**Troubleshoot:**
1. Check **Logs** tab for error messages
2. Look for migration errors or missing dependencies
3. Verify `gunicorn` is in requirements.txt ✅

### Admin panel shows 404
**Fix:**
1. Run migrations in Shell: `python manage.py migrate`
2. Restart service
3. Try again

---

## 📊 Monitoring Your App

### Logs
Click **Logs** to see:
- Request logs
- Error messages
- Migration failures
- Performance issues

### Metrics
Click **Metrics** to view:
- CPU usage
- Memory usage
- Network I/O
- Response times

### Deployments
Click **Deployments** to see:
- Deployment history
- Build status
- Deployment times
- Rollback options

---

## 🔄 How Railway Deployment Works

1. **You push to GitHub**
   ```bash
   git add .
   git commit -m "Update features"
   git push origin main
   ```

2. **Railway detects changes**
   - Webhook triggered automatically
   - Pulls latest code from GitHub

3. **Build process starts**
   - Creates new deployment
   - Installs dependencies
   - Runs collectstatic
   - Runs migrations

4. **App goes live**
   - Old deployment stays until new one succeeds
   - Automatic rollback if new deployment fails
   - Zero-downtime deployments

---

## 🆘 Need Help During Deployment?

**Check these first:**

1. **Logs** - Click "Logs" to see detailed error messages
2. **Variables** - Ensure all required env vars are set
3. **Database** - Check PostgreSQL service is running
4. **Git** - Latest code pushed to `main` branch

**Common Issues:**
- Missing environment variables → Add in Variables tab
- Database not initialized → Run `python manage.py migrate` in Shell
- Static files not loading → Run `python manage.py collectstatic --noinput` in Shell
- Gunicorn not starting → Check requirements.txt has `gunicorn`

---

## ✅ Deployment Checklist

- [ ] GitHub account with code pushed
- [ ] Railway account created
- [ ] Project created and deployed from GitHub
- [ ] PostgreSQL service added and running
- [ ] Environment variables set:
  - [ ] DEBUG = False
  - [ ] SECRET_KEY = [strong key]
  - [ ] ALLOWED_HOSTS = [your Railway domain]
- [ ] Migrations run in Shell
- [ ] Admin user created
- [ ] Public URL accessible
- [ ] Admin panel working at /admin/
- [ ] Sample data loaded (optional)
- [ ] Static files loading correctly
- [ ] Database queries working

---

## 🚀 Your Live App

**Once deployed, you have:**
- 🌐 Live domain: `https://web-production-XXXX.up.railway.app`
- 🛡️ Automatic HTTPS/SSL
- 🗄️ PostgreSQL database
- 📊 Real-time monitoring
- 🔄 Auto-deploy on git push
- 💾 Automatic backups (paid tier)

**Next steps:**
- Add custom domain (optional)
- Monitor app performance
- Keep dependencies updated
- Regular database backups
- Consider upgrading plan for production

---

## 📱 Custom Domain (Optional)

To use your own domain (e.g., college-hub.com):

1. In Railway, go to web service **Settings**
2. Scroll to **Custom Domains**
3. Click **Add Custom Domain**
4. Enter your domain: `www.yourdomain.com`
5. Railway shows you DNS configuration
6. Update DNS records with your domain provider (Namecheap, GoDaddy, etc.)
7. Wait 24-48 hours for DNS to propagate

---

## 💰 Railway Pricing

- **Free tier**: $5 credit/month (great for testing)
- **Pay as you go**: $0.013/hour per 512MB RAM + storage costs
- **Starter**: $5/month for guaranteed 512MB RAM

Most hobby projects fit in the free tier. Monitor your usage to avoid surprises.

---

## 🎉 Congratulations!

Your College Project Hub is now live and accessible to the world!

**Your app is accessible at:**
- 🌐 **Main site**: `https://your-railway-domain.railway.app`
- 📊 **Admin panel**: `https://your-railway-domain.railway.app/admin/`
- 👥 **Students**: `https://your-railway-domain.railway.app/accounts/students/`
- 📂 **Projects**: `https://your-railway-domain.railway.app/projects/`

Share it with your college! 🎓
