import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
from api import create, update

@contextmanager
def get_db_connection(dbname, user, password, host="localhost", port="5432"):
    """
    Context manager to handle connecting to a PostgreSQL database.
    
    Parameters:
        dbname (str): The name of the database.
        user (str): The username used to authenticate.
        password (str): The password used to authenticate.
        host (str, optional): The host of the database. Defaults to "localhost".
        port (str, optional): The port of the database. Defaults to "5432".
        
    Yields:
        connection: A connection object to the PostgreSQL database.
    """
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        yield conn
    except psycopg2.DatabaseError as e:
        print(f"Error connecting to the database: {e}")
        raise
    finally:
        if conn is not None:
            conn.close()

# Example usage
if __name__ == "__main__":
    # Database configuration
    db_config = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "admin",
        "host": "localhost",
        "port": "5432"
    }

    # Using the get_db_connection function
    with get_db_connection(**db_config) as conn:
        print("Connected to the database successfully!")
        # You can now use conn to execute queries, etc.
        # e.g., with conn.cursor() as cur: cur.execute("SELECT 1")
        # Example usage
        matrix_name = "matrixA"
        matrix_data = [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0]
        ]

        create_table_sql, matrix_obj = create(matrix_name, matrix_data)
        update_sql = update(matrix_name, matrix_data)
        print("Generated CREATE TABLE statement:")
        print(create_table_sql)
        print("\nMatrix object:")
        print(f"Name: {matrix_obj.name}, Dimensions: {matrix_obj.dim}")
        print("Generate SQL to update matrix values:")
        print(update_sql)
        