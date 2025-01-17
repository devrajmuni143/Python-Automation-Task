from backend.dbcon import DatabaseConnectionManager
import pandas as pd

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.db_manager = DatabaseConnectionManager(host, user, password, database)

    def create_tables(self):
        """Creates necessary tables in the database."""
        try:
            with self.db_manager.get_connection_and_cursor() as (connection, cursor):
                if connection is None or cursor is None:
                    print("Failed to create tables due to database connection error.")
                    return

                # Table to store the imported files
                create_imported_files_table_query = """
                CREATE TABLE IF NOT EXISTS imported_files (
                    filename VARCHAR(255) NOT NULL PRIMARY KEY
                );
                """
                cursor.execute(create_imported_files_table_query)
                connection.commit()

                # Table for the revenue data
                create_revenue_data_table_query = """
                CREATE TABLE IF NOT EXISTS revenue_data (
                    date DATE NOT NULL,
                    city_code INT NOT NULL,
                    plans VARCHAR(10) NOT NULL,
                    plan_revenue_crores FLOAT NOT NULL,
                    PRIMARY KEY (date, city_code, plans)
                );
                """
                cursor.execute(create_revenue_data_table_query)
                connection.commit()
        except Exception as e:
            print(f"Error while creating tables: {e}")

    def is_file_imported(self, filename):
        """Checks if a file has already been imported."""
        try:
            with self.db_manager.get_connection_and_cursor() as (connection, cursor):
                if connection is None or cursor is None:
                    print("Failed to check file due to database connection error.")
                    return False

                query = "SELECT 1 FROM imported_files WHERE filename = %s;"
                cursor.execute(query, (filename,))
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            print(f"Error while checking if file is imported: {e}")
            return False

    def mark_file_as_imported(self, filename):
        """Marks a file as imported in the database."""
        try:
            with self.db_manager.get_connection_and_cursor() as (connection, cursor):
                if connection is None or cursor is None:
                    print("Failed to mark file as imported due to database connection error.")
                    return

                query = "INSERT INTO imported_files (filename) VALUES (%s);"
                cursor.execute(query, (filename,))
                connection.commit()
        except Exception as e:
            print(f"Error while marking file as imported: {e}")

    def insert_data_to_revenue_table(self, df):
        """Inserts data from a DataFrame into the revenue_data table."""
        try:
            with self.db_manager.get_connection_and_cursor() as (connection, cursor):
                if connection is None or cursor is None:
                    print("Failed to insert data due to database connection error.")
                    return

                for _, row in df.iterrows():
                    try:
                        insert_query = """
                        INSERT INTO revenue_data (date, city_code, plans, plan_revenue_crores)
                        VALUES (%s, %s, %s, %s);
                        """
                        cursor.execute(insert_query, (row['date'], row['city_code'], row['plans'], row['plan_revenue_crores']))
                    except Exception as row_error:
                        print(f"Error inserting row {row}: {row_error}")

                connection.commit()
        except Exception as e:
            print(f"Error while inserting data into revenue table: {e}")

    def fetch_all_records_as_dataframe(self):
        """Fetches all records from the revenue_data table and returns them as a DataFrame."""
        try:
            query = "SELECT * FROM revenue_data"
            with self.db_manager.get_connection_and_cursor() as (connection, cursor):
                if connection is None or cursor is None:
                    print("Failed to fetch records due to database connection error.")
                    return pd.DataFrame()

                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]  # Get column names
                return pd.DataFrame(rows, columns=columns)
        except Exception as e:
            print(f"Error while fetching records as DataFrame: {e}")
            return pd.DataFrame()

    def get_record_with_max_revenue(self):
        """Fetches all records from the revenue_data table and returns them as a DataFrame."""
        try:
            query = """
            SELECT 
                city_code,
                date,
                round(sum(plan_revenue_crores),2) as tot_revenue
            FROM revenue_data
            GROUP BY city_code, date
            ORDER BY tot_revenue DESC
            LIMIT 1;
            """
            with self.db_manager.get_connection_and_cursor() as (connection, cursor):
                if connection is None or cursor is None:
                    print("Failed to fetch records due to database connection error.")
                    return "No data available."

                cursor.execute(query)
                row = cursor.fetchone()  # Fetch one row (the one with max revenue)
                print("Row fetched:", row)  # Debugging: print the row fetched
                if row:
                    # Access dictionary values correctly
                    city_code = row['city_code']
                    date = row['date']
                    tot_revenue = row['tot_revenue']
                    # Return the result in a readable format
                    return row
                else:
                    return "No records found."
        except Exception as e:
            print(f"Error while fetching record with maximum revenue: {e}")
            return "Error fetching record."

    def get_plan_with_max_revenue(self):
        """Fetches all records from the revenue_data table and returns them as a DataFrame."""
        try:
            query = """
            SELECT 
                plans, 
                round(sum(plan_revenue_crores),2) as tot_revenue 
            from revenue_data
            group by plans
            order by tot_revenue desc
            limit 1
            """
            with self.db_manager.get_connection_and_cursor() as (connection, cursor):
                if connection is None or cursor is None:
                    print("Failed to fetch records due to database connection error.")
                    return "No data available."

                cursor.execute(query)
                row = cursor.fetchone()  # Fetch one row (the one with max revenue)
                print("Row fetched:", row)  # Debugging: print the row fetched
                if row:
                    # Access dictionary values correctly
                    plan = row['plans']
                    tot_revenue = row['tot_revenue']
                    # Return the result in a readable format
                    return row
                else:
                    return "No records found."
        except Exception as e:
            print(f"Error while fetching record with maximum revenue: {e}")
            return "Error fetching record."

    def get_total_city_count(self):
        """Fetches all records from the revenue_data table and returns them as a DataFrame."""
        try:
            query = """
           select 
                count(distinct(city_code)) as city_count 
            from revenue_data
            where plans='p3' and plan_revenue_crores <> 0
               """
            with self.db_manager.get_connection_and_cursor() as (connection, cursor):
                if connection is None or cursor is None:
                    print("Failed to fetch records due to database connection error.")
                    return "No data available."

                cursor.execute(query)
                row = cursor.fetchone()  # Fetch one row (the one with max revenue)
                print("Row fetched:", row)  # Debugging: print the row fetched
                if row:
                    # Access dictionary values correctly
                    city_count = row['city_count']
                    # Return the result in a readable format
                    return row
                else:
                    return "No records found."
        except Exception as e:
            print(f"Error while fetching record with maximum revenue: {e}")
            return "Error fetching record."

    def get_city_by_revenue_across_plans(self):
        """Fetches all records from the revenue_data table and returns them as a DataFrame."""
        try:
            query = """
                WITH RankedRevenue AS (
                SELECT
                    city_code,
                    plans,
                    plan_revenue_crores,
                    RANK() OVER (PARTITION BY plans ORDER BY plan_revenue_crores DESC) AS ranking
                FROM
                    revenue_data
                )
                SELECT
                    city_code,
                    ROUND(SUM(plan_revenue_crores),2) AS total_revenue
                FROM
                    RankedRevenue
                WHERE
                    ranking = 1
                GROUP BY
                    city_code
                ORDER BY
                    total_revenue DESC
                LIMIT 1;
               """
            with self.db_manager.get_connection_and_cursor() as (connection, cursor):
                if connection is None or cursor is None:
                    print("Failed to fetch records due to database connection error.")
                    return "No data available."

                cursor.execute(query)
                row = cursor.fetchone()  # Fetch one row (the one with max revenue)
                print("Row fetched:", row)  # Debugging: print the row fetched
                if row:
                    # Access dictionary values correctly
                    city_code = row['city_code']
                    total_revenue = row['total_revenue']
                    # Return the result in a readable format
                    return row
                else:
                    return "No records found."
        except Exception as e:
            print(f"Error while fetching record with maximum revenue: {e}")
            return "Error fetching record."
# if __name__ == "__main__":
#     # Replace these with your actual database credentials
#     host = "localhost"
#     user = "root"
#     password = "root"
#     database = "revenue_db"
#
#     # Initialize the DatabaseManager with the credentials
#     db_manager = DatabaseManager(host, user, password, database)
#
#     # Call the get_record_with_max_revenue method and print the result
#     print(db_manager.get_city_by_revenue_across_plans())