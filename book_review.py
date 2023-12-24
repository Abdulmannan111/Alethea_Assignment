# app.py

from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Replace 'your_username', 'your_password', 'your_database' with your actual MySQL credentials
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="check"
)
cursor = db.cursor()

# API endpoints
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = data['user_id']
    username = data['username']

    # Check if the user already exists
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'error': 'User already exists'})

    # Inserting a new user
    cursor.execute("INSERT INTO users (user_id, username) VALUES (%s, %s)", (user_id, username))
    db.commit()

    return jsonify({'message': 'User added successfully'})

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data['title']

    # Check if the book already exists
    cursor.execute("SELECT * FROM books WHERE title = %s", (title,))
    existing_book = cursor.fetchone()
    if existing_book:
        return jsonify({'error': 'Book already exists'})

    # Inserting a new book
    cursor.execute("INSERT INTO books (title) VALUES (%s)", (title,))
    db.commit()

    return jsonify({'message': 'Book added successfully'})

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    rating = data['rating']
    book_id = data['book_id']
    user_id = data['user_id']

    # Check if the book exists
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    if not book:
        return jsonify({'error': 'Book not found'})

    # Check if the user exists
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'})

    # Check if the user has already rated the book
    cursor.execute("SELECT * FROM reviews WHERE book_id = %s AND user_id = %s", (book_id, user_id))
    existing_review = cursor.fetchone()
    if existing_review:
        return jsonify({'error': 'User has already rated the book'})

    # Inserting a new review
    cursor.execute("INSERT INTO reviews (rating, book_id, user_id) VALUES (%s, %s, %s)", (rating, book_id, user_id))
    db.commit()

    return jsonify({'message': 'Review added successfully'})

# ...

@app.route('/books', methods=['GET'])
def get_books():
    # Fetching all books with their average ratings and user information
    cursor.execute("""
        SELECT books.id as book_id, books.title, IFNULL(AVG(reviews.rating), 0) as average_rating,
               GROUP_CONCAT(users.user_id) as user_ids, GROUP_CONCAT(users.username) as usernames
        FROM books
        LEFT JOIN reviews ON books.id = reviews.book_id
        LEFT JOIN users ON reviews.user_id = users.user_id
        GROUP BY books.id, books.title
    """)
    books = cursor.fetchall()

    result = [{
        'book_id': book[0],
        'title': book[1],
        'average_rating': float(book[2]),
        'user_ids': list(map(int, book[3].split(','))) if book[3] is not None else [],
        'usernames': book[4].split(',') if book[4] is not None else []
    } for book in books]

    return jsonify(result)

# ...


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Creating the 'users', 'books', and 'reviews' tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT UNIQUE,
            username VARCHAR(50) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rating FLOAT NOT NULL,
            book_id INT NOT NULL,
            user_id INT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    app.run(debug=True)
