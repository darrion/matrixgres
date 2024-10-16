import psycopg2

from model import Matrix

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
        clause = " + ".join([f"a.c{i + 1} * b.c{j + 1}" for i in range(num_cols_A)])
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
