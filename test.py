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
SELECT u.UserID, u.Username, u.Email,
       COUNT(c.CommentID) AS TotalComments,
       AVG(c.Rating) AS AvgRatingGiven,
       COUNT(DISTINCT c.ProductID) AS TotalProductsReviewed,
       lc.LastComment AS LastComment,
       lc.LastCommentDate AS LastCommentDate
FROM User u
LEFT JOIN Comment c ON u.UserID = c.UserID
LEFT JOIN (
    SELECT UserID, Comment AS LastComment, PublishDate AS LastCommentDate
    FROM Comment
    WHERE (UserID, PublishDate) IN (
        SELECT UserID, MAX(PublishDate) AS LastCommentDate
        FROM Comment
        GROUP BY UserID
    )
) AS lc ON u.UserID = lc.UserID
GROUP BY u.UserID, u.Username, u.Email, lc.LastComment, lc.LastCommentDate
ORDER BY TotalComments DESC, LastCommentDate DESC, AvgRatingGiven DESC;
"""

execute_query(query)
