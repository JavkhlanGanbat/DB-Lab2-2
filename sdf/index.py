import mysql.connector

# Establish database connection
def connect_to_db():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='labdatabase'
    )
    return connection

def create_indexes(cursor):
    #cursor.execute("CREATE INDEX idx_category_id ON Product(C_ID);")
    print("Product(C_ID) indexed.")

    #cursor.execute("CREATE INDEX idx_email ON Customer(Email);")
    print("Customer(Email) indexed.")

    #cursor.execute("CREATE INDEX idx_order_customer ON OrderInfo(C_ID);")
    print("OrderInfo(C_ID) indexed.")
    
    cursor.execute("CREATE INDEX idx_customer_uid ON Customer(U_ID);")
    print("UserID indexed.")

    cursor.execute("CREATE INDEX idx_product_pid ON Product(P_ID);")
    print("ProdID indexed.")

def main():
    connection = connect_to_db()
    cursor = connection.cursor()
    
    try:
        create_indexes(cursor)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
