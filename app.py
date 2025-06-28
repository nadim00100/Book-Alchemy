"""
Book Alchemy - Flask App Initialization and Routes
"""
import os

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
from flask_sqlalchemy import SQLAlchemy

from data_models import db, Author, Book

app = Flask(__name__)
app.secret_key = 'supersecret123'
# Use absolute path for the SQLite database URI
basedir = os.path.abspath(os.path.dirname(__file__))  # <-- get project root directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data/library.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():
    """
    Display all books, optionally filtered by a search keyword and sorted.
    """
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by')

    query = Book.query.join(Author)

    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Book.title.ilike(search_pattern),
                Author.name.ilike(search_pattern)
            )
        )

    if sort_by == 'title':
        query = query.order_by(Book.title.asc())
    elif sort_by == 'author':
        query = query.order_by(Author.name.asc())

    books = query.all()

    return render_template('home.html', books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Add a new author via form submission.
    """
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birthdate']
        date_of_death = request.form.get('date_of_death')

        author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death if date_of_death else None
        )
        db.session.add(author)
        db.session.commit()
        flash(f"Author '{name}' added successfully.", "success")

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Add a new book via form submission.
    """
    authors = Author.query.order_by(Author.name).all()

    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id
        )
        db.session.add(book)
        db.session.commit()
        flash(f"Book '{title}' added successfully.", "success")

    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Delete a book by its ID.
    Also deletes the author if they have no other books left.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()

    remaining_books = Book.query.filter_by(author_id=author.id).count()
    if remaining_books == 0:
        db.session.delete(author)
        db.session.commit()

    flash(f"Deleted book '{book.title}'.", "success")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
