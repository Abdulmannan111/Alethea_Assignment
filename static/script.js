document.addEventListener('DOMContentLoaded', function () {
    // Fetch and display books on page load
    fetchBooks();

    // Optional: Add event listeners for other actions
});

function fetchBooks() {
    fetch('/books')
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('bookList');
            bookList.innerHTML = '';

            data.forEach(book => {
                const bookItem = document.createElement('div');
                bookItem.classList.add('book-item');
                bookItem.innerHTML = `<strong>${book.title}</strong> (ID: ${book.book_id}) - 
                    Average Rating: ${book.average_rating}<br>Users: ${formatUsers(book.user_ids, book.usernames)}`;
                bookList.appendChild(bookItem);
            });
        })
        .catch(error => console.error('Error fetching books:', error));
}

function formatUsers(userIds, usernames) {
    return userIds.map((id, index) => `${usernames[index]} (ID: ${id})`).join(', ');
}

function addUser() {
    const userId = document.getElementById('userId').value;
    const username = document.getElementById('username').value;
    fetch('/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId, username: username }),
    })
        .then(response => response.json())
        .then(data => {
            console.log('User added successfully:', data);
            // Refresh the user list or perform other actions if needed
        })
        .catch(error => console.error('Error adding user:', error));
}

function addBook() {
    const bookTitle = document.getElementById('bookTitle').value;
    fetch('/books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: bookTitle }),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Book added successfully:', data);
            fetchBooks(); // Refresh the book list after adding a book
        })
        .catch(error => console.error('Error adding book:', error));
}

function addReview() {
    const bookId = document.getElementById('bookId').value;
    const rating = document.getElementById('rating').value;
    const userId = document.getElementById('userIdReview').value;

    fetch('/reviews', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rating: rating, book_id: bookId, user_id: userId }),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Review added successfully:', data);
            fetchBooks(); // Refresh the book list after adding a review
        })
        .catch(error => console.error('Error adding review:', error));
}
