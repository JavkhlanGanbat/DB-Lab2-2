import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import random

# Connect to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="labdatabase"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Generate random dates for testing
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Insert dummy data into each table
def insert_data(connection):
    cursor = connection.cursor()
    tables = [
        ("Country", "INSERT INTO Country (CountryID, CountryName) VALUES (%s, %s)"),
        ("ProductCategory", "INSERT INTO ProductCategory (ProductCategoryID, CategoryType) VALUES (%s, %s)"),
        ("User", "INSERT INTO User (UserID, Username, Email, Password, DateJoined, Role) VALUES (%s, %s, %s, %s, %s, %s)"),
        ("Owner", "INSERT INTO Owner (OwnerID, OwnerName, ProductID) VALUES (%s, %s, %s)"),
        ("Product", "INSERT INTO Product (ProductID, ProductName, ProductDescription, Total, Stock, ProductCategoryID, OwnerID, ListedDate, AvgRating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"),
        ("ProductCopy", "INSERT INTO ProductCopy (ProductCopyID, ProductID, Price) VALUES (%s, %s, %s)"),
        ("Address", "INSERT INTO Address (AddressID, Street, AddressLine, City, CountryID) VALUES (%s, %s, %s, %s, %s)"),
        ("UserAddress", "INSERT INTO UserAddress (UserID, AddressID) VALUES (%s, %s)"),
        ("ShoppingCart", "INSERT INTO ShoppingCart (CartID, UserID, CreationDate) VALUES (%s, %s, %s)"),
        ("CartItem", "INSERT INTO CartItem (CartItemID, CartID, DateAdded, Quantity, ProductCopyID) VALUES (%s, %s, %s, %s, %s)"),
        ("PaymentMethod", "INSERT INTO PaymentMethod (PaymentID, UserID, PaymentType, Company, CardNumber, ExpDate, IsMain) VALUES (%s, %s, %s, %s, %s, %s, %s)"),
        ("Order", "INSERT INTO `Order` (OrderID, UserID, Total, Status, PaymentID, OrderDate, AddressID) VALUES (%s, %s, %s, %s, %s, %s, %s)"),
        ("OrderItems", "INSERT INTO OrderItems (OrderItemsID, ProductCopyID, OrderID, Quantity) VALUES (%s, %s, %s, %s)"),
        ("Comment", "INSERT INTO Comment (CommentID, Comment, ProductID, UserID, PublishDate, Rating) VALUES (%s, %s, %s, %s, %s, %s)"),
    ]
def insert_data(connection):
    cursor = connection.cursor()
    tables = [
        ("Country", "INSERT INTO Country (CountryID, CountryName) VALUES (%s, %s)"),
        ("ProductCategory", "INSERT INTO ProductCategory (ProductCategoryID, CategoryType) VALUES (%s, %s)"),
        ("User", "INSERT INTO User (UserID, Username, Email, Password, DateJoined, Role) VALUES (%s, %s, %s, %s, %s, %s)"),
        ("Owner", "INSERT INTO Owner (OwnerID, OwnerName, ProductID) VALUES (%s, %s, %s)"),
        ("Product", "INSERT INTO Product (ProductID, ProductName, ProductDescription, Total, Stock, ProductCategoryID, OwnerID, ListedDate, AvgRating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"),
        ("ProductCopy", "INSERT INTO ProductCopy (ProductCopyID, ProductID, Price) VALUES (%s, %s, %s)"),
        ("Address", "INSERT INTO Address (AddressID, Street, AddressLine, City, CountryID) VALUES (%s, %s, %s, %s, %s)"),
        ("UserAddress", "INSERT INTO UserAddress (UserID, AddressID) VALUES (%s, %s)"),
        ("ShoppingCart", "INSERT INTO ShoppingCart (CartID, UserID, CreationDate) VALUES (%s, %s, %s)"),
        ("CartItem", "INSERT INTO CartItem (CartItemID, CartID, DateAdded, Quantity, ProductCopyID) VALUES (%s, %s, %s, %s, %s)"),
        ("PaymentMethod", "INSERT INTO PaymentMethod (PaymentID, UserID, PaymentType, Company, CardNumber, ExpDate, IsMain) VALUES (%s, %s, %s, %s, %s, %s, %s)"),
        ("Order", "INSERT INTO `Order` (OrderID, UserID, Total, Status, PaymentID, OrderDate, AddressID) VALUES (%s, %s, %s, %s, %s, %s, %s)"),
        ("OrderItems", "INSERT INTO OrderItems (OrderItemsID, ProductCopyID, OrderID, Quantity) VALUES (%s, %s, %s, %s)"),
        ("Comment", "INSERT INTO Comment (CommentID, Comment, ProductID, UserID, PublishDate, Rating) VALUES (%s, %s, %s, %s, %s, %s)"),
    ]

    existing_user_addresses = set()  # To track existing (UserID, AddressID) pairs

    for table, query in tables:
        num_rows = int(input(f"Enter the number of rows to insert into {table}: "))
        for i in range(num_rows):
            # Dummy data generation for each table (same as before)
            if table == "Country":
                data = (i + 1, f"Country_{i + 1}")

            elif table == "ProductCategory":
                data = (i + 1, f"Category_{i + 1}")

            elif table == "User":
                data = (i + 1, f"User_{i + 1}", f"user{i + 1}@example.com", "password123", 
                        random_date(datetime(2020, 1, 1), datetime.now()).date(), "Customer")

            elif table == "Owner":
                product_id = min(i + 1, num_rows)
                data = (i + 1, f"Owner_{i + 1}", product_id)

            elif table == "Product":
                category_id = random.randint(1, num_rows)
                owner_id = random.randint(1, num_rows)
                data = (i + 1, f"Product_{i + 1}", f"Description for Product {i + 1}", random.randint(10, 100), random.randint(1, 20), 
                        category_id, owner_id, datetime.now().date(), round(random.uniform(1, 5), 1))

            elif table == "ProductCopy":
                product_id = random.randint(1, num_rows)
                data = (i + 1, product_id, round(random.uniform(10, 100), 2))

            elif table == "Address":
                country_id = random.randint(1, num_rows)
                data = (i + 1, f"Street_{i + 1}", f"AddressLine_{i + 1}", f"City_{i + 1}", country_id)

            elif table == "UserAddress":
                user_id = random.randint(1, num_rows)
                address_id = random.randint(1, num_rows)
                # Check for uniqueness
                while (user_id, address_id) in existing_user_addresses:
                    user_id = random.randint(1, num_rows)
                    address_id = random.randint(1, num_rows)
                existing_user_addresses.add((user_id, address_id))
                data = (user_id, address_id)

            elif table == "ShoppingCart":
                user_id = random.randint(1, num_rows)
                data = (i + 1, user_id, datetime.now().date())

            elif table == "CartItem":
                cart_id = random.randint(1, num_rows)
                product_copy_id = random.randint(1, num_rows)
                data = (i + 1, cart_id, datetime.now(), random.randint(1, 5), product_copy_id)

            elif table == "PaymentMethod":
                user_id = random.randint(1, num_rows)
                data = (i + 1, user_id, "Credit Card", "Bank_" + str(i + 1), random.randint(1000000000000000, 9999999999999999), 
                        random_date(datetime(2024, 1, 1), datetime(2030, 12, 31)), random.choice([True, False]))

            elif table == "Order":
                user_id = random.randint(1, num_rows)
                payment_id = random.randint(1, num_rows)
                address_id = random.randint(1, num_rows)
                data = (i + 1, user_id, round(random.uniform(50, 500), 2), "Completed", payment_id, datetime.now().date(), address_id)

            elif table == "OrderItems":
                product_copy_id = random.randint(1, num_rows)
                order_id = random.randint(1, num_rows)
                data = (i + 1, product_copy_id, order_id, random.randint(1, 5))

            elif table == "Comment":
                product_id = random.randint(1, num_rows)
                user_id = random.randint(1, num_rows)
                data = (i + 1, f"Comment {i + 1}", product_id, user_id, random_date(datetime(2020, 1, 1), datetime.now()).date(), round(random.uniform(1, 5), 1))

            cursor.execute(query, data)
        print(f"Inserted {num_rows} rows into {table}.")

    # Commit the transaction
    connection.commit()
    print("Data inserted successfully.")


# Execute the functions
connection = create_connection()
if connection:
    insert_data(connection)
    connection.close()
    print("Data inserted and database connection closed.")
