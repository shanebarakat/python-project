# Flask-Commerce: A Modular E-commerce Platform

This is a comprehensive, full-stack e-commerce platform built with Python and Flask. It serves as a large-scale example application demonstrating best practices for building modular and scalable web applications. The project includes a customer-facing storefront, a powerful admin dashboard, and a complete REST API.

## Core Features

-   **Modular Architecture**: The application is organized into blueprints (`main`, `auth`, `api`), making it easy to manage and scale.
-   **Full-Featured Admin Dashboard**: A comprehensive admin interface built with Flask-Admin for managing users, products, categories, and orders.
-   **Complete Authentication System**: User registration, login/logout, and session management using Flask-Login.
-   **Product Catalog**: A complete system for managing products and categories.
-   **REST API**: A versioned REST API built with Flask-RESTx for programmatic access to resources (WIP).
-   **Database Management**: Uses Flask-SQLAlchemy for database interaction and Flask-Migrate (Alembic) for handling database schema migrations.
-   **Environment-Based Configuration**: The application uses a robust configuration system to adapt to different environments (development, testing, production).

## Project Structure

```
.
├── migrations/         # Database migration scripts
├── src/
│   └── app/
│       ├── admin.py        # Flask-Admin setup
│       ├── models.py       # SQLAlchemy database models
│       ├── config.py       # Environment-specific configuration
│       ├── __init__.py     # Application factory
│       ├── main/           # Main public blueprint (homepage, products)
│       │   ├── __init__.py
│       │   ├── views.py
│       │   └── ...
│       ├── auth/           # Authentication blueprint
│       │   ├── __init__.py
│       │   ├── views.py
│       │   └── forms.py
│       ├── api/            # REST API blueprint (WIP)
│       └── templates/      # Jinja2 templates
│           ├── base.html
│           ├── main/
│           └── auth/
├── tests/              # Application tests (WIP)
├── .env                # Environment variables (local development)
├── manage.py           # CLI for running and managing the app
└── pyproject.toml      # Project dependencies and metadata
```

## Getting Started

### Prerequisites

-   Python 3.9+
-   `pip` and `venv`

### Installation and Setup

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd flask-commerce-project
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    The application and all its dependencies are defined in `pyproject.toml`.
    ```sh
    pip install -e .
    ```

4.  **Create a `.env` file:**
    Copy the `.env.example` (or create a new `.env` file) and set your own `SECRET_KEY`.
    ```
    FLASK_APP=manage.py
    FLASK_ENV=development
    SECRET_KEY='your-super-secret-key'
    DATABASE_URL="sqlite:///dev.db"
    ```

5.  **Initialize the database:**
    This will create the database file and apply the initial schema.
    ```sh
    flask db init  # Run this only the very first time
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6.  **Seed the database with an admin user:**
    This will create an admin user so you can access the admin dashboard.
    ```sh
    flask seed_db
    ```
    Default admin credentials: `admin` / `admin@example.com` / `admin`

### Running the Application

-   **Run the development server:**
    ```sh
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.
-   **Access the Admin Dashboard:**
    Navigate to `http://127.0.0.1:5000/admin` and log in with the admin credentials.

## What's Next?

This is a foundational build. The next steps to expand this massive project would be:

-   Building out the **Shopping Cart** functionality.
-   Implementing the **Order Processing** workflow.
-   Developing the **REST API** with endpoints for all resources.
-   Writing a comprehensive **Test Suite**.
-   Adding more complex features like **product reviews**, **payment gateway integration**, and **background tasks**. 