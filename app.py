"""
Book Alchemy - Flask App Initialization
This script initializes the Flask application and configures the SQLite database using SQLAlchemy.
"""

from flask import Flask  # Core Flask package for web framework
from flask_sqlalchemy import SQLAlchemy  # Extension to integrate SQLAlchemy with Flask

# Importing db and models (to be defined in the next step)
from data_models import db, Author, Book

# Create an instance of the Flask application
app = Flask(__name__)

# Configure the SQLite database location using a URI string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'

# Disable tracking modifications to save memory (optional but recommended)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension with the Flask app
db.init_app(app)
