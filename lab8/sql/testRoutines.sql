CALL AddBook('The Two Towers', 3, 'Fantasy', 20.99);

SELECT * FROM books;

CALL GetCustomerOrders(1);

SELECT GetOrderTotal(1) AS TotalPrice;

INSERT INTO Books (Title, AuthorID, Genre, Price) 
VALUES ('Faulty Book', 1, 'Drama', -5.99); -- should fail

SELECT * FROM Orders; -- Verify old orders are removed

DROP EVENT IF EXISTS ArchiveOldOrders;