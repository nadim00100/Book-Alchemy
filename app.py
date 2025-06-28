"""
Book Alchemy - Flask App Initialization
This script initializes the Flask application and configures the SQLite database using SQLAlchemy.
"""

import os
from flask import Flask  # Core Flask package for web framework
from flask_sqlalchemy import SQLAlchemy  # Extension to integrate SQLAlchemy with Flask

# Importing db and models
from data_models import db, Author, Book

# Create an instance of the Flask application
app = Flask(__name__)

# Get absolute path to the directory where app.py is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Construct absolute path to the SQLite database file
db_path = os.path.join(BASE_DIR, 'data', 'library.sqlite')

# Configure the SQLite database location using an absolute URI string
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Disable tracking modifications to save memory (optional but recommended)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension with the Flask app
db.init_app(app)
