# Modern University Website - Django

A comprehensive university website built with Django, featuring student registration, course management, faculty profiles, events, and more.

## Features

### 🎓 Student Management
- **Secure Registration & Login System**: JWT-based authentication with password hashing
- **Student Profiles**: Complete profile management with photo uploads
- **Course Enrollment**: Easy course registration and management
- **Academic Dashboard**: Personal dashboard showing enrolled courses and grades

### 👨‍🏫 Faculty Management
- **Faculty Profiles**: Detailed profiles with qualifications, research interests, and publications
- **Department Organization**: Faculty organized by departments with hierarchical structure
- **Course Assignment**: Faculty can be assigned to teach specific courses

### 📚 Course Management
- **Course Catalog**: Comprehensive course listings with detailed descriptions
- **Prerequisites System**: Course dependency management
- **Enrollment Limits**: Maximum student capacity per course
- **Multiple Semesters**: Support for different academic terms

### 📅 Events & Announcements
- **Event Management**: Create and manage university events with registration
- **Announcements**: Priority-based announcement system
- **Calendar Integration**: Event calendar view
- **Targeted Communications**: Announcements for specific audiences

### 🖼️ Media Gallery
- **Photo Gallery**: Upload and organize university photos
- **Video Gallery**: YouTube/Vimeo video integration
- **Featured Content**: Highlight important media

### 🔍 Advanced Search
- **Global Search**: Search across courses, faculty, and events
- **Filtered Results**: Advanced filtering options
- **Real-time Search**: Instant search suggestions

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-first Bootstrap 5 design
- **Dark Mode Toggle**: User preference-based theme switching
- **Interactive Elements**: Hover effects, animations, and micro-interactions
- **Accessibility**: WCAG compliant design

### 🛡️ Security Features
- **CSRF Protection**: Built-in Django CSRF protection
- **SQL Injection Prevention**: Django ORM protection
- **User Authentication**: Secure login/logout system
- **Permission-based Access**: Role-based access control

## Technology Stack

### Backend
- **Django 4.2.7**: Python web framework
- **SQLite**: Database (easily switchable to PostgreSQL/MySQL)
- **Pillow**: Image processing
- **Django Crispy Forms**: Enhanced form rendering

### Frontend
- **Bootstrap 5.3.2**: CSS framework
- **Bootstrap Icons**: Icon library
- **Custom CSS**: Enhanced styling and animations
- **Vanilla JavaScript**: Interactive functionality

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd university-website
   
   # Or extract the downloaded files
   ```

2. **Create Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   # Create database tables
   python manage.py makemigrations
   python manage.py migrate
   
   # Create superuser (admin account)
   python manage.py createsuperuser
   ```

5. **Load Sample Data (Optional)**
   ```bash
   # Create some sample departments and data
   python manage.py shell
   ```
   
   Then run this Python code:
   ```python
   from accounts.models import Department
   from django.contrib.auth.models import User
   
   # Create sample departments
   Department.objects.create(name="Computer Science", code="CS", description="Computer Science and Engineering")
   Department.objects.create(name="Business Administration", code="BBA", description="Business and Management")
   Department.objects.create(name="Islamic Studies", code="IS", description="Islamic Studies and Arabic")
   
   exit()
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Website**
   - Main website: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
university_website/
├── university_website/          # Main project directory
│   ├── __init__.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── main/                       # Main app (homepage, contact, etc.)
│   ├── models.py               # Contact, Gallery, University Info models
│   ├── views.py                # Main views
│   ├── urls.py                 # Main app URLs
│   ├── forms.py                # Contact form
│   └── admin.py                # Admin configuration
├── accounts/                   # User management app
│   ├── models.py               # User profiles, Faculty, Department models
│   ├── views.py                # Authentication and profile views
│   ├── urls.py                 # Account URLs
│   ├── forms.py                # Registration and profile forms
│   └── admin.py                # User admin configuration
├── courses/                    # Course management app
│   ├── models.py               # Course, Enrollment models
│   ├── views.py                # Course views
│   ├── urls.py                 # Course URLs
│   └── admin.py                # Course admin
├── events/                     # Events and announcements app
│   ├── models.py               # Event, Announcement models
│   ├── views.py                # Event views
│   ├── urls.py                 # Event URLs
│   └── admin.py                # Event admin
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── main/                   # Main app templates
│   ├── accounts/               # Account templates
│   ├── courses/                # Course templates
│   └── events/                 # Event templates
├── static/                     # Static files
│   ├── css/
│   │   └── style.css           # Custom CSS
│   └── js/
│       └── script.js           # Custom JavaScript
├── media/                      # User uploaded files
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
└── README.md                   # This file
```

## Usage Guide

### Admin Panel
1. Access admin panel at `/admin/`
2. Login with superuser credentials
3. Manage all content including:
   - Users and profiles
   - Departments and faculty
   - Courses and enrollments
   - Events and announcements
   - Gallery images and videos

### Student Registration
1. Visit `/accounts/register/`
2. Fill in required information
3. Select department and year
4. Create account and login

### Course Enrollment
1. Browse courses at `/courses/`
2. View course details
3. Click "Enroll" if logged in as student
4. View enrolled courses in profile

### Faculty Profiles
1. Admin creates faculty profiles
2. Faculty information displayed at `/accounts/faculty/`
3. Individual faculty pages show detailed information

### Events Management
1. Admin creates events at admin panel
2. Events displayed at `/events/`
3. Students can view and register for events

## Customization

### Adding New Features
1. Create new Django apps: `python manage.py startapp app_name`
2. Add to `INSTALLED_APPS` in settings.py
3. Create models, views, and templates
4. Update URL configurations

### Styling Customization
1. Edit `static/css/style.css` for custom styles
2. Modify Bootstrap variables if needed
3. Update templates for layout changes

### Database Configuration
To use PostgreSQL instead of SQLite:

1. Install psycopg2: `pip install psycopg2-binary`
2. Update `DATABASES` in settings.py:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'university_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## Security Considerations

### Production Deployment
1. **Change SECRET_KEY**: Generate new secret key
2. **Set DEBUG = False**: Disable debug mode
3. **Configure ALLOWED_HOSTS**: Add your domain
4. **Use HTTPS**: Enable SSL/TLS
5. **Database Security**: Use strong database passwords
6. **Media Files**: Configure secure file uploads
7. **Static Files**: Use CDN for static files

### Environment Variables
Create `.env` file for sensitive settings:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=your-database-url
EMAIL_HOST_PASSWORD=your-email-password
```

## Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py makemigrations --empty app_name
   python manage.py migrate --fake-initial
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Permission Errors**
   - Check file permissions
   - Ensure virtual environment is activated

4. **Database Connection Issues**
   - Verify database settings
   - Check database server status

### Getting Help
- Check Django documentation: https://docs.djangoproject.com/
- Review error logs in console
- Check Django debug page for detailed errors

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support and questions:
- Create an issue in the repository
- Contact: support@iiuc.ac.bd
- Documentation: Check Django official docs

---

**Built with ❤️ using Django and Bootstrap**