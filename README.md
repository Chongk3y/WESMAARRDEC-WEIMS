# WESMAARRDEC Web System

**Western Mindanao Agriculture, Aquatic and Natural Resources Research and Development Consortium (WESMAARRDEC) Web-based Equipment Information Management System**

A comprehensive Django-based web application for managing research equipment, programs, projects, commodities, and consortium operations.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Default Credentials](#default-credentials)
- [Project Structure](#project-structure)
- [Available Modules](#available-modules)
- [User Roles](#user-roles)
- [Common Commands](#common-commands)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Equipment Management (WEIMS)
- **Equipment Tracking**: Comprehensive equipment inventory management
- **Status Management**: Track equipment status (Available, In Use, Under Maintenance, Lost, etc.)
- **Bulk Operations**: Bulk archive, delete, and status/category updates
- **Return Management**: Equipment return processing with documentation
- **History Logs**: Complete audit trail of all equipment actions
- **Report Generation**: 
  - Customizable reports with column selection
  - Export to Word, Excel, and CSV formats
  - PDF report generation
  - Total equipment value calculation
- **Advanced Filtering**: Filter by status, category, location, dates, etc.
- **Archiving System**: Soft delete with restoration capabilities
- **Image Management**: Equipment photos and documentation

### Consortium Management
- **Member Organizations**: Manage consortium member institutions
- **Secretariat**: Track secretariat members and personnel
- **Programs & Projects**: Research program and project management
- **Commodities**: Agricultural commodity tracking
- **Teams**: Research team management

### Content Management
- **Blog System**: News and updates management
- **Dynamic Content**: Customizable web content
- **File Management**: Document and media handling

### User Management
- **Role-Based Access Control**: Admin, Encoder, Client, Viewer roles
- **Authentication System**: Secure login and session management
- **Permission Management**: Granular permission controls

---

## 🛠 Tech Stack

- **Backend**: Django 4.x (Python Web Framework)
- **Database**: SQLite3 (Development) / PostgreSQL (Production-ready)
- **Frontend**: 
  - HTML5, CSS3, JavaScript
  - Bootstrap 5 (UI Framework)
  - jQuery & DataTables (Interactive tables)
- **Document Generation**:
  - `python-docx` (Word documents)
  - `openpyxl` (Excel files)
  - ReportLab (PDF generation)
- **Image Processing**: Pillow (PIL)

---

## 📦 Prerequisites

Before running this project, ensure you have:

- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **Virtual Environment**: (Recommended) `venv` or `virtualenv`
- **Git**: For version control (optional)

---

## 🚀 Installation

### 1. Clone or Navigate to the Project

```bash
# Navigate to your project directory
cd /path/to/your/project
```

### 2. Activate Virtual Environment

The project includes a pre-configured virtual environment:

**On Windows:**
```bash
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install django pillow openpyxl python-docx reportlab django-filter
```

### 4. Navigate to Project Directory

```bash
cd WESMAARRDEC
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional - if needed)

```bash
python manage.py createsuperuser
```

---

## 🏃 Running the Project

### Start the Development Server

```bash
# Navigate to the project directory (where manage.py is located)
cd WESMAARRDEC

# Start the Django development server
python manage.py runserver
```

### Access the Application

Open your web browser and navigate to:

- **Main Website**: `http://localhost:8000/`
- **Equipment Management (WEIMS)**: `http://localhost:8000/weims/`
- **Admin Panel**: `http://localhost:8000/admin/`

### Stop the Server

Press `Ctrl + C` in the terminal

---

## 🔐 Default Credentials

### Admin Account

- **Username**: `admin`
- **Password**: `w32m@ARRd3c_pR0j3cT`

**Note**: For security, change the default password after first login in production environments.

---

## 📁 Project Structure

```
WESMAARRDEC/
├── auth_user/              # Custom user authentication module
├── cmsblg/                 # Blog/News content management
├── cmscore/                # Core CMS functionality
├── commodity/              # Commodity management
├── consortium/             # Consortium member management
├── equipments/             # Equipment management (WEIMS)
│   ├── templates/          # HTML templates
│   ├── static/             # CSS, JS, images
│   ├── models.py           # Database models
│   ├── views.py            # Business logic
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL routing
│   ├── helpers.py          # Helper functions
│   └── report_utils.py     # Report generation utilities
├── media/                  # User-uploaded files
│   ├── equipment_pic/      # Equipment photos
│   ├── report_templates/   # Report templates
│   └── ...
├── program/                # Research programs
├── project/                # Research projects
├── secretariat/            # Secretariat management
├── static/                 # Global static files
├── team/                   # Team management
├── templates/              # Global templates
├── WESMAARRDEC_WEB/       # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

---

## 📚 Available Modules

### WEIMS (Equipment Information Management System)

**URL**: `/weims/`

**Features**:
- Equipment list with advanced filtering
- Equipment detail view with full history
- Add/Edit/Archive equipment
- Bulk operations (archive, delete, update status/category)
- Return equipment with documentation
- Generate reports (Word, Excel, CSV, PDF)
- Equipment replacement tracking
- Equipment action logs and history

### Admin Panel

**URL**: `/admin/`

Full Django admin interface for:
- User management
- Group/Role assignments
- Equipment categories and statuses
- All database models

---

## 👥 User Roles

| Role | Permissions |
|------|-------------|
| **Superadmin** | Full system access, user management, all CRUD operations |
| **Admin** | Manage equipment, generate reports, bulk operations |
| **Encoder** | Add/edit equipment, limited delete permissions |
| **Client** | View equipment, generate reports (read-only) |
| **Viewer** | Basic view access |

---

## 🔧 Common Commands

### Database Management

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create database backup
python manage.py dumpdata > backup.json

# Load data from backup
python manage.py loaddata backup.json
```

### User Management

```bash
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword <username>

# List all users
python manage.py shell -c "from auth_user.models import User; [print(u.username) for u in User.objects.all()]"
```

### Static Files

```bash
# Collect static files (for production)
python manage.py collectstatic
```

### Development

```bash
# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Run tests
python manage.py test

# Open Django shell
python manage.py shell
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Use a different port
python manage.py runserver 8080
```

### Module Not Found Error

```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Migration Issues

```bash
# Reset migrations (CAUTION: Development only)
python manage.py migrate --run-syncdb

# Or delete db.sqlite3 and run migrations again
del db.sqlite3  # Windows
rm db.sqlite3   # Mac/Linux
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading

```bash
# Ensure DEBUG = True in settings.py for development
# Check STATIC_URL and STATICFILES_DIRS settings

# Collect static files
python manage.py collectstatic
```

### Permission Denied Errors

- Ensure you're logged in with appropriate role
- Check group assignments in admin panel
- Verify decorators on views match your user role

---

## 🤝 Contributing

### Development Workflow

1. Create a new branch for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test thoroughly

3. Commit with descriptive messages
   ```bash
   git commit -m "Add: Description of feature"
   ```

4. Push to repository
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request

### Code Standards

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write docstrings for functions and classes
- Test new features before committing

---

## 📝 Environment Configuration

### Development Settings

Located in `WESMAARRDEC_WEB/settings.py`:

- `DEBUG = True` (Development only)
- `ALLOWED_HOSTS = ['*']` (Restrict in production)
- Database: SQLite3 (default)

### Production Recommendations

- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS` with your domain
- Use PostgreSQL or MySQL database
- Set up proper `SECRET_KEY` management
- Configure static file serving (nginx/Apache)
- Enable HTTPS/SSL
- Set up proper logging
- Configure email backend for notifications

---

## 🔒 Security Notes

- Change default admin password immediately
- Keep `SECRET_KEY` confidential
- Don't commit sensitive data to version control
- Use environment variables for sensitive settings
- Regularly update dependencies
- Enable CSRF protection (enabled by default)
- Use strong passwords for all accounts

---

## 🎯 Version History

- **Current Version**: 1.0.0
- **Last Updated**: August 2025
- **Developed by**: WESMAARRDEC Development Team

---

## 🙏 Acknowledgments

- WESMAARRDEC Consortium Members
- Development Team
- Contributing Researchers
- All users and testers

---
