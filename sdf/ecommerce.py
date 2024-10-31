import mysql.connector
import random
import string

# Connect to the database
def connect_to_db():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='labdatabase'
    )
    return connection

# Generate random string data for faster user data generation
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Generate random users in bulk
def generate_users(cursor, n, batch_size=1000):
    users = []
    for _ in range(n):
        name = generate_random_string(10)
        email = f"{generate_random_string(5)}@example.com"
        password = generate_random_string(10)
        users.append(f"('{name}', '{email}', '{password}')")
        
        # Insert in batches
        if len(users) >= batch_size:
            cursor.execute(f"INSERT INTO Customer (Name, Email, Password) VALUES {', '.join(users)}")
            users = []
    
    # Insert any remaining users
    if users:
        cursor.execute(f"INSERT INTO Customer (Name, Email, Password) VALUES {', '.join(users)}")

# Generate random orders in bulk
def generate_orders(cursor, n, percentage_with_orders, batch_size=1000):
    cursor.execute("SELECT U_ID FROM Customer")
    users = cursor.fetchall()
    total_users = len(users)
    users_with_orders = int((percentage_with_orders / 100) * total_users)
    orders = []

    for _ in range(n):
        if users_with_orders > 0:
            user_id = random.choice(users)[0]
            amount = round(random.uniform(10.0, 1000.0), 2)
            date = f"{random.randint(2020, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            orders.append(f"('{user_id}', '{amount}', '{date}')")
            users_with_orders -= 1
            
            # Insert in batches
            if len(orders) >= batch_size:
                cursor.execute(f"INSERT INTO OrderInfo (C_ID, Amount, Date) VALUES {', '.join(orders)}")
                orders = []
    
    # Insert any remaining orders
    if orders:
        cursor.execute(f"INSERT INTO OrderInfo (C_ID, Amount, Date) VALUES {', '.join(orders)}")

# Generate random payments in bulk
def generate_payments(cursor, n, percentage_with_payments, batch_size=1000):
    cursor.execute("SELECT U_ID FROM Customer")
    users = cursor.fetchall()
    total_users = len(users)
    users_with_payments = int((percentage_with_payments / 100) * total_users)
    payments = []

    for _ in range(n):
        if users_with_payments > 0:
            user_id = random.choice(users)[0]
            payment_type = random.choice(['Credit Card', 'PayPal', 'Bank Transfer'])
            amount = round(random.uniform(10.0, 500.0), 2)
            payments.append(f"('{payment_type}', '{amount}', '{user_id}')")
            users_with_payments -= 1
            
            # Insert in batches
            if len(payments) >= batch_size:
                cursor.execute(f"INSERT INTO Payment (Type, Amount, U_ID) VALUES {', '.join(payments)}")
                payments = []
    
    # Insert any remaining payments
    if payments:
        cursor.execute(f"INSERT INTO Payment (Type, Amount, U_ID) VALUES {', '.join(payments)}")

# Generate random product categories
def generate_categories(cursor, n, batch_size=1000):
    categories = []
    for _ in range(n):
        name = generate_random_string(8)
        picture = "https://example.com/image.jpg"
        description = generate_random_string(30)
        categories.append(f"('{name}', '{picture}', '{description}')")
        
        # Insert in batches
        if len(categories) >= batch_size:
            cursor.execute(f"INSERT INTO Category (Name, Picture, Description) VALUES {', '.join(categories)}")
            categories = []
    
    # Insert any remaining categories
    if categories:
        cursor.execute(f"INSERT INTO Category (Name, Picture, Description) VALUES {', '.join(categories)}")

# Generate random products in bulk
def generate_products(cursor, n, batch_size=1000):
    cursor.execute("SELECT C_ID FROM Category")
    categories = cursor.fetchall()
    products = []

    for _ in range(n):
        category_id = random.choice(categories)[0]
        name = generate_random_string(10)
        price = round(random.uniform(5.0, 500.0), 2)
        description = generate_random_string(30)
        products.append(f"('{name}', '{price}', '{description}', '{category_id}')")
        
        # Insert in batches
        if len(products) >= batch_size:
            cursor.execute(f"INSERT INTO Product (Name, Price, Description, C_ID) VALUES {', '.join(products)}")
            products = []
    
    # Insert any remaining products
    if products:
        cursor.execute(f"INSERT INTO Product (Name, Price, Description, C_ID) VALUES {', '.join(products)}")

def main():
    connection = connect_to_db()
    cursor = connection.cursor()

    # Table choices for user
    tables = {
        1: generate_users,
        2: generate_orders,
        3: generate_payments,
        4: generate_categories,
        5: generate_products,
    }

    while True:
        print("Select a table to insert data into:")
        print("1. Customer")
        print("2. OrderInfo")
        print("3. Payment")
        print("4. Category")
        print("5. Product")
        print("7. Exit")

        choice = int(input("Enter your choice (1-7): "))

        if choice == 7:
            break

        if choice in tables:
            n = int(input("Enter the number of rows to insert: "))

            # For Orders and Payments, ask for a percentage of users who should have them
            if choice == 2:
                percentage_with_orders = float(input("Enter the percentage of users that should have orders (0-100): "))
                tables[choice](cursor, n, percentage_with_orders)
            elif choice == 3:
                percentage_with_payments = float(input("Enter the percentage of users that should have payment methods (0-100): "))
                tables[choice](cursor, n, percentage_with_payments)
            else:
                tables[choice](cursor, n)

            connection.commit()
            print(f"Inserted {n} rows into the selected table.")
        else:
            print("Invalid choice, please select a valid table.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
