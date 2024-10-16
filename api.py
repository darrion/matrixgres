import psycopg2

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

def generate_matrix_multiplication_sql(matrixA, matrixB, result_matrix):
    # Assume matrixA is MxN and matrixB is NxP, and the result matrix will be MxP
    num_rows_A, num_cols_A = dimA
    num_cols_B = dimB[1]
    
    # Create the CREATE TABLE statement for the result matrix
    create_table_sql = f"CREATE TABLE {result_matrix} ("
    create_table_sql += ", ".join([f"c{i + 1} DOUBLE PRECISION" for i in range(num_cols_B)]) + ");"

    # Generate the multiplication SQL query
    select_clauses = []
    for j in range(num_cols_B):  # Columns in matrixB
        clause = " + ".join([f"a.c{i + 1} * b.c{j + 1}" for i in range(num_cols_A)])
        select_clauses.append(f"SUM({clause}) AS c{j + 1}")

    insert_sql = f"INSERT INTO {result_matrix} ({', '.join([f'c{i + 1}' for i in range(num_cols_B)])})\n"
    insert_sql += "SELECT " + ", ".join(select_clauses) + "\n"
    insert_sql += f"FROM {matrixA} a, {matrixB} b\n"
    insert_sql += "WHERE a.row_id = b.row_id\n"  # Need a unique column in both
    insert_sql += "GROUP BY a.row_id;"
    return create_table_sql, insert_sql
# Connect to database

