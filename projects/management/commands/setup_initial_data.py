from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from projects.models import Category, Technology, Project

User = get_user_model()

class Command(BaseCommand):
    help = 'Sets up initial categories, technologies, users, and sample projects'

    def handle(self, *args, **kwargs):
        # Categories
        categories = [
            {'name': 'Machine Learning', 'slug': 'machine-learning', 'icon': 'bi-robot'},
            {'name': 'Web Development', 'slug': 'web-development', 'icon': 'bi-globe'},
            {'name': 'Mobile App', 'slug': 'mobile-app', 'icon': 'bi-phone'},
            {'name': 'Data Science', 'slug': 'data-science', 'icon': 'bi-graph-up'},
            {'name': 'IoT', 'slug': 'iot', 'icon': 'bi-cpu'},
            {'name': 'Cybersecurity', 'slug': 'cybersecurity', 'icon': 'bi-shield-lock'},
            {'name': 'Cloud Computing', 'slug': 'cloud-computing', 'icon': 'bi-cloud'},
            {'name': 'Blockchain', 'slug': 'blockchain', 'icon': 'bi-box'},
        ]
        for cat in categories:
            Category.objects.get_or_create(
                slug=cat['slug'],
                defaults={'name': cat['name'], 'icon': cat['icon']}
            )

        # Technologies
        technologies = [
            {'name': 'Python', 'slug': 'python', 'color': '#3776ab'},
            {'name': 'Django', 'slug': 'django', 'color': '#092e20'},
            {'name': 'JavaScript', 'slug': 'javascript', 'color': '#f7df1e'},
            {'name': 'React', 'slug': 'react', 'color': '#61dafb'},
            {'name': 'TensorFlow', 'slug': 'tensorflow', 'color': '#ff6f00'},
            {'name': 'PyTorch', 'slug': 'pytorch', 'color': '#ee4c2c'},
            {'name': 'Scikit-learn', 'slug': 'scikit-learn', 'color': '#f7931e'},
            {'name': 'Pandas', 'slug': 'pandas', 'color': '#150458'},
            {'name': 'NumPy', 'slug': 'numpy', 'color': '#013243'},
            {'name': 'HTML/CSS', 'slug': 'html-css', 'color': '#e34f26'},
            {'name': 'Node.js', 'slug': 'nodejs', 'color': '#339933'},
            {'name': 'MongoDB', 'slug': 'mongodb', 'color': '#47a248'},
            {'name': 'PostgreSQL', 'slug': 'postgresql', 'color': '#336791'},
            {'name': 'Docker', 'slug': 'docker', 'color': '#2496ed'},
            {'name': 'AWS', 'slug': 'aws', 'color': '#ff9900'},
            {'name': 'Flutter', 'slug': 'flutter', 'color': '#02569b'},
            {'name': 'OpenCV', 'slug': 'opencv', 'color': '#5c3ee8'},
            {'name': 'FastAPI', 'slug': 'fastapi', 'color': '#009688'},
        ]
        for tech in technologies:
            Technology.objects.get_or_create(
                slug=tech['slug'],
                defaults={'name': tech['name'], 'color': tech['color']}
            )

        # Create default admin and sample student user
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@projecthub.test',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_superuser': True,
                'is_staff': True,
            }
        )
        if not admin_user.pk:
            admin_user.set_password('admin123')
            admin_user.save()
        else:
            admin_user.set_password('admin123')
            admin_user.save()

        student_user, _ = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student1@projecthub.test',
                'first_name': 'Amy',
                'last_name': 'Shah',
                'role': 'student',
                'department': 'Computer Science',
                'year': 3,
                'is_staff': False,
            }
        )
        student_user.set_password('student123')
        student_user.save()

        # Create sample projects only if none exist
        if not Project.objects.exists():
            ml_cat = Category.objects.filter(slug='machine-learning').first()
            web_cat = Category.objects.filter(slug='web-development').first()
            ds_cat = Category.objects.filter(slug='data-science').first()
            python = Technology.objects.filter(slug='python').first()
            django = Technology.objects.filter(slug='django').first()
            js = Technology.objects.filter(slug='javascript').first()
            aws = Technology.objects.filter(slug='aws').first()

            p1 = Project.objects.create(
                title='Smart Attendance with Face Recognition',
                description='Web app for attendance using face detection and recognition.',
                detailed_description='A Django-based platform for automated attendance with login, admin dashboard, and detailed reports.',
                author=student_user,
                category=ml_cat,
                status='featured',
                github_link='https://github.com/example/face-attendance',
                live_demo_link='https://example.com/attendance',
            )
            p1.technologies.set([python, django, js])

            p2 = Project.objects.create(
                title='Campus Event Insights Dashboard',
                description='Data visualization dashboard for student event analytics.',
                detailed_description='Interactive charts for event attendance, trends, and feedback with export options.',
                author=student_user,
                category=ds_cat,
                status='approved',
                github_link='https://github.com/example/event-insights',
                live_demo_link='https://example.com/event-dashboard',
            )
            p2.technologies.set([python, aws])

            p3 = Project.objects.create(
                title='Group Study Collaboration Platform',
                description='A modern web portal for forming study groups and sharing resources.',
                detailed_description='Students can create groups, share notes, assign tasks, and chat in real time.',
                author=student_user,
                category=web_cat,
                status='approved',
                github_link='https://github.com/example/study-collab',
                live_demo_link='https://example.com/study-collab',
            )
            p3.technologies.set([python, django, js])

        self.stdout.write(self.style.SUCCESS('Initial data and synthetic sample projects created successfully!'))
