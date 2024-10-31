import mysql.connector

# Establish database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="labdatabase"
)

cursor = conn.cursor()

def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            U_ID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100),
            Email VARCHAR(100) NOT NULL,
            Password VARCHAR(100) NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Category (
            C_ID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100),
            Picture TEXT,
            Description TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            P_ID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100),
            Price DECIMAL(10, 2),
            Description TEXT,
            C_ID INT,
            FOREIGN KEY (C_ID) REFERENCES Category(C_ID)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OrderInfo (
            O_ID INT AUTO_INCREMENT PRIMARY KEY,
            C_ID INT,
            Amount DECIMAL(10, 2),
            Date DATE,
            FOREIGN KEY (C_ID) REFERENCES Customer(U_ID)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Payment (
            P_ID INT AUTO_INCREMENT PRIMARY KEY,
            Type VARCHAR(50),
            Amount DECIMAL(10, 2),
            U_ID INT,
            FOREIGN KEY (U_ID) REFERENCES Customer(U_ID)
        );
    ''')

create_tables(cursor)

print("OK.")

cursor.close()
conn.close()
