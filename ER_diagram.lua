+-----------+      +-------------+      +-----------+
|   Books   |      |   Reviews   |      |   Users   |
+-----------+      +-------------+      +-----------+
| book_id   |      | review_id   |      | user_id   |
| title     |----->| rating      |<-----| username  |
+-----------+      | book_id (FK)|      +-----------+
                   | user_id (FK)|
                   +-------------+
