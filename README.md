
# Django Inventory Management System

## Project Overview
This is a Django-based Inventory Management System that allows users to manage products and a shopping cart. It supports both general users and admin (staff) users with different levels of access.

---

## Features

###  User Features
- View all products
- Search products by name
- Filter products by category
- View product details
- Add products to cart
- Update cart quantity
- Remove items from cart

###  Admin Features
- Add new products
- Edit existing products
- Delete products

---

##  Tech Stack

- **Backend:** Python, Django  
- **Database:** SQLite (default Django DB)  
- **Frontend:** HTML (Django Templates)  
- **Other:** Django Messages Framework, Django Sessions  

---

##  Project Structure

```

inventory/
│── models.py
│── views.py
│── urls.py
│── tests.py
│── templates/
│   └── inventory/
│       ├── product\_list.html
│       ├── product\_detail.html
│       ├── add\_product.html
│       ├── edit\_product.html
│       ├── cart.html

````

---

##  Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <project-folder>
````

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # For Windows
```

### 3. Install Dependencies

```bash
pip install django
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

***

##  Application URLs

| Feature                | URL               |
| ---------------------- | ----------------- |
| Product List           | `/`               |
| Product Detail         | `/product/<id>/`  |
| Category Filter        | `/category/<id>/` |
| Add Product (Admin)    | `/add/`           |
| Edit Product (Admin)   | `/edit/<id>/`     |
| Delete Product (Admin) | `/delete/<id>/`   |
| Cart                   | `/cart/`          |



##  Running Tests

Run test cases using:

```bash
python manage.py test
```

***

## Permissions

*   Only users with `is_staff=True` can:
    *   Add products
    *   Edit products
    *   Delete products






