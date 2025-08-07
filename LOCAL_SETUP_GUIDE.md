# WESMAARRDEC Local Development Setup Guide

## Fixed Issues
✅ **FIXED**: Missing comma in `INSTALLED_APPS` after `'wdamms'` that was causing `ModuleNotFoundError: No module named 'wdammsequipments'`
✅ **FIXED**: Created missing `wdamms` app (Activity Management System) to resolve `NoReverseMatch` error for `'wdamms:index'`
✅ **FIXED**: Configured database to use SQLite for local development
✅ **READY**: Django development server running successfully at http://127.0.0.1:8000/

## Prerequisites
1. **Python 3.8+** installed on your system
2. **Virtual environment** (recommended)
3. **Database** (SQLite for development or MySQL for production-like setup)

## Step-by-Step Setup

### 1. Configure Python Environment
```bash
# Navigate to project directory
cd d:\WESMAARRDEC1\WESMAARRDEC

# Activate virtual environment (if you have one)
# For Windows:
venv\Scripts\activate
# For Linux/Mac:
# source venv/bin/activate

# If you don't have a virtual environment, create one:
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# If you encounter issues with specific packages, install them individually:
pip install Django==5.0.6
pip install mysqlclient  # For MySQL support
pip install django-crispy-forms
pip install django-widget-tweaks
pip install django-filters
pip install django-simple-history
pip install django-auditlog
pip install crispy-bootstrap5
pip install Pillow  # For image handling
pip install openpyxl  # For Excel export/import
```

### 3. Database Configuration
The project is currently configured for MySQL. You have several options:

#### Option A: Use SQLite (Easiest for development)
Edit `WESMAARRDEC_WEB/settings.py` and uncomment/use the SQLite configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

#### Option B: Use MySQL (Current configuration)
1. Install MySQL/MariaDB or use XAMPP/Laragon
2. Create database: `wesmaarrdecdb`
3. Update credentials in settings.py if needed
4. Ensure MySQL service is running

### 4. Handle Missing Apps
The `wdamms` app is referenced in settings but doesn't exist. You have two options:

#### Option A: Remove the missing app
Edit `WESMAARRDEC_WEB/settings.py` and remove or comment out:
```python
# 'wdamms',  # Comment out if app doesn't exist
```

#### Option B: Create the missing app
```bash
python manage.py startapp wdamms
```

### 5. Apply Database Migrations
```bash
# Check for migration issues first
python manage.py check

# Create migrations for all apps
python manage.py makemigrations auth_user
python manage.py makemigrations cmscore
python manage.py makemigrations cmsblg
python manage.py makemigrations commodity
python manage.py makemigrations consortium
python manage.py makemigrations secretariat
python manage.py makemigrations team
python manage.py makemigrations program
python manage.py makemigrations project
python manage.py makemigrations sub
python manage.py makemigrations equipments
# python manage.py makemigrations wdamms  # Only if you created this app

# Apply all migrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Load Initial Data (if available)
```bash
# If you have fixture files
python manage.py loaddata initial_categories.json  # Example
python manage.py loaddata initial_statuses.json    # Example
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000/`

## Common Issues and Solutions

### Issue 1: `ModuleNotFoundError: No module named 'wdammsequipments'`
**Solution**: ✅ Already fixed - added missing comma in INSTALLED_APPS

### Issue 2: Migration errors
```bash
# Reset migrations if needed (CAUTION: This will lose data)
# Delete migration files (keep __init__.py)
# Then run:
python manage.py makemigrations
python manage.py migrate
```

### Issue 3: Database connection errors
- Check database credentials in settings.py
- Ensure database server is running
- Create the database if it doesn't exist

### Issue 4: Missing static files
```bash
python manage.py collectstatic
```

### Issue 5: Permission errors
- Make sure your user has write permissions to the project directory
- Check media folder permissions

## Project Structure Overview
```
WESMAARRDEC/
├── auth_user/          # Custom user authentication
├── cmsblg/            # Blog/CMS functionality
├── cmscore/           # Core CMS features
├── commodity/         # Commodity management
├── consortium/        # Consortium management
├── equipments/        # Equipment management (WEIMS)
├── secretariat/       # Secretariat functionality
├── team/              # Team management
├── program/           # Program management
├── project/           # Project management
├── sub/               # Sub-modules
├── media/             # Uploaded files
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
└── WESMAARRDEC_WEB/   # Main project settings
```

## Next Steps
1. Test the equipment management system at `/weims/`
2. Create initial categories and statuses for equipment
3. Configure user roles and permissions
4. Import/create sample equipment data
5. Test all functionality

## Important Notes
- The project uses a custom user model: `auth_user.User`
- Equipment management is the main feature (WEIMS)
- Bootstrap 5 and crispy forms are used for UI
- The system supports multiple user roles (Admin, Encoder, Client, etc.)
