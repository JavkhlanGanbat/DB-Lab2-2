CALL AddBook('The Two Towers', 3, 'Fantasy', 20.99);

SELECT * FROM Books;

CALL GetCustomerOrders(3);

SELECT GetOrderTotal(5) AS TotalPrice;

INSERT INTO Books (Title, AuthorID, Genre, Price) 
VALUES ('Faulty Book', 1, 'Drama', -5.99); -- should fail

-- Insert old order
INSERT INTO Orders(CustomerID, OrderDate)
VALUES (1, '2022-01-01');

SELECT * FROM Orders; -- Verify old orders are removed

DROP EVENT IF EXISTS ArchiveOldOrders;