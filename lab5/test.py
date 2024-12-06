import mysql.connector
import time

def execute_query(query):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="labdatabase"
        )

        cursor = connection.cursor()

        # Initial read/write status before executing the query
        cursor.execute("SHOW SESSION STATUS LIKE 'Handler_read%'")
        initial_reads = {name: int(value) for name, value in cursor.fetchall()}

        cursor.execute("SHOW SESSION STATUS LIKE 'Handler_write'")
        initial_writes = int(cursor.fetchone()[1])

        # Measure execution time
        start_time = time.time()
        cursor.execute(query)

        # Fetch results if it's a SELECT query; otherwise, commit changes
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()  # Only for SELECT queries
            if results:
                print(f"Number of rows returned: {len(results)}")
            else:
                print("No results returned.")
        else:
            connection.commit()

        end_time = time.time()
        execution_time = end_time - start_time

        # Final read/write status after executing the query
        cursor.execute("SHOW SESSION STATUS LIKE 'Handler_read%'")
        final_reads = {name: int(value) for name, value in cursor.fetchall()}

        cursor.execute("SHOW SESSION STATUS LIKE 'Handler_write'")
        final_writes = int(cursor.fetchone()[1])

        # Calculate the difference in reads and writes for this specific query
        read_operations = {key: final_reads[key] - initial_reads[key] for key in initial_reads}
        total_read_operations = sum(read_operations.values())
        write_operations = final_writes - initial_writes

        # Output the execution time, read and write operations
        print(f"Execution Time: {execution_time:.6f} seconds")
        print(f"Total Read Operations: {total_read_operations}")
        print("Detailed Read Operations:", read_operations)
        print(f"Write Operations: {write_operations}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        connection.close()

# Example query
query = """
SELECT pc.CategoryType, p.ProductID, p.ProductName, p.AvgRating AS MaxRating,
       o.OwnerID, o.OwnerName,
       COALESCE(SUM(oi.Quantity), 0) AS TotalQuantitySold
FROM ProductCategory pc
JOIN Product p ON pc.ProductCategoryID = p.ProductCategoryID
JOIN Owner o ON p.OwnerID = o.OwnerID
LEFT JOIN OrderItems oi ON p.ProductID = oi.ProductCopyID
WHERE p.AvgRating = (
    SELECT MAX(sub_p.AvgRating)
    FROM Product sub_p
    WHERE sub_p.ProductCategoryID = pc.ProductCategoryID
)
GROUP BY pc.CategoryType, p.ProductID, p.ProductName, p.AvgRating, o.OwnerID, o.OwnerName
ORDER BY pc.CategoryType, p.AvgRating DESC;
"""

execute_query(query)
