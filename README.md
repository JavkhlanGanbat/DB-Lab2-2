# Book Borrowing System

## About

- Tables
    - Authors
    - Books
    - Customers
    - Orders
    - OrderDetails

- Routines
  - Procedures
    - AddBook(title, authorID, genre, price)
    - GetCustomerOrders(customerID)
  - Functions
    - GetOrderTotal(orderID)
  - Triggers
    - PreventNegativePrice
  - Events
    - ArchiveOldOrders

## Instructions

- install dependencies
`cd lab8`
`npm i`

- start the server
`npm run dev`