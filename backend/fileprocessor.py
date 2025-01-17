import pandas as pd
import streamlit as st

class FileProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def process_file(self, uploaded_file):
        filename = uploaded_file.name

        try:
            # Check if file is already imported
            if self.db_manager.is_file_imported(filename):
                st.warning(f"The file '{filename}' has already been imported.")
                return

            try:
                # Reading and processing the file
                df = pd.read_csv(uploaded_file)
                df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
                df = df.dropna(subset=['date'])
                df['date'] = df['date'].dt.strftime('%Y-%m-%d')

                # Inserting data into the database and marking the file as imported
                self.db_manager.insert_data_to_revenue_table(df)
                self.db_manager.mark_file_as_imported(filename)

                st.success(f"Data from '{filename}' imported successfully.")

            except pd.errors.ParserError:
                st.error(f"Error parsing the file '{filename}'. Please ensure the file is a valid CSV.")
            except KeyError:
                st.error(f"Error: The file '{filename}' is missing required columns, such as 'date'.")
            except Exception as e:
                st.error(f"Error processing file '{filename}': {e}")

        except Exception as e:
            # Handle errors that might occur outside of file processing
            st.error(f"Unexpected error with file '{filename}': {e}")

    def process_multiple_files(self, uploaded_files):
        for uploaded_file in uploaded_files:
            self.process_file(uploaded_file)
