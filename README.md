# Project overview
This is a Django-based Inventory Management System developed to manage products, categories, and a session-based shopping cart. The project demonstrates clean MVC architecture, CRUD operations, and unit testing.

##  Features
- Product & Category Management
- Product Search & Filtering
- Session-Based Cart
- Admin Panel Integration
- Unit Tests for Models & Views

##  Tech Stack
- Python
- Django
- SQLite (Development)
- HTML / Django Templates

# setup instruction
- clone repository
git clone <repository-url>
cd inventory_project
- activate venv
- install dependencies
pip install -r requirements.txt
- apply database migrations
python manage.py migrate
- create superuser
python manage.py createsuperuser
- run server
python manage.py runserver
- run tests
python manage.py test inventory