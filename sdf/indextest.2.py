import mysql.connector
import time

# Connect to the database
def connect_to_db():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='labdatabase'
    )
    return connection

def measure_query_time(query):
    connection = connect_to_db()
    cursor = connection.cursor()

    # Measure the time before executing the query
    start_time = time.time()

    cursor.execute(query)
    results = cursor.fetchall()

    # Measure the time after executing the query
    end_time = time.time()

    # Calculate and print the total time taken
    execution_time = end_time - start_time
    print(f"Query executed in {execution_time:.5f} seconds.")

    cursor.close()
    connection.close()

    return results, execution_time

if __name__ == "__main__":
    query = "SELECT * FROM Product WHERE C_ID = 1;"
    measure_query_time(query)
