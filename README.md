# College Project Hub

A modern, professional platform for students to showcase, discover, and collaborate on academic projects. Built with Django and Bootstrap 5 for a premium user experience.

## 🎯 Overview

College Project Hub is a centralized portal where students can upload their academic projects, explore works from peers, and connect through a collaborative community. The platform features project discovery, student directory, admin dashboard for project moderation, and a rich social interaction system.

## ✨ Key Features

### For Students
- **Project Upload & Management** - Create, edit, and showcase academic projects with rich metadata
- **Project Discovery** - Browse, search, and filter projects by category, technology, and year
- **Student Directory** - Connect with peers through a searchable student profile system
- **Social Interactions** - Like, bookmark, and comment on projects
- **Profile Management** - Customize your profile with bio, links, and profile picture
- **Personal Dashboard** - Track your projects, bookmarks, and engagement metrics

### For Faculty & Admins
- **Project Moderation** - Approve, reject, or feature student projects
- **Admin Dashboard** - View platform analytics and project statistics
- **Category & Technology Management** - Organize projects across 8+ categories and 18+ technologies

## 🛠️ Tech Stack

### Backend
- **Django 6.0** - High-level Python web framework
- **Python 3.13** - Modern Python runtime
- **SQLite** - Default database (easily upgradeable to PostgreSQL)
- **Django Forms** - Form handling and validation

### Frontend
- **Bootstrap 5** - Responsive CSS framework
- **Plus Jakarta Sans** - Premium typography
- **Bootstrap Icons** - Comprehensive icon library
- **Custom CSS** - Professional gradient and glass-morphism effects

### Storage & CDN
- **Cloudinary** - Image storage and optimization
- **Django Crispy Forms** - Enhanced form rendering

## 📦 Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone or navigate to project**
   ```bash
   cd "c:\Users\Lesa Shan\Documents\Projectss\Django project\college_project_hub"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   - Create a `.env` file in the project root (if using environment variables)
   - Update `college_project_hub/settings.py` with your configuration

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Load initial data**
   ```bash
   python manage.py setup_initial_data
   ```
   This seeds the database with:
   - 8 project categories
   - 18+ technologies
   - Sample student user (username: `student1`, password: `student123`)
   - Admin user (username: `admin`, password: `admin123`)
   - 3 sample projects for demonstration

7. **Start development server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser

## 🔐 Default Credentials

After running `setup_initial_data`:

| Role | Username | Password |
|------|----------|----------|
| Student | `student1` | `student123` |
| Admin | `admin` | `admin123` |

⚠️ **Security Notice**: Change all default passwords in production!

## 📁 Project Structure

```
college_project_hub/
├── accounts/                 # User management app
│   ├── models.py            # Custom User model with roles
│   ├── views.py             # Auth, profile, student list views
│   ├── urls.py              # Account routing
│   ├── forms.py             # User registration & profile forms
│   └── migrations/          # Database migrations
├── projects/                # Project management app
│   ├── models.py            # Project, Category, Technology models
│   ├── views.py             # Project CRUD, filtering, admin actions
│   ├── urls.py              # Project routing
│   ├── forms.py             # Project form
│   ├── management/          # Custom management commands
│   │   └── commands/
│   │       └── setup_initial_data.py
│   └── migrations/          # Database migrations
├── college_project_hub/     # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Root URL router
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── templates/               # HTML templates
│   ├── base.html            # Base template with navbar & footer
│   ├── home.html            # Homepage
│   ├── accounts/            # Account templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   ├── profile_edit.html
│   │   └── student_list.html
│   └── projects/            # Project templates
│       ├── project_list.html
│       ├── project_detail.html
│       ├── project_form.html
│       ├── my_projects.html
│       ├── dashboard.html
│       └── pending_projects.html
├── static/                  # Static assets
│   ├── css/
│   │   └── style.css        # Custom premium styling
│   └── js/
│       └── main.js          # Client-side interactivity
├── manage.py                # Django CLI entry point
├── db.sqlite3              # SQLite database (generated)
└── requirements.txt        # Python dependencies
```

## 🌐 URL Routing

### Public Routes
- `/` - Homepage with featured projects
- `/projects/` - Browse all projects (with filters & search)
- `/projects/<slug>/` - Project detail view
- `/accounts/students/` - Student directory
- `/accounts/profile/<id>/` - Student profile

### Authentication
- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/profile/edit/` - Edit own profile

### Student Routes (Authenticated)
- `/projects/create/` - Upload new project
- `/my-projects/` - Manage own projects
- `/bookmarks/` - Saved projects
- `POST /api/projects/<id>/like/` - Toggle like
- `POST /api/projects/<id>/bookmark/` - Toggle bookmark
- `POST /projects/<id>/comment/` - Add comment

### Admin/Faculty Routes (Authenticated)
- `/dashboard/` - Admin analytics dashboard
- `/pending/` - Review pending projects
- `POST /projects/<id>/approve/` - Approve project
- `POST /projects/<id>/reject/` - Reject project
- `POST /projects/<id>/feature/` - Feature project

## 🎨 Design System

### Colors
- **Primary**: `#1652f0` - Vibrant blue for CTAs and accents
- **Secondary**: `#101f3b` - Deep navy for headers
- **Accent**: `#7f5dff` - Purple for highlights
- **Success**: `#00c0a3` - Teal for positive actions
- **Background**: Professional gradient from light blue to white

### Typography
- **Font**: Plus Jakarta Sans (premium, modern)
- **Headings**: Bold, professional emphasis
- **Body**: Clean, readable sans-serif

### Components
- Rounded cards with subtle shadows
- Glass-morphism effects on navbar
- Smooth hover animations
- Responsive grid layouts
- Premium badge styling

## ⚙️ Configuration

### Database
Default SQLite database is configured in `settings.py`. To use PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'college_hub',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Email (Optional)
Configure email backend in `settings.py` for notifications:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

### Media Files
Configure Cloudinary for image storage:

```python
import cloudinary
cloudinary.config(
    cloud_name="Your cloud name",
    api_key="Your API key",
    api_secret="Your API secret"
)
```

## 📊 Database Models

### User (Extended from Django User)
- Role: student, faculty, admin
- Department, Year, Roll Number
- Bio, Profile Picture, GitHub/LinkedIn profiles

### Project
- Title, Description, Detailed Description
- Author, Collaborators
- Category, Technologies (M2M)
- Status: pending, approved, rejected, featured
- Links: GitHub, Live Demo, Video, Dataset, Documentation
- Views count, Likes, Comments, Bookmarks

### Category
- Name, Slug, Icon (Bootstrap Icon class)
- Examples: Machine Learning, Web Development, IoT, etc.

### Technology
- Name, Slug, Color code
- Examples: Python, Django, React, TensorFlow, etc.

## 🚀 Deployment

This project is pre-configured for deployment to **Render** using the `render.yaml` blueprint configuration.

### 📖 Render Quick Start

For detailed step-by-step deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

**Quick Summary:**
1. Push code to GitHub
2. Connect repo to Render
3. Set environment variables
4. Deploy automatically

**Key Features:**
- ✅ Auto-scaling web service with Gunicorn
- ✅ PostgreSQL database (auto-created)
- ✅ Environment variable configuration
- ✅ Static file handling with WhiteNoise
- ✅ Continuous deployment on git push
- ✅ HTTPS/SSL included

### Environment Variables

Required for Render (set in Dashboard):
```
DEBUG = false
ALLOWED_HOSTS = your-app-name.onrender.com
SECRET_KEY = [Render auto-generates]
DATABASE_URL = [Render auto-links from PostgreSQL]
```

Optional:
```
CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = your_api_key
CLOUDINARY_API_SECRET = your_api_secret
```

### Deployment Files Included

- **`render.yaml`** - Render deployment manifest (web service + PostgreSQL)
- **`build.sh`** - Custom build script for pip install, collectstatic, migrate
- **`.env.example`** - Environment variable template
- **`requirements.txt`** - All production dependencies pre-configured

### Production Checklist
- [ ] Create GitHub repository and push code
- [ ] Create Render account
- [ ] Connect GitHub repo to Render
- [ ] Set environment variables in Render dashboard
- [ ] Database (PostgreSQL) auto-created
- [ ] Run migrations via Render Shell
- [ ] Create admin user
- [ ] Test at your Render domain
- [ ] Set custom domain (optional)
- [ ] Configure Cloudinary (optional)

### Alternative Deployment Options
- **Heroku** - Procfile included, simple git push deployment
- **AWS** - EC2, RDS, S3 for scalable deployment
- **DigitalOcean** - Affordable VPS with one-click apps
- **PythonAnywhere** - Beginner-friendly Python hosting
- **Railway** - Similar to Render, great PostgreSQL support
- **Fly.io** - Modern containerized deployment

## 🐛 Troubleshooting

### Port Already in Use
```bash
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Mac/Linux
```

### Migration Issues
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Lock
```bash
rm db.sqlite3
python manage.py migrate
python manage.py setup_initial_data
```

## 📝 Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make changes and test**
   ```bash
   python manage.py runserver
   ```

3. **Run tests**
   ```bash
   python manage.py test
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   git push origin feature/amazing-feature
   ```

## 📚 API Examples

### Get All Projects
```bash
GET /projects/
```

### Search Projects
```bash
GET /projects/?search=machine+learning&category=ml&tech=python
```

### Like a Project
```bash
POST /api/projects/1/like/
Content-Type: application/json
```

### Add Comment
```bash
POST /projects/1/comment/
Content-Type: application/x-www-form-urlencoded

content=Great+project!
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available under the MIT License. See LICENSE file for details.

## 👥 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team
- Check documentation in `/docs` folder

## 🎓 Credits

Built as a modern solution for academic project showcase and peer learning.

**Technologies Used:**
- Django Framework
- Bootstrap 5
- Cloudinary
- Crispy Forms

---

**Last Updated**: March 18, 2026  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
"# Project_Hub" 
