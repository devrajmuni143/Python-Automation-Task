from multiprocessing.connection import default_family

import streamlit as st
import pandas as pd
import plotly.express as px

class AnalysisManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def perform_analysis1(self):
        st.write('**Q1. What is the total revenue (in crores) generated from all plans across all cities?**')
        records = self.db_manager.fetch_all_records_as_dataframe()
        if not records.empty:
            if 'plan_revenue_crores' in records.columns:
                total_revenue = records['plan_revenue_crores'].sum()
                st.write(f"Ans 1. Total Revenue: {total_revenue} Crores")
            else:
                st.write("'plan_revenue_crores' column not found in the DataFrame.")
        else:
            st.write("No data available to calculate total revenue.")

    def perform_analysis2(self):
        st.write('**Q2. Which city (city_code) generated the highest revenue on a single day?**')
        max_revenue_record = self.db_manager.get_record_with_max_revenue()
        if isinstance(max_revenue_record, dict):
            st.write(
                f"Ans 2. City Code: {max_revenue_record['city_code']} | "
                f"Total Revenue: {max_revenue_record['tot_revenue']} | Date: {max_revenue_record['date']}"
            )
        else:
            st.write("Error fetching the record.")

    def perform_analysis3(self):
        st.write('**Q3. Which plan generated the highest total revenue across all cities?**')
        all_records = self.db_manager.get_plan_with_max_revenue()
        if isinstance(all_records, dict):
            st.write(
                f"Ans 3. Plan: {all_records['plans']} | Total Revenue: {all_records['tot_revenue']}"
            )
        else:
            st.write("Error fetching the record.")

    def perform_analysis4(self):
        st.write('**Q4. How many cities (city_code) contributed to the total revenue for the plan "p3"?**')
        count = self.db_manager.get_total_city_count()
        if isinstance(count, dict):
            st.write(f"Ans 4. Total City Count: {count['city_count']}")
        else:
            st.write("Error fetching the count.")

    def perform_analysis5(self):
        st.write('**Q5. Which city contributed the most to the total revenue across all plans?**')
        city_details = self.db_manager.get_city_by_revenue_across_plans()
        if isinstance(city_details, dict):
            st.write(
                f"Ans 5. City Code: {city_details['city_code']} | "
                f"Total Revenue: {city_details['total_revenue']}"
            )
        else:
            st.write("Error fetching the details.")

    def display_visualizations(self):

        # Fetch all records as a DataFrame
        df = self.db_manager.fetch_all_records_as_dataframe()
        df['city_code'] = df['city_code'].astype(str)
        import pandas as pd
        import plotly.express as px
        import streamlit as st

        st.subheader('Revenue Trend By Month')
        df['date'] = pd.to_datetime(df['date'])

        # Aggregate data by month
        df_monthly = df.groupby('date', as_index=False)['plan_revenue_crores'].sum()

        # Calculate the max value for the y-axis
        max_value = df_monthly['plan_revenue_crores'].max()

        # Create the line chart
        fig_line = px.line(
            df_monthly,
            x='date',
            y='plan_revenue_crores',
            labels={'date': 'Date', 'plan_revenue_crores': 'Revenue (in Crores)'},
            text='plan_revenue_crores',  # Add data labels
        )

        # Update layout to show all months on the x-axis
        fig_line.update_traces(
            textposition='top center'  # Position data labels above the data points
        )

        fig_line.update_layout(
            xaxis_title='Date',
            yaxis_title='Revenue (in Crores)',
            xaxis_tickformat='%b %Y',  # Format ticks as "Month Year"
            xaxis=dict(
                tickmode='linear',  # Show all ticks
                dtick="M1",  # Force tick interval to 1 month
            ),
            yaxis=dict(range=[0, max_value * 1.1]),  # Ensure y-axis starts at 0 and ends slightly above max value
            hovermode='x unified',
            showlegend=False,  # Hide the legend as the line is self-explanatory
        )

        # Display the chart
        st.plotly_chart(fig_line)

        # Group by city_code and sum the revenue
        df_grouped = df.groupby('city_code')['plan_revenue_crores'].sum().reset_index()

        # # Ensure city_code is treated as a string to avoid formatting issues

        # Create the bar chart for Sales By City
        fig_bar = px.bar(
            df_grouped,
            x='city_code',  # Column name as a string
            y='plan_revenue_crores',  # Column name as a string
            labels={'city_code': 'City Code', 'plan_revenue_crores': 'Revenue (in Crores)'}
        )

        # Add data labels
        fig_bar.update_traces(texttemplate='%{y:.2f}', textposition='outside')

        # Update layout for readability
        fig_bar.update_layout(
            xaxis_title='City Code',
            yaxis_title='Revenue (in Crores)',
            xaxis=dict(type='category'),  # Ensure city codes are treated as categories
            showlegend=False
        )
        st.subheader('Revenue By City')
        # Display the bar chart
        st.plotly_chart(fig_bar)

        # Group by city_code and sum the revenue
        df_grouped = df.groupby('plans')['plan_revenue_crores'].sum().reset_index()

        # # Ensure city_code is treated as a string to avoid formatting issues

        # Create the bar chart for Sales By City
        fig_bar = px.bar(
            df_grouped,
            x='plans',  # Column name as a string
            y='plan_revenue_crores',  # Column name as a string
            labels={'city_code': 'Plans', 'plan_revenue_crores': 'Revenue (in Crores)'}
        )

        # Add data labels
        fig_bar.update_traces(texttemplate='%{y:.2f}', textposition='outside')

        # Update layout for readability
        fig_bar.update_layout(
            xaxis_title='Plans',
            yaxis_title='Revenue (in Crores)',
            xaxis=dict(type='category'),  # Ensure city codes are treated as categories
            showlegend=False
        )
        st.subheader('Revenue By City')
        # Display the bar chart
        st.plotly_chart(fig_bar)