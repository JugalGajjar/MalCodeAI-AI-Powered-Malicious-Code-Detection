-- Create schema and tables
CREATE SCHEMA library_db;

CREATE TABLE library_db.books (
    book_id INT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE library_db.members (
    member_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE library_db.loans (
    loan_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES library_db.members(member_id),
    book_id INT REFERENCES library_db.books(book_id),
    loan_date DATE DEFAULT CURRENT_DATE
);

-- Insert sample data
INSERT INTO library_db.books VALUES
(1, '1984', 'George Orwell', TRUE),
(2, 'To Kill a Mockingbird', 'Harper Lee', TRUE),
(3, 'The Great Gatsby', 'F. Scott Fitzgerald', TRUE);

INSERT INTO library_db.members VALUES
(1, 'Alice'), (2, 'Bob');

-- Borrow a book
UPDATE library_db.books SET available = FALSE WHERE book_id = 1;
INSERT INTO library_db.loans (member_id, book_id) VALUES (1, 1);

-- List all currently borrowed books
SELECT b.title, m.name, l.loan_date
FROM library_db.loans l
JOIN library_db.books b ON l.book_id = b.book_id
JOIN library_db.members m ON l.member_id = m.member_id;