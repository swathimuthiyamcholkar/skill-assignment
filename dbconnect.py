import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# -------------------------------
# 1. CONNECT TO SQL SERVER
# -------------------------------
def connect_to_sql_server(server, database, username, password, trusted_connection=False):
    """
    Connects to an MS SQL Server database.

    Args:
        server (str): The SQL Server instance name or IP.
        database (str): The name of the database to connect to.
        username (str): The username for SQL Server authentication.
        password (str): The password for SQL Server authentication.
        trusted_connection (bool): Set to True for Windows authentication.

    Returns:
        pyodbc.Connection: A database connection object, or None if connection fails.
    """
    try:
        if trusted_connection:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                "Trusted_Connection=yes;"
            )
        else:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password};"
            )

        cnxn = pyodbc.connect(conn_str)
        print("Connection to SQL Server successful!")
        return cnxn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Error connecting to SQL Server: {sqlstate}")
        return None

if __name__ == "__main__":
    # --- Configuration for your SQL Server ---
    # !! IMPORTANT: Replace with your actual SQL Server details !!
    SQL_SERVER = ".\\SQLEXPRESS" # e.g., "localhost", "192.168.1.10", "SERVERNAME\SQLEXPRESS"
    DATABASE = "online_retail"
    
    # Choose one authentication method:

    # 1. SQL Server Authentication
    USERNAME = "swathi"
    PASSWORD = "$wathi@04"
    TRUSTED_CONNECTION = False

    # 2. Windows Authentication (uncomment below and comment out SQL Server Auth if using this)
    # USERNAME = "" # Not needed for Windows Auth
    # PASSWORD = "" # Not needed for Windows Auth
    # TRUSTED_CONNECTION = True
    
    db_connection = connect_to_sql_server(SQL_SERVER, DATABASE, USERNAME, PASSWORD, TRUSTED_CONNECTION)

    if db_connection:
        try:
            cursor = db_connection.cursor()
            # -------------------------------
            # 2. LOAD DATA INTO PANDAS
            # -------------------------------

            # Example: Execute a SELECT query
            print("\nExecuting a sample query...")
            #cursor.execute("SELECT @@VERSION AS 'SQL Server Version'")
            cursor.execute("SELECT * FROM [dbo].[onlineretail] WHERE Quantity > 0")  # Replace with your actual table name
            #row = cursor.fetchall()
            df = pd.DataFrame.from_records(
            cursor.fetchall(),
            columns=[col[0] for col in cursor.description]
            )
            print(df)
            # for row in cursor.fetchall():
            #  print(row)

            # Create Revenue column
            df['Revenue'] = df['Quantity'] * df['UnitPrice']

            # Convert InvoiceDate to datetime
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

            # Extract Year-Month
            df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')

            # -------------------------------
            # 3. TOTAL REVENUE OVER TIME
            # -------------------------------

            revenue_over_time = df.groupby('YearMonth')['Revenue'].sum().reset_index()
            revenue_over_time['YearMonth'] = revenue_over_time['YearMonth'].astype(str)

            plt.figure(figsize=(12,6))
            sns.lineplot(data=revenue_over_time, x='YearMonth', y='Revenue')
            plt.xticks(rotation=45)
            plt.title("Total Revenue Over Time")
            plt.tight_layout()
            plt.show()

            # -------------------------------
            # 4. TOP 10 BEST-SELLING PRODUCTS
            # -------------------------------

            top_products = (
                df.groupby('Description')['Quantity']
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            plt.figure(figsize=(10,6))
            sns.barplot(data=top_products, y='Description', x='Quantity')
            plt.title("Top 10 Best-Selling Products")
            plt.tight_layout()
            plt.show()

            # -------------------------------
            # 5. MONTHLY SALES TREND
            # -------------------------------

            monthly_sales = (
                df.groupby('YearMonth')['Revenue']
                .sum()
                .reset_index()
            )

            monthly_sales['YearMonth'] = monthly_sales['YearMonth'].astype(str)

            plt.figure(figsize=(12,6))
            sns.lineplot(data=monthly_sales, x='YearMonth', y='Revenue')
            plt.xticks(rotation=45)
            plt.title("Monthly Sales Trend")
            plt.tight_layout()
            plt.show()

       
            # -------------------------------
            # 6. TOP CUSTOMER SEGMENTS
            # -------------------------------

            customer_spending = (
                df.groupby('CustomerID')['Revenue']
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            plt.figure(figsize=(10,6))
            sns.barplot(data=customer_spending, x='CustomerID', y='Revenue')
            plt.title("Top 10 Customers by Spending")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()


            # -------------------------------
            # 7. SALES DISTRIBUTION BY COUNTRY
            # -------------------------------

            country_sales = (
                df.groupby('Country')['Revenue']
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            plt.figure(figsize=(10,6))
            sns.barplot(data=country_sales, x='Revenue', y='Country')
            plt.title("Top Countries by Sales")
            plt.tight_layout()
            plt.show()

            #DASHBOARD FEATURES (if using Streamlit or similar)

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Error during query execution: {sqlstate}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            db_connection.close()
            print("Database connection closed.")
