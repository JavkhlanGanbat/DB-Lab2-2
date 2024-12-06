import mysql.connector

# Establish database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="labdatabase"
)

cursor = conn.cursor()

queries = {
    "address": "SELECT COUNT(*) FROM address;",
    "cartitem": "SELECT COUNT(*) FROM cartitem;",
    "comment": "SELECT COUNT(*) FROM comment;",
    "country": "SELECT COUNT(*) FROM country;",
    "Order": "SELECT COUNT(*) FROM `Order`;",
    "Orderitems": "SELECT COUNT(*) FROM Orderitems;",
    "Owner": "SELECT COUNT(*) FROM Owner;",
    "Paymentmethod": "SELECT COUNT(*) FROM Paymentmethod;",
    "product": "SELECT COUNT(*) FROM product;",
    "productcategory": "SELECT COUNT(*) FROM productcategory;",
    "productcopy": "SELECT COUNT(*) FROM productcopy;",
    "shoppingcart": "SELECT COUNT(*) FROM shoppingcart;",
    "user": "SELECT COUNT(*) FROM user;",
    "useraddress": "SELECT COUNT(*) FROM useraddress;",
}

for table_name, query in queries.items():
    cursor.execute(query)
    row_count = cursor.fetchone()[0]  
    print(f"{table_name}: {row_count}")

cursor.close()
