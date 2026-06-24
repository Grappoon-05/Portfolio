import mysql.connector
from mysql.connector import Error

# =====================
# CONNECTION FUNCTIONS
# =====================
def create_server_connection(host_name, user_name, user_password):
    """
    Function that establishes a global connection to a MySQL server using the provided credentials.

    parameters :
        - host_name : host address of the MySQL server (e.g, "localhost")
        - user_name : username for authentication
        - user_password : password associated with the user

    output :
        - connection : the MySQL server connection object, or None if an error occurs
    """
    connection = None # Close all existing connections so that the server isn't overwhelmed by multiple open connections.
    try:
        connection = mysql.connector.connect( # Attempt to connect to the server using a hostname, username, and password.
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_db_connection(host_name, user_name, user_password, db_name):
    """
    Function that establishes a targeted connection to a specific database on a MySQL server.

    parameters :
        - host_name : host address of the MySQL server
        - user_name : username for authentication
        - user_password : password associated with the user
        - db_name : name of the database to connect to

    output :
        - connection : the database connection object, or None if an error occurs
    """
    connection = None
    try:
        connection = mysql.connector.connect(# Attempt to establish a connection to the server using a hostname, username, password, and database.
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

# =======================
# SQL EXECUTION FUNCTION
# =======================
def create_database(connection, query):
    """
    Function that creates the database by executing the given SQL query on the server via the connection.

    parameters :
        - connection : the connection object to the database server
        - query : the SQL query string used to create the database
    """
    cursor = connection.cursor() # The cursor method allows you to create a cursor object based on a connection object.
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def execute_query(connection, query):
    """
    Function that executes an SQL query, passed as a string, on the server using the connection cursor.

    parameter :
        - connection : the connection object to the database
        - query : the SQL query string to be executed
    """
    cursor = connection.cursor() # The cursor method allows you to create a cursor object based on a connection object.
    try:
        cursor.execute(query) # Allows SQL queries to be executed on the server
        connection.commit() # Ensures that the detailed SQL query statements are implemented.
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def ajouter_modifier_pieces(connection, serial_number, parts_type, qt2add):
    """
    Function that adds a new part to the database using its serial number, or increases its quantity if the part already exists.

    parameter :
        - connection : the connection object to the database
        - serial_number : the unique serial number of the part
        - parts_type : the category or type of the part
        - qt2add : the quantity to add to the inventory
    """
    cursor = connection.cursor()
    query = """
    INSERT INTO parts_inventory (serial_number, parts_type, quantity)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE quantity = quantity + %s;
    """
    # The values to replace “%s” with.
    # We pass `quantity_to_add` twice: once for the `VALUES` clause and once for the `UPDATE` clause.
    
    values = (serial_number, parts_type, qt2add, qt2add)
    
    try:
        cursor.execute(query, values) # Allows SQL queries to be executed on the server using the specified values
        connection.commit() # Ensures that the detailed SQL query statements are implemented.
        print(f"Parts '{serial_number}' successfully treated (Add quantity : {qt2add}).")
    except Error as err:
        print(f"Error while processing the part : '{err}'")

# ============================================================
# ESTABLISHING THE CONNECTION, EXECUTION, MODIFICATION, ETC.
# ============================================================

connection = create_server_connection("localhost", "sae", "ocr")

create_database_query = "CREATE DATABASE IF NOT EXISTS SAE"
create_database(connection, create_database_query)

create_SerialNumber_table = """
CREATE TABLE IF NOT EXISTS parts_inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    serial_number VARCHAR(100) NOT NULL UNIQUE,
    parts_type VARCHAR(150) NOT NULL,
    quantity INT NOT NULL DEFAULT 0
);
""" # A variable that creates an SQL table if one does not already exist, with the category names on the left, the types in the center, and the parameters associated with those types for each category.

connection = create_db_connection("localhost", "sae", "ocr", "SAE")
execute_query(connection, create_SerialNumber_table)
