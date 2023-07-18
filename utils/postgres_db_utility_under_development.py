import psycopg2
from config import logger

# Replace the following with your PostgreSQL connection details
db_config = {
    "host": "localhost",
    "port": "5432",
    "database": "your_database",
    "user": "your_username",
    "password": "your_password",
}

def connect_to_postgres():
    try:
        conn = psycopg2.connect(**db_config)
        logger.info("Connected to PostgreSQL successfully!")
        return conn
    except psycopg2.Error as e:
        logger.error("Could not connect to PostgreSQL: ", e)
        return None

def create_table(conn):
    try:
        cursor = conn.cursor()

        # Create a table called "my_table" with appropriate columns
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS my_table ("
            "id SERIAL PRIMARY KEY,"
            "name VARCHAR(255) NOT NULL,"
            "age INT,"
            "email VARCHAR(255)"
            ");"
        )

        cursor.execute(create_table_query)
        print("Table 'my_table' created successfully!")
        cursor.close()
    except psycopg2.Error as e:
        print("Error:", e)

def insert_record(conn, record_data):
    try:
        cursor = conn.cursor()

        # Insert a record into the table
        insert_query = "INSERT INTO my_table (name, age, email) VALUES (%s, %s, %s);"
        cursor.execute(insert_query, record_data)
        conn.commit()

        print("Record inserted successfully!")
        cursor.close()
    except psycopg2.Error as e:
        print("Error:", e)

def delete_record(conn, record_id):
    try:
        cursor = conn.cursor()

        # Delete a record from the table by ID
        delete_query = "DELETE FROM my_table WHERE id = %s;"
        cursor.execute(delete_query, (record_id,))
        conn.commit()

        print("Record deleted successfully!")
        cursor.close()
    except psycopg2.Error as e:
        print("Error:", e)

def update_record(conn, record_id, updated_data):
    try:
        cursor = conn.cursor()

        # Update a record in the table by ID
        update_query = "UPDATE my_table SET name = %s, age = %s, email = %s WHERE id = %s;"
        cursor.execute(update_query, (*updated_data, record_id))
        conn.commit()

        print("Record updated successfully!")
        cursor.close()
    except psycopg2.Error as e:
        print("Error:", e)