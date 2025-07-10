import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This should be at the very top of the entrypoint file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from src.app import create_app, db
from src.app.models import User, Product, Category, Order, OrderItem
from flask.cli import FlaskGroup

# Create an application instance that we can use for the CLI
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
cli = FlaskGroup(create_app=lambda: app)

@cli.command("seed_db")
def seed_db():
    """Seeds the database with initial data."""
    print("Seeding database...")
    # Example of adding a user
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('admin')
        db.session.add(admin)
        print("Admin user created.")

    # Example of adding a category
    if not Category.query.filter_by(name='Default').first():
        default_cat = Category(name='Default', description='Default category')
        db.session.add(default_cat)
        print("Default category created.")
    
    db.session.commit()
    print("Database seeded!")

@cli.command("recreate_db")
def recreate_db():
    """Drops and recreates the database."""
    print("Dropping database...")
    db.drop_all()
    print("Creating database...")
    db.create_all()
    print("Database recreated!")

if __name__ == '__main__':
    cli() 