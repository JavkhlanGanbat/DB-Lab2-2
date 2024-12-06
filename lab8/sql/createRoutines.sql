-- Procedures
DELIMITER //
CREATE PROCEDURE AddBook(
    IN p_Title VARCHAR(255),
    IN p_AuthorID INT,
    IN p_Genre VARCHAR(100),
    IN p_Price DECIMAL(10, 2)
)
BEGIN
    INSERT INTO Books (Title, AuthorID, Genre, Price) 
    VALUES (p_Title, p_AuthorID, p_Genre, p_Price);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetCustomerOrders(IN p_CustomerID INT)
BEGIN
    SELECT o.OrderID, o.OrderDate, b.Title, od.Quantity, o.CustomerID 
    FROM Orders o
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    JOIN Books b ON od.BookID = b.BookID
    WHERE o.CustomerID = p_CustomerID;
END //
DELIMITER ;

-- Functions
DELIMITER //
CREATE FUNCTION GetOrderTotal(p_OrderID INT)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10, 2);
    SELECT SUM(b.Price * od.Quantity)
    INTO total
    FROM OrderDetails od
    JOIN Books b ON od.BookID = b.BookID
    WHERE od.OrderID = p_OrderID;
    RETURN total;
END //
DELIMITER ;

-- Triggers
DELIMITER //
CREATE TRIGGER PreventNegativePrice
BEFORE INSERT ON Books
FOR EACH ROW
BEGIN
    IF NEW.Price < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Price cannot be negative.';
    END IF;
END //
DELIMITER ;

-- Events
DELIMITER //
CREATE EVENT ArchiveOldOrders
ON SCHEDULE EVERY 1 MINUTE
DO
BEGIN
    DELETE FROM Orders
    WHERE OrderDate < CURDATE() - INTERVAL 1 YEAR;
END //
DELIMITER ;


-- Show all sub functions
delimiter //
create procedure showSubFunctions()
begin
select specific_name, routine_type from information_schema.routines where routine_schema = 'bookstore'
union
SELECT TRIGGER_NAME, "TRIGGER" FROM INFORMATION_SCHEMA.TRIGGERS WHERE TRIGGER_SCHEMA = 'bookstore'
union
SELECT EVENT_NAME, "EVENT" FROM INFORMATION_SCHEMA.EVENTS WHERE EVENT_SCHEMA = 'bookstore';
end //
delimiter ;