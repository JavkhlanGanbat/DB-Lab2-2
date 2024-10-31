import mysql.connector

# Establish database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="labdatabase"
)

cursor = conn.cursor()

# Define the queries and corresponding table names
queries = {
    "Customers": "SELECT COUNT(*) FROM Customer;",
    "Orders": "SELECT COUNT(*) FROM OrderInfo;",
    "Products": "SELECT COUNT(*) FROM Product;",
    "Categories": "SELECT COUNT(*) FROM Category;",
    "Payments": "SELECT COUNT(*) FROM Payment;"
}

# Execute each query and print the result with the table name
for table_name, query in queries.items():
    cursor.execute(query)
    row_count = cursor.fetchone()[0]  # Fetch the first column of the result
    print(f"{table_name}: {row_count}")

# Close the cursor and connection
cursor.close()
