I installed xampp for mysql 

just go to phpmyadmin and create database with name "check"

pip install flask mysql-connector-python for import mysql.connector

for 
Optimization Challenge
Write an SQL query to fetch the top 5 books with the highest average rating, with more than
10 reviews.
Explain how your query is optimized for performance and how it might perform as the
number of reviews grows.
Hidden problem: The query does not use indexing efficiently, and candidates should suggest
the necessary indexes.
Cost/Complexity Consideration (Estimated Time: 30 minutes):


SELECT b.book_id, b.title, AVG(r.rating) AS average_rating
FROM books b
JOIN reviews r ON b.book_id = r.book_id
GROUP BY b.book_id, b.title
HAVING COUNT(r.review_id) > 10
ORDER BY AVG(r.rating) DESC
LIMIT 5;


