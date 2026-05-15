import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        # If the file doesn't exist, SQLite will create it automatically
        conn = sqlite3.connect("./rep-database.db")
        print(f"Connected to SQLite. Version: {sqlite3.version}")
        return conn
    except Error as e:
        print(f"Error: {e}")
    
    return conn

def create_table(conn):
    """ Create a sample table structure """
    try:
        sql_create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id integer PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL,
            email text UNIQUE,
            join_date timestamp DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor = conn.cursor()
        cursor.execute(sql_create_users_table)
        print("Table 'users' created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")

def main():
    database = "my_app_database.db"

    # 1. Establish connection
    conn = create_connection(database)

    # 2. Create tables
    if conn is not None:
        create_table(conn)
        
        # 3. Close the connection when done
        conn.close()
        print("Connection closed.")
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()