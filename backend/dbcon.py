from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error


class DatabaseConnectionManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    @contextmanager
    def get_connection_and_cursor(self):
        """Context manager to yield a connection and cursor with error handling."""
        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if connection.is_connected():
                print("Connection Successful!")
            else:
                print("Failed to connect to the server")

            cursor = connection.cursor(dictionary=True)
            yield connection, cursor  # Yield the resources to the caller
        except Error as e:
            print(f"Database error occurred: {e}")
            yield None, None  # Return None for both connection and cursor in case of an error
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()


# import mysql.connector
# from contextlib import contextmanager
#
# @contextmanager
# def get_database_connection_and_cursor():
#     connection = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='root',
#         database='revenue_db'
#     )
#
#     if connection.is_connected():
#         print('Connection Successful!')
#     else:
#         print('Failed in connecting the server')
#
#     cursor = connection.cursor(dictionary=True)
#     try:
#         yield connection, cursor  # Yield both connection and cursor
#     finally:
#         cursor.close()
#         connection.close()
#
# def fetch_all_records():
#     with get_database_connection_and_cursor() as (connection, cursor):
#         cursor.execute('SELECT * FROM revenue_data')
#         records = cursor.fetchall()
#         for record in records:
#             print(record)
#         print(len(records))
#
