import psycopg2
from psycopg2 import sql
from contextlib import contextmanager

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
        "dbname": "your_database_name",
        "user": "your_username",
        "password": "your_password",
        "host": "localhost",
        "port": "5432"
    }

    # Using the get_db_connection function
    with get_db_connection(**db_config) as conn:
        print("Connected to the database successfully!")
        # You can now use conn to execute queries, etc.
        # e.g., with conn.cursor() as cur: cur.execute("SELECT 1")
