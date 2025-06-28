"""
Database initialization script for Book Alchemy.
Use this once to create the tables in the SQLite database.
"""

from app import app  # Import the Flask app with db.init_app() already called
from data_models import db

# Create the tables within the Flask app context
with app.app_context():
    db.create_all()
    print("Database tables created.")
