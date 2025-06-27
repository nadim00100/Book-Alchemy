"""
Book Alchemy - Flask App Initialization
This script initializes the Flask application
"""

from flask import Flask  # Core Flask framework to create the web application
from flask_sqlalchemy import SQLAlchemy  # Extension to handle SQLAlchemy ORM with Flask

# Create the Flask application instance
app = Flask(__name__)

