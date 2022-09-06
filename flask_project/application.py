import sqlite3
# from os import path

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from werkzeug.exceptions import abort

app = Flask(__name__)


def get_connection():
    # BASE_DIR = path.dirname(path.abspath(__file__))
    # db_path = path.join(BASE_DIR, "books_db.sqlite")
    conn = sqlite3.connect('books_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/books/list')
def list_books():
    conn = get_connection()
    books = conn.execute('SELECT * FROM books;').fetchall()
    conn.close()

    return render_template('books/list.html', books=books)


@app.route('/books/detail/<int:book_id>')
def detail_book(book_id):
    conn = get_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book is None:
        abort(404)

    return render_template('books/detail.html', book=book)


@app.route('/books/create', methods=('GET', 'POST'))
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        if title and author:
            conn = get_connection()
            conn.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
            conn.commit()
            conn.close()
            return redirect(url_for('list_books'))
    return render_template('books/create.html')


@app.route('/books/update/<int:book_id>', methods=('GET', 'POST'))
def edit_book(book_id):
    conn = get_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        if title and author:
            conn = get_connection()
            conn.execute('UPDATE books SET title = ?, author = ? WHERE id = ?', (title, author, book_id))
            conn.commit()
            conn.close()
            return redirect(url_for('list_books'))

    return render_template('books/edit.html', book=book)


@app.route('/books/delete/<int:book_id>', methods=('GET', 'POST'))
def delete_book(book_id):
    conn = get_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()

    if request.method == 'POST':
        conn = get_connection()
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('list_books'))

    return render_template('books/delete.html', book=book)


app.run(debug=True, port=5050)
