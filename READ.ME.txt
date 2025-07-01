# My Digital Library (Flask App)

A simple web application built with Flask and SQLAlchemy to manage a personal digital library of books and authors.

## Features

* **View Books:** Browse a list of all books in the library.
* **Search Books:** Search for books by title or ISBN.
* **Sort Books:** Sort the book list by title, author name, or publication year.
* **Add Authors:** Add new authors with their birth and death dates.
* **Add Books:** Add new books, linking them to existing authors.
* **Delete Books:** Remove books from the library. Automatically deletes authors if they have no remaining books.
* **Dynamic Cover Images:** Fetches book covers using the Open Library Covers API based on ISBN.
* **Responsive UI:** Basic responsive design for better viewing on various devices.
* **Flash Messages:** Provides user feedback for successful operations and errors.

## Technologies Used

* **Backend:** Python (Flask, Flask-SQLAlchemy)
* **Database:** SQLite (managed by SQLAlchemy)
* **Frontend:** HTML, CSS (minimal JavaScript for confirmation dialogs)
* **External API:** Open Library Covers API for book images.

## Setup Instructions

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository (if applicable)

If you're starting from scratch, you can ignore this step. If this project were hosted on GitHub, you would clone it:
```bash
git clone https://github.com/nadim00100/Book-Alchemy.git
cd Book_Alchemy # Or whatever your project folder is called

2. Create a Python Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

Bash

cd /Users/n00100/Desktop/PythonProject/Book_Alchemy/
python3 -m venv .venv
3. Activate the Virtual Environment
macOS / Linux:

Bash

source .venv/bin/activate
Windows (Command Prompt):

Bash

.venv\Scripts\activate
Windows (PowerShell):

PowerShell

.venv\Scripts\Activate.ps1
(You may need to allow script execution with Set-ExecutionPolicy RemoteSigned -Scope CurrentUser if you encounter issues)

4. Install Dependencies
Install all required Python packages using pip:

Bash

pip install -r requirements.txt
5. Initialize the Database and Populate with Sample Data
First, ensure the data directory exists, as the database file will be stored there.

Bash

mkdir -p data # Creates 'data' directory if it doesn't exist
Then, run the database initialization script (this will create library.sqlite inside the data folder and set up the tables):

Bash

python populate_db.py
(This script also populates some sample data. If you only want to initialize tables without data, you can run python init_db.py if you created that previously, otherwise populate_db.py includes db.create_all())

6. Run the Flask Application
Bash

python app.py
You should see output similar to this in your terminal:

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) (Press CTRL+C to quit)
(Note: The port might be different if you changed it in app.py, e.g., 5001 or 8000).

7. Access the Application in Your Browser
Open your web browser and navigate to the address shown in your terminal, usually:

[suspicious link removed]

If you changed the port, use that one (e.g., http://127.0.0.1:5001/).

Usage
Use the navigation links in the header to go to "Home", "Add Author", or "Add Book".

On the Home page, use the search bar to find books by title or ISBN.

Click the "Sort by" links to reorder the book list.

Use the "Delete Book" button below each book to remove it. If an author's last book is deleted, the author will also be removed.

