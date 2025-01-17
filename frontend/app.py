import sys
import os
# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import plotly.express as px
import streamlit as st
from backend import DatabaseManager
from backend import FileProcessor

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
            self.perform_analysis1()
            self.perform_analysis2()
            self.perform_analysis3()
            self.perform_analysis4()
            self.perform_analysis5()
        with col2:
            # Display records from the database in the right column
            st.header("Database Records")
            df = self.db_manager.fetch_all_records_as_dataframe()
            if not df.empty:
                # Reset the index to start from 1
                df.index = df.index + 1

                # Display the DataFrame as an interactive table with container width
                st.dataframe(df, use_container_width=True)
            else:
                st.write("No records found in the database.")
                # Display the record with the maximum revenue
        st.columns(1)
        st.header('Data Visualization')
        df = self.db_manager.fetch_all_records_as_dataframe()
        df['city_code'] = df['city_code'].astype(str)
        st.subheader('Sales By City')
        fig_bar = px.bar(df,x='city_code', y='plan_revenue_crores')

        fig_bar.update_layout(
            xaxis_title='City Code',
            yaxis_title='Revenue (in Crores)',
            xaxis_tickangle=-45,  # Rotate x-axis labels for better visibility


        )
        st.plotly_chart(fig_bar)

        st.subheader('Revenue Trend By Month')

        # Fetch data
        df = self.db_manager.fetch_all_records_as_dataframe()

        # Ensure 'date' is properly formatted as a datetime type
        df['date'] = pd.to_datetime(df['date'])

        # Aggregate revenue by month if necessary
        # Replace with appropriate aggregation logic for your dataset
        df_monthly = df.groupby('date', as_index=False)['plan_revenue_crores'].sum()

        # Create line chart
        fig_line = px.line(
            df_monthly,
            x='date',
            y='plan_revenue_crores',
            title='Revenue Trend By Month',
            labels={'date': 'Date', 'plan_revenue_crores': 'Revenue (in Crores)'},
        )

        # Customize layout
        fig_line.update_layout(
            xaxis_title='Date',
            yaxis_title='Revenue (in Crores)',
            xaxis_tickformat='%b %Y',  # Format x-axis as "Month Year"
            hovermode='x unified',  # Show unified hover for all data points
        )

        # Display the chart
        st.plotly_chart(fig_line)

    def perform_analysis1(self):
        st.header("Data Analysis")

        # Fetch all records from the database as a DataFrame
        records = self.db_manager.fetch_all_records_as_dataframe()

        if not records.empty:
            # Calculate the total revenue using the correct column name
            st.write('Q1. What is the total revenue (in crores) generated from all plans across all cities?')
            if 'plan_revenue_crores' in records.columns:
                total_revenue = records['plan_revenue_crores'].sum()
                st.write(f"     Ans 1. Total Revenue: {total_revenue} Crores")
            else:
                st.write("'plan_revenue_crores' column not found in the DataFrame.")
        else:
            st.write("No data available to calculate total revenue.")

    def perform_analysis2(self):
        st.write('Q2. Which city (city_code) generated the highest revenue on a single day?')
        # Get the record with max revenue from the database
        max_revenue_record = self.db_manager.get_record_with_max_revenue()
        # Check if max_revenue_record is a string (indicating an error message)
        if isinstance(max_revenue_record, dict):
            st.write(f'Ans 2. City Code : {max_revenue_record['city_code']} | Total Revenue : {max_revenue_record['tot_revenue']} | Date : {max_revenue_record['date']} ')

    def perform_analysis3(self):
        st.write('Q3. Which plan generated the highest total revenue across all cities?')
        # Get the record with max revenue from the database
        all_records = self.db_manager.get_plan_with_max_revenue()
        # Check if max_revenue_record is a string (indicating an error message)
        if isinstance(all_records, dict):
            st.write(f'Ans 3. Plan : {all_records['plans']} | Total Revenue : {all_records['tot_revenue']} ')

    def perform_analysis4(self):
        st.write('Q4. How many cities (city_code) contributed to the total revenue for the plan "p3"?')
        # Get the record with max revenue from the database
        count = self.db_manager.get_total_city_count()
        # Check if max_revenue_record is a string (indicating an error message)
        if isinstance(count, dict):
            st.write(f'Ans 4. Total City Count  : {count['city_count']}  ')

    def perform_analysis5(self):
        st.write('Q5. Which city contributed the most to the total revenue across all plans?')
        # Get the record with max revenue from the database
        city_details = self.db_manager.get_city_by_revenue_across_plans()
        # Check if max_revenue_record is a string (indicating an error message)
        if isinstance(city_details, dict):
            st.write(f'Ans 5. City Code  : {city_details['city_code']} | Total Revenue  : {city_details['total_revenue']}  ')


if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
