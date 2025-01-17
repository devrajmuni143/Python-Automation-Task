import sys
import os
# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import DatabaseManager
from backend import FileProcessor
from analysis import AnalysisManager
import streamlit as st

# Set the page layout to wide
st.set_page_config(page_title="Revenue Dashboard", layout="wide")

class StreamlitApp:
    def __init__(self):
        # Replace these with your actual database credentials
        host = "localhost"
        user = "root"
        password = "root"
        database = "revenue_db"

        # Initialize the DatabaseManager with proper arguments
        self.db_manager = DatabaseManager(host, user, password, database)
        self.file_processor = FileProcessor(self.db_manager)
        self.analysis_manager = AnalysisManager(self.db_manager)
    def run(self):
        # Create database tables if they don't exist
        self.db_manager.create_tables()

        # Divide the screen into two columns
        col1, col2 = st.columns(2)

        with col1:
            # File uploader in the left column
            uploaded_files = st.file_uploader(
                "Choose one or more CSV files", type=["csv"], accept_multiple_files=True
            )
            if uploaded_files:
                self.file_processor.process_multiple_files(uploaded_files)
            self.analysis_manager.perform_analysis1()
            self.analysis_manager.perform_analysis2()
            self.analysis_manager.perform_analysis3()
            self.analysis_manager.perform_analysis4()
            self.analysis_manager.perform_analysis5()
        with col2:
            # Display records from the database in the right column
            st.header("Database Records")
            df = self.db_manager.fetch_all_records_as_dataframe()
            df['city_code'] = df['city_code'].astype(str)
            if not df.empty:
                # Reset the index to start from 1
                df.index = df.index + 1

                # Display the DataFrame as an interactive table with container width
                st.dataframe(df, use_container_width=True)
            else:
                st.write("No records found in the database.")
                # Display the record with the maximum revenue
        st.title('Data Visualization')
        self.analysis_manager.display_visualizations()


if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
