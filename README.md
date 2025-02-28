# Revenue Dashboard - Streamlit Application

## Overview
The Revenue Dashboard is a Streamlit application designed for visualizing and analyzing revenue data. The application enables users to upload CSV files containing revenue data, store them in a MySQL database, and perform various analyses, such as identifying the highest revenue-generating cities and plans.


## Backend

### DatabaseConnectionManager (`dbcon.py`)
- Manages database connections with error handling using a context manager.
- Ensures proper closure of connections and cursors.

### DatabaseManager (`databasemanager.py`)
- Handles database interactions such as table creation, data insertion, and querying.
- Includes methods for specific analyses (e.g., fetching records with max revenue, plans with max revenue, and city counts).

### FileProcessor (`fileprocessor.py`)
- Processes single and multiple uploaded CSV files.
- Prevents duplicate file processing by maintaining a table of imported files.
- Validates and parses CSV files into the required format for database insertion.

---

## Frontend

### App (`app.py`)
- Sets up the Streamlit UI, including file uploaders, analysis display, and data visualization.
- Integrates backend functionality into an interactive user interface.

### AnalysisManager (`analysis.py`)
- Conducts analytical queries and displays results in Streamlit.
- Includes multiple analyses like total revenue, top-performing cities/plans, and city contributions.
- Provides data visualizations (e.g., revenue trends, bar charts).

---

## Higlighted Features
- **File Upload and Data Processing:**
  - Upload one or more CSV files.
  - Check if a file has already been imported to prevent duplicate uploads.
  - Parse and clean data, including handling missing or invalid dates.
  - Store data in a MySQL database for further analysis.
  - Provide Data Driven Analysis and Generate Dynamic Vi

- **Database Management:**
  - Automated table creation for storing imported files and revenue data.
  - Insert revenue data into the database.
  - Perform queries for analysis and insights.
  - Efficient data insertion and validation.
    
- **Data Visualization:**
  - Uses Plotly to provide clear and interactive charts.  
  - Interactive bar chart to visualize revenue by city.
  - Line chart to track revenue trends over time.

  **Error Handling**
  - Handles common database and file parsing issues with detailed logging.

- **Data Analysis:**
  - Total revenue across all plans and cities.
  - City generating the highest revenue on a single day.
  - Plan generating the highest total revenue.
  - Number of cities contributing to revenue for a specific plan (`p3`).
  - City with the highest total revenue across all plans.

## Folder Structure
```
project/
├── backend/
│   ├── dbcon.py
│   ├── databasemanager.py
│   ├── fileprocessor.py
├── frontend/
│   ├── app.py
│   ├── analysis.py


```
Floder Structure image
![image](https://github.com/user-attachments/assets/9ba229c0-6a6d-40c4-b5f0-cdf8b2b48066)


## Requirements
- Python 3.12
- MySQL Server
- Streamlit
- Plotly
- Pandas
- mysql-connector-python

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your MySQL database:
   - Create a database named `revenue_db`.
   - Update database credentials in `app.py`:
     ```python
     host = "localhost"
     user = "root"
     password = "root"
     database = "revenue_db"
     ```

4. Run the application:
   ```bash
   streamlit run frontend/app.py
   ```

## Usage
1. Launch the app by running the `streamlit` command.
2. Upload CSV files containing revenue data. Ensure the CSV files have the following columns:
   - `date` (DD-MM-YYYY format)
   - `city_code` (Integer)
   - `plans` (String)
   - `plan_revenue_crores` (Float)
3. Explore the dashboard for visualizations and insights.

## Modules

### 1. `dbcon.py`
Handles the database connection using a context manager for efficient resource management. Provides:
- Connection establishment.
- Error handling for database operations.

### 2. `databasemanager.py`
Handles database operations such as:
- Creating necessary tables.
- Checking if a file is already imported.
- Inserting data into the database.
- Fetching records and performing analytical queries.

### 3. `fileprocessor.py`
Processes CSV files:
- Reads and cleans data.
- Checks for missing or invalid entries.
- Inserts data into the database.

### 4. `app.py`
Main Streamlit application:
- User interface for uploading files and visualizing data.
- Diplaying all the records that has been uploaded
### 5. 'analysis.py'
Data Analysis & Visualization
- Performs analysis and displays results.
- Generates interactive charts using Plotly.

## Queries Performed

1. **Total Revenue:**
   ```sql
   SELECT SUM(plan_revenue_crores) AS total_revenue FROM revenue_data;
   ```

2. **Highest Revenue on a Single Day:**
   ```sql
   SELECT city_code, date, ROUND(SUM(plan_revenue_crores), 2) AS tot_revenue
   FROM revenue_data
   GROUP BY city_code, date
   ORDER BY tot_revenue DESC
   LIMIT 1;
   ```

3. **Highest Revenue Plan:**
   ```sql
   SELECT plans, ROUND(SUM(plan_revenue_crores), 2) AS tot_revenue
   FROM revenue_data
   GROUP BY plans
   ORDER BY tot_revenue DESC
   LIMIT 1;
   ```

4. **City Count for Plan `p3`:**
   ```sql
   SELECT COUNT(DISTINCT city_code) AS city_count
   FROM revenue_data
   WHERE plans = 'p3' AND plan_revenue_crores <> 0;
   ```

5. **City with Highest Revenue Across Plans:**
   ```sql
   WITH RankedRevenue AS (
       SELECT city_code, plans, plan_revenue_crores,
              RANK() OVER (PARTITION BY plans ORDER BY plan_revenue_crores DESC) AS ranking
       FROM revenue_data
   )
   SELECT city_code, ROUND(SUM(plan_revenue_crores), 2) AS total_revenue
   FROM RankedRevenue
   WHERE ranking = 1
   GROUP BY city_code
   ORDER BY total_revenue DESC
   LIMIT 1;
   ```

## Future Enhancements
- Add user authentication to secure the app.
- Include export functionality for analyzed data.
- Support additional file formats (e.g., Excel).
- Improve error handling and logging mechanisms.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
