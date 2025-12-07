# DjangoApp
PythonDjango

Django Article Management System
A web application built with Django that allows users to manage articles with role-based access control. The system distinguishes between Administrators, Editors, and regular Users Reader.

🛠 Technology Stack
Language: Python

Framework: Django

Frontend: HTML5, CSS3, Bootstrap 5

Database: SQLite (default)

👥 User Roles & Permissions
The application implements a custom permission system:

Admin: Full access. Can create, edit, and delete articles.

Editor: Can create and edit articles, but cannot delete them.

User (Viewer): Can only browse and view article details.

Unlogged users cannot read articles - only view list.

🚀 How to Run
Follow these steps to set up the project locally:

1. Clone the repository
git clone https://github.com/Nixxias/DjangoApp.git
cd DjangoApp

2. Create and activate a virtual environment 

#Windows 
python -m venv venv
venv\Scripts\activate

Mac/Linux
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install django
4. Apply database migrations
python manage.py migrate

5. Create a Superuser (Admin)
To access admin features and manage the app:
python manage.py createsuperuser

6. Run the server
python manage.py runserver


✨ Key Features
Authentication: Secure Login, Registration, and Logout system.
CRUD Operations: Create, Read, Update, and Delete articles.
Access Control: Decorators (e.g., @role_required) ensure unauthorized users cannot access restricted views.
