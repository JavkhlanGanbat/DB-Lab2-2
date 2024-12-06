DROP DATABASE IF EXISTS bookstore;
CREATE DATABASE bookstore;
USE bookstore;

CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Bio TEXT
);

CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255),
    AuthorID INT,
    Genre VARCHAR(100),
    Price DECIMAL(10, 2),
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID) ON DELETE CASCADE
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    OrderDate DATE
);

CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    BookID INT,
    Quantity INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE
);

AlTER TABLE Books
    ADD CONSTRAINT fk_books_authors
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID)
    ON DELETE CASCADE;

AlTER TABLE Orders
    ADD CONSTRAINT fk_orders_customers
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    ON DELETE CASCADE;

ALTER TABLE OrderDetails
    ADD CONSTRAINT fk_orderdetails_books
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
    ON DELETE CASCADE;

ALTER TABLE OrderDetails
    ADD CONSTRAINT fk_orderdetails_orders
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
    ON DELETE CASCADE;