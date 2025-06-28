"""
Book Alchemy - Flask App with routes to add authors, books and display the library.
"""

import os
from flask import Flask, render_template, request

from data_models import db, Author, Book

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():
    """
    Display all books, optionally filtered by a search keyword and sorted.
    """
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by')

    # Base query joining Author to Book for author filtering
    query = Book.query.join(Author)

    # If search query is provided, filter books by title or author name (case-insensitive)
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Book.title.ilike(search_pattern),
                Author.name.ilike(search_pattern)
            )
        )

    # Sorting logic
    if sort_by == 'title':
        query = query.order_by(Book.title.asc())
    elif sort_by == 'author':
        query = query.order_by(Author.name.asc())

    books = query.all()

    return render_template('home.html', books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Display a form to add authors on GET.
    On POST, add author to database and show success message.
    """
    message = None

    if request.method == 'POST':
        name = request.form.get('name')
        birth_date = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')

        # Convert string dates to date objects
        from datetime import datetime

        birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
        date_of_death_obj = None
        if date_of_death:
            date_of_death_obj = datetime.strptime(date_of_death, '%Y-%m-%d').date()

        new_author = Author(
            name=name,
            birth_date=birth_date_obj,
            date_of_death=date_of_death_obj
        )
        db.session.add(new_author)
        db.session.commit()

        message = f"Author '{name}' added successfully!"

    return render_template('add_author.html', message=message)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Display a form to add books on GET.
    On POST, add book to database and show success message.
    """
    message = None
    authors = Author.query.order_by(Author.name).all()

    if request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=int(publication_year),
            author_id=int(author_id)
        )
        db.session.add(new_book)
        db.session.commit()

        message = f"Book '{title}' added successfully!"

    return render_template('add_book.html', authors=authors, message=message)



if __name__ == '__main__':
    app.run(debug=True)
