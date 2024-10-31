import mysql.connector
import time

def execute_query(query):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="labdatabase"
        )

        cursor = connection.cursor()

        cursor.execute("SHOW SESSION STATUS LIKE 'Handler_read%'")
        initial_reads = {name: int(value) for name, value in cursor.fetchall()}

        cursor.execute("SHOW SESSION STATUS LIKE 'Handler_write'")
        initial_writes = int(cursor.fetchone()[1])

        start_time = time.time()

        cursor.execute(query)

        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()

        else:
            connection.commit()

        end_time = time.time()
        execution_time = end_time - start_time

        cursor.execute("SHOW SESSION STATUS LIKE 'Handler_read%'")
        final_reads = {name: int(value) for name, value in cursor.fetchall()}

        cursor.execute("SHOW SESSION STATUS LIKE 'Handler_write'")
        final_writes = int(cursor.fetchone()[1])

        read_operations = {key: final_reads[key] - initial_reads[key] for key in initial_reads}
        total_read_operations = sum(read_operations.values())
        print(f"Total Read Operations: {total_read_operations}")
        write_operations = final_writes - initial_writes

        print(f"Execution Time: {execution_time:.6f} seconds")
        print("Read Operations:", read_operations)
        print(f"Write Operations: {write_operations}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        connection.close()

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
