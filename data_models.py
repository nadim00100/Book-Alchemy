# data_models.py

"""
This module defines the SQLAlchemy models for the library application:
Author and Book. It also initializes the SQLAlchemy extension.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author in the digital library.

    Attributes:
        id (int): Primary key, unique identifier for the author.
        name (str): The full name of the author, must be unique.
        birth_date (date): The author's birth date (optional).
        date_of_death (date): The author's date of death (optional).
        books (relationship): A relationship to the Book model,
                              representing books written by this author.
                              Configured with 'cascade' to delete associated
                              books if the author is deleted.
    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship(
        'Book',
        backref='author',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        """
        Returns a string representation of the Author object,
        useful for debugging.
        """
        return f"<Author {self.name}>"

    def __str__(self):
        """
        Returns a user-friendly string representation of the Author object.
        """
        birth_str = self.birth_date.strftime('%Y-%m-%d') \
            if self.birth_date else 'N/A'
        death_str = self.date_of_death.strftime('%Y-%m-%d') \
            if self.date_of_death else 'N/A'
        return (f"Author: {self.name} (Born: {birth_str}, "
                f"Died: {death_str})")


class Book(db.Model):
    """
    Represents a book in the digital library.

    Attributes:
        id (int): Primary key, unique identifier for the book.
        isbn (str): International Standard Book Number, must be unique.
        title (str): The title of the book.
        publication_year (int): The year the book was published (optional).
        author_id (int): Foreign key linking to the Author table.
        author (relationship): A back-reference to the Author object.
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)
    # New: Added a rating column for Bonus #4 (uncomment if doing bonus)
    # rating = db.Column(db.Integer, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
                          nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the Book object,
        useful for debugging.
        """
        return f"<Book '{self.title}' by Author ID: {self.author_id}>"

    def __str__(self):
        """
        Returns a user-friendly string representation of the Book object.
        """
        return (f"Book: '{self.title}' (ISBN: {self.isbn}, "
                f"Year: {self.publication_year or 'N/A'})")