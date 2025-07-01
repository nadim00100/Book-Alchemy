# app.py

"""
This module contains the Flask application routes for the digital library.
It handles displaying books, adding authors and books, searching, sorting,
and deleting books.
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import date
import datetime  # For current_year in templates


# Create an instance of the Flask application
app = Flask(__name__)
# Needed for flash messages
app.config['SECRET_KEY'] = '1234567890'

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'library.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the Flask-SQLAlchemy extension with the Flask app
db.init_app(app)


@app.route('/')
def home():
    """
    Renders the home page, displaying a list of books.
    Supports sorting and keyword search.

    Queries the Book table based on sort criteria and search query.
    Generates dynamic cover URLs for each book using ISBN.

    :param sort (str, optional): The column to sort by.
                                 Defaults to 'title'.
                                 Accepted values: 'title', 'author', 'year'.
    :param search_query (str, optional): A keyword to search for in book
                                         titles or ISBNs.
    :return: Rendered home.html template with books data, search query,
             and current year.
    """
    sort_by = request.args.get('sort', 'title')
    search_query = request.args.get('search_query', '').strip()

    books_query = Book.query

    if search_query:
        # Case-insensitive search for title or ISBN
        search_pattern = f"%{search_query}%"
        books_query = books_query.filter(
            (Book.title.ilike(search_pattern)) | (Book.isbn.ilike(search_pattern))
        )

    if sort_by == 'title':
        books_query = books_query.order_by(Book.title)
    elif sort_by == 'author':
        books_query = books_query.join(Author).order_by(Author.name,
                                                         Book.title)
    elif sort_by == 'year':
        books_query = books_query.order_by(Book.publication_year.desc(),
                                           Book.title)
    else:
        books_query = books_query.order_by(Book.title)

    books = books_query.all()

    # Add cover URLs to each book object (dynamic generation)
    for book in books:
        book.cover_url = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-M.jpg"

    return render_template('home.html',
                           books=books,
                           search_query=search_query,
                           current_year=datetime.datetime.now().year)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handles adding new authors to the database.

    - On GET request: Renders the add_author.html form.
    - On POST request: Processes the form data, validates input,
      creates a new Author record, and saves it to the database.
      Flashes success or error messages and redirects to the same page.

    :return: Rendered add_author.html template or a redirect.
    """
    if request.method == 'POST':
        author_name = request.form['name'].strip()
        birth_date_str = request.form.get('birth_date')
        date_of_death_str = request.form.get('date_of_death')

        if not author_name:
            flash('Author name cannot be empty!', 'error')
            return redirect(url_for('add_author'))

        existing_author = Author.query.filter_by(name=author_name).first()
        if existing_author:
            flash(f'Author "{author_name}" already exists!', 'error')
            return redirect(url_for('add_author'))

        try:
            birth_date = date.fromisoformat(birth_date_str) \
                if birth_date_str else None
            date_of_death = date.fromisoformat(date_of_death_str) \
                if date_of_death_str else None

            new_author = Author(name=author_name,
                                birth_date=birth_date,
                                date_of_death=date_of_death)
            db.session.add(new_author)
            db.session.commit()
            flash(f'Author "{author_name}" added successfully!', 'success')
            return redirect(url_for('add_author'))
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            db.session.rollback()
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding author: {e}', 'error')
            # app.logger.error(f"Error adding author: {e}")
            return redirect(url_for('add_author'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handles adding new books to the database.

    - On GET request: Renders the add_book.html form, populating
      the author dropdown with existing authors.
    - On POST request: Processes the form data, validates input,
      creates a new Book record, and saves it to the database.
      Flashes success or error messages and redirects to the same page.

    :return: Rendered add_book.html template or a redirect.
    """
    authors = Author.query.order_by(Author.name).all()

    if request.method == 'POST':
        title = request.form['title'].strip()
        isbn = request.form['isbn'].strip()
        publication_year_str = request.form.get('publication_year')
        author_id = request.form['author_id']

        if not title or not isbn or not author_id:
            flash('Title, ISBN, and Author are required!', 'error')
            return redirect(url_for('add_book'))

        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            flash(f'Book with ISBN "{isbn}" already exists!', 'error')
            return redirect(url_for('add_book'))

        try:
            publication_year = int(publication_year_str) \
                if publication_year_str else None
            new_book = Book(
                title=title,
                isbn=isbn,
                publication_year=publication_year,
                author_id=author_id
            )
            db.session.add(new_book)
            db.session.commit()
            flash(f'Book "{title}" added successfully!', 'success')
            return redirect(url_for('add_book'))
        except ValueError:
            flash('Publication year must be a valid number.', 'error')
            db.session.rollback()
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding book: {e}', 'error')
            # app.logger.error(f"Error adding book: {e}")
        return redirect(url_for('add_book'))

    return render_template('add_book.html',
                           authors=authors,
                           current_year=datetime.datetime.now().year)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Deletes a specific book from the database.
    If the deleted book's author has no other books, the author is also deleted.

    Handles POST requests from the delete button on the home page.

    :param book_id (int): The ID of the book to be deleted.
    :return: Redirects to the home page with a success or error message.
    """
    book_to_delete = Book.query.get_or_404(book_id)
    author_id_of_book = book_to_delete.author_id
    book_title = book_to_delete.title

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        flash(f'Book "{book_title}" deleted successfully!', 'success')

        # Check if the author has any other books after deletion
        remaining_books_by_author = \
            Book.query.filter_by(author_id=author_id_of_book).count()

        if remaining_books_by_author == 0:
            author_to_delete = Author.query.get(author_id_of_book)
            if author_to_delete:
                author_name = author_to_delete.name
                db.session.delete(author_to_delete)
                db.session.commit()
                flash(f'Author "{author_name}" also deleted as they have '
                      'no remaining books.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book "{book_title}": {e}', 'error')
        # app.logger.error(f"Error deleting book: {e}")

    return redirect(url_for('home'))


if __name__ == '__main__':
    # This ensures the Flask app context is available for db operations
    # when run directly with `python app.py`
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
        #print("Database tables created (if they didn't exist).")

    # You can uncomment the line below to run the development server
    app.run(port=5001, debug=True)