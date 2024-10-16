import psycopg2

from model import Matrix

def create(matrix_name, matrix_data):
    """
    Generate a CREATE TABLE statement for a matrix and create a Matrix object.

    Parameters:
        matrix_name (str): The name of the matrix.
        matrix_data (list of list of float): The matrix data as a list of rows.

    Returns:
        tuple: (CREATE TABLE SQL statement, Matrix object)
    """
    # Get the dimensions of the matrix
    num_rows = len(matrix_data)
    num_cols = len(matrix_data[0]) if num_rows > 0 else 0

    # Create the CREATE TABLE SQL statement
    create_table_sql = f"CREATE TABLE {matrix_name} (\n"
    create_table_sql += ",\n".join([f"c{i + 1} DOUBLE PRECISION" for i in range(num_cols)]) + "\n);"

    # Create the Matrix object
    matrix_obj = Matrix(matrix_name, (num_rows, num_cols))

    return create_table_sql, matrix_obj

def update(matrix_name, matrix_data):
    """
    Generate SQL statements to replace all data in a matrix table.

    Parameters:
        matrix_name (str): The name of the matrix table.
        matrix_data (list of list of float): The matrix data as a list of rows.

    Returns:
        str: The combined SQL statements for deleting existing data and inserting new data.
    """
    # Get the number of columns based on the first row of the matrix data
    num_cols = len(matrix_data[0]) if len(matrix_data) > 0 else 0

    # Generate the column names (c1, c2, ..., cn)
    column_names = ", ".join([f"c{i + 1}" for i in range(num_cols)])

    # Generate the values for each row
    value_rows = []
    for row in matrix_data:
        # Format each row as a string of comma-separated values
        values = ", ".join([str(value) for value in row])
        value_rows.append(f"({values})")

    # Join all value rows with commas
    values_clause = ",\n".join(value_rows)

    # Create the DELETE statement to remove all existing data
    delete_sql = f"DELETE FROM {matrix_name};"

    # Create the INSERT INTO SQL statement to add the new data
    insert_sql = f"INSERT INTO {matrix_name} ({column_names}) VALUES\n{values_clause};"

    # Combine both statements
    replace_sql = f"{delete_sql}\n{insert_sql}"

    return replace_sql

def get_matrix_dimensions(conn, matrix_name):
    # Retrieve the number of columns (width) from the matrix table
    with conn.cursor() as cur:
        cur.execute(f"SELECT count(*) FROM information_schema.columns WHERE table_name = '{matrix_name}'")
        cols = cur.fetchone()[0]
    # Get the number of rows (height)
    with conn.cursor() as cur:
        cur.execute(f"SELECT count(*) FROM {matrix_name}")
        rows = cur.fetchone()[0]
    return rows, cols

def validate_multiplication(dimA, dimB):
    # Check if the number of columns in A equals the number of rows in B
    return dimA[1] == dimB[0]

def generate_matrix_multiplication_sql(A: Matrix, B: Matrix, C: Matrix):
    # Assume matrixA is MxN and matrixB is NxP, and the result matrix will be MxP
    dimA = A.get_dimensions()
    dimB = B.get_dimensions()
    num_rows_A, num_cols_A = dimA
    num_cols_B = dimB[1]
    
    # Create the CREATE TABLE statement for the result matrix
    create_table_sql = f"CREATE TABLE {C.get_name()} ("
    create_table_sql += ", ".join([f"c{i + 1} DOUBLE PRECISION" for i in range(num_cols_B)]) + ");"

    # Generate the multiplication SQL query
    select_clauses = []
    for j in range(num_cols_B):  # Columns in matrixB
        clause = " + ".join([f"(a.c{i + 1} * b.c{j + 1})" for i in range(num_cols_A)])
        select_clauses.append(f"SUM({clause}) AS c{j + 1}")

    insert_sql = f"INSERT INTO {C.get_name()} ({', '.join([f'c{i + 1}' for i in range(num_cols_B)])})\n"
    insert_sql += "SELECT " + ", ".join(select_clauses) + "\n"
    insert_sql += f"FROM {A.get_name()} a, {B.get_name()} b\n"
    insert_sql += "WHERE a.row_id = b.row_id\n"  # Need a unique column in both
    insert_sql += "GROUP BY a.row_id;"
    return create_table_sql, insert_sql

if __name__ == "__main__":

    m, n, p = 3, 10, 4

    create_query, insert_query = generate_matrix_multiplication_sql(    
        Matrix("matrix_a", (m, n)),
        Matrix("matrix_b", (n, p)),
        Matrix("matrix_c", (m, p))
    )

    print (f"Create: {create_query}")
    print (f"Insert: {insert_query}")
