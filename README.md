# **Museum Backend Setup Guide**

## **Project Overview**

The Museum project is a web application that manages museum exhibits, items, visitors, and transactions. It provides functionalities such as retrieving information, adding new records, updating existing data, and generating reports on exhibit popularity and sales.

This guide will help you set up the backend environment to run the application locally.

---

## **Table of Contents**

- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Activate the Virtual Environment](#3-activate-the-virtual-environment)
  - [4. Install Dependencies](#4-install-dependencies)
- [Database Setup](#database-setup)
  - [1. Install MySQL Server](#1-install-mysql-server)
  - [2. Create a Database](#2-create-a-database)
  - [3. Configure Database Settings](#3-configure-database-settings)
- [Running Migrations](#running-migrations)
- [Running the Development Server](#running-the-development-server)
- [Testing the API](#testing-the-api)
- [Troubleshooting](#troubleshooting)
- [Installing drf-spectacular](#install-drf-spectacular)
- [Additional Resources](#additional-resources)

---

## **Prerequisites**

Before setting up the project, ensure you have the following installed on your machine:

- **Python 3.8 or higher**
- **Git**
- **MySQL Server**
- **pip** (Python package manager)
- **Virtualenv** (optional but recommended)

---

## **Project Setup**

### **1. Clone the Repository**

First, clone the project repository from GitHub:

```bash
git clone https://github.com/yourusername/museum.git
```

Replace `https://github.com/yourusername/museum.git` with the actual repository URL.

Navigate to the project directory:

```bash
cd museum
```

### **2. Create a Virtual Environment**

It's recommended to use a virtual environment to manage project dependencies.

```bash
# For macOS/Linux:
python3 -m venv env

# For Windows:
python -m venv env
```

### **3. Activate the Virtual Environment**

```bash
# For macOS/Linux:
source env/bin/activate

# For Windows:
env\Scripts\activate
```

### **4. Install Dependencies**

Upgrade `pip` and install required packages:

```bash
pip install --upgrade pip

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

If a `requirements.txt` file is not provided, you can install the necessary packages manually:

```bash
pip install django djangorestframework mysqlclient
```

**Note**: Installing `mysqlclient` may require additional steps. See the [Troubleshooting](#troubleshooting) section if you encounter issues.

---

## **Database Setup**

### **1. Install MySQL Server**

If you don't have MySQL Server installed, download and install it from the [official website](https://dev.mysql.com/downloads/mysql/).

Ensure that the MySQL server is running.

### **2. Create a Database**

Log in to the MySQL command-line client or use a GUI tool like MySQL Workbench to create a new database:

```sql
CREATE DATABASE museum_db;
```

### **3. Configure Database Settings**

Update the database configuration in `museum_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'museum_db',          # Your database name
        'USER': 'your_username',      # Your MySQL username
        'PASSWORD': 'your_password',  # Your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Replace `'your_username'` and `'your_password'` with your actual MySQL credentials.

---

## **Running Migrations**

Apply database migrations to create the necessary tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## **Running the Development Server**

Start the Django development server:

```bash
python manage.py runserver
```

The application will be accessible at `http://localhost:8000/`.

---

## **Testing the API**

You can test the API endpoints using a tool like Postman, or directly in your browser using Django's browsable API.

### **Accessing the API Endpoints**

- **Persons**: `http://localhost:8000/api/persons/`
- **Exhibits**: `http://localhost:8000/api/exhibits/`
- **Visits**: `http://localhost:8000/api/visits/`
- **Items**: `http://localhost:8000/api/items/`
- **Transactions**: `http://localhost:8000/api/transactions/`
- **Transaction Items**: `http://localhost:8000/api/transaction-items/`

### **Admin Interface**

Create a superuser to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

Access the admin interface at `http://localhost:8000/admin/`.

---

## **Troubleshooting**

### **Issue: Unable to Install `mysqlclient`**

**Error Message**:

```
Error: Can't find valid pkg-config name.
Specify MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS env vars manually
```

**Solution**:

1. **Install `pkg-config` and MySQL Development Headers**

   **For macOS**:

   - Install Homebrew if you haven't already:

     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```

   - Install `pkg-config` and MySQL:

     ```bash
     brew install pkg-config mysql
     ```

2. **Set Environment Variables** (if necessary)

   ```bash
   export PATH="/usr/local/opt/mysql-client/bin:$PATH"
   export MYSQLCLIENT_CFLAGS=$(mysql_config --cflags)
   export MYSQLCLIENT_LDFLAGS=$(mysql_config --libs)
   ```

3. **Install `mysqlclient` Again**

   ```bash
   pip install mysqlclient
   ```

**Alternative**:

Use `PyMySQL` instead of `mysqlclient`:

1. **Install `PyMySQL`**

   ```bash
   pip install PyMySQL
   ```

2. **Configure Django to Use `PyMySQL`**

   In `museum_project/__init__.py`, add:

   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

### **Issue: Database Connection Errors**

Ensure that:

- MySQL server is running.
- Database credentials in `settings.py` are correct.
- The database `museum_db` exists.

### **Issue: Migrations Fail**

- Delete any existing migration files in the `migrations` directories, except for `__init__.py`.
- Run `python manage.py makemigrations` and `python manage.py migrate` again.

---

## **Setting up drf-spectular**

Since Swagger UI has not been maintained, you can use drf-spectualar to achieve swagger ui look.

1. **Installing drf-spectular**
   ```bash
      pip install drf-spectacular
   ```
2. **Configuration of setting.py**
   - Add drf-_spectacular to your installed_apps:
   ```python
      INSTALLED_APPS = [
         # ALL YOUR APPS
         'drf_spectacular',
      ]
   ```

   - Add Rest Framework or modeifiy your existing one to include default_schema_class:
   ```python
      REST_FRAMEWORK = {
         # YOUR SETTINGS
         'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
      }
   ```
3. **Update your url.py**
   - add SpectacularAPIView and SpectacularSwaggerView to the top of the url file:
      ```python
         from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
      ```
   
   - add two new url to be able to access the swagger ui
      ```python
         path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
         path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
      ```
      Once add, you should be able to enter in the url to your browser and be able to see all your serializers and routes in the swagger ui.

      If it doesn't show up:
         - Check to see if you wrote the url correctly with /schema/swagger-ui/
         - Make sure you set up your setting right
         - Make sure you download the correct pip

## **Additional Resources**

- **Django Documentation**: [https://docs.djangoproject.com/en/stable/](https://docs.djangoproject.com/en/stable/)
- **Django REST Framework Documentation**: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
- **MySQL Documentation**: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
- **drf-spectacular Documentation**: [https://drf-spectacular.readthedocs.io/en/latest/readme.html#/](https://drf-spectacular.readthedocs.io/en/latest/readme.html#/)

---

**Happy Coding!**

---

**Note**: Make sure to replace placeholders like `your_username`, `your_password`, and `your.email@example.com` with the actual information relevant to your project.

---

## **Appendix**

### **Project Structure**

```
museum/
├── museum/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── museum_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── env/ (virtual environment directory)
├── manage.py
└── README.md
```

### **Dependencies**

If a `requirements.txt` file is not available, you can generate one using:

```bash
pip freeze > requirements.txt
```

Common dependencies for this project may include:

```
Django==4.x.x
djangorestframework==3.x.x
mysqlclient==2.x.x
PyMySQL==1.x.x  # If using PyMySQL
```

Ensure that the versions are compatible with your Python version.

---

## **Best Practices**

- **Use Virtual Environments**: Always use virtual environments to isolate project dependencies.
- **Keep Dependencies Updated**: Regularly update your dependencies to receive security patches and new features.
- **Secure Sensitive Information**: Do not commit sensitive information like passwords or secret keys to version control.
- **Follow Coding Standards**: Maintain consistent coding styles and standards throughout the project.
- **Version Control**: Commit changes frequently with clear and descriptive commit messages.

---

## **FAQs**

### **1. How do I reset the database?**

If you need to reset the database:

1. Drop the existing database:

   ```sql
   DROP DATABASE museum_db;
   ```

2. Create a new database:

   ```sql
   CREATE DATABASE museum_db;
   ```

3. Run migrations again:

   ```bash
   python manage.py migrate
   ```

### **2. How do I load initial data?**

If you have fixture files:

```bash
python manage.py loaddata initial_data.json
```

### **3. How do I add a new dependency?**

Install the package and update `requirements.txt`:

```bash
pip install package_name
pip freeze > requirements.txt
```

---

## **Contributing**

- **Branching Strategy**: Use feature branches and submit pull requests for code reviews.
- **Code Reviews**: All code changes should be reviewed by at least one other team member.
- **Issue Tracking**: Use GitHub Issues to track bugs and feature requests.

---