# #821160 - SQL Database Analysis & Dashboard Creation

# SQL Server Analysis Dashboard with Streamlit
# streamlit run d:/src/821160-sqldbanalysis.py

import streamlit as st
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Online Retail Dashboard", layout="wide")
st.title("📊 Online Retail Sales Dashboard")


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


def load_data_from_sql(db_connection):    
    #if db_connection:
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
               # Data Cleaning
            df = df.dropna(subset=['CustomerID', 'Description'])
            df = df[df['UnitPrice'] > 0]

            # Feature Engineering
            df['Revenue'] = df['Quantity'] * df['UnitPrice']
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
            df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
            return df       
            # for row in cursor.fetchall():
            #  print(row)
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Error during query execution: {sqlstate}")
            return None

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            db_connection.close()        
            print("Database connection closed.")

df = load_data_from_sql(db_connection)
print(df)

# ----------------------------
# KPI SECTION
# ----------------------------
total_revenue = df['Revenue'].sum()
total_orders = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()
avg_order_value = total_revenue / total_orders

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Total Customers", f"{total_customers:,}")
col4.metric("Avg Order Value", f"₹{avg_order_value:,.2f}")

st.markdown("---")

# ----------------------------
# MONTHLY REVENUE TREND
# ----------------------------
st.subheader("📈 Monthly Revenue Trend")

monthly_sales = df.groupby('YearMonth')['Revenue'].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(10,5))
sns.lineplot(data=monthly_sales, x='YearMonth', y='Revenue', marker='o', ax=ax1)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('₹{x:,.0f}'))
plt.tight_layout()

st.pyplot(fig1)

st.markdown("---")

# ----------------------------
# TWO COLUMN SECTION
# ----------------------------
col_left, col_right = st.columns(2)

# Top Countries
with col_left:
    st.subheader("🌍 Top 10 Countries by Revenue")

    country_sales = (
        df.groupby('Country')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2, ax2 = plt.subplots(figsize=(6,4))
    sns.barplot(data=country_sales, x='Revenue', y='Country', ax=ax2)
    ax2.xaxis.set_major_formatter(mtick.StrMethodFormatter('₹{x:,.0f}'))
    plt.tight_layout()

    st.pyplot(fig2)

# Top Products
with col_right:
    st.subheader("🛍 Top 10 Best-Selling Products")

    top_products = (
        df.groupby('Description')['Quantity']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3, ax3 = plt.subplots(figsize=(6,4))
    sns.barplot(data=top_products, x='Quantity', y='Description', ax=ax3)
    plt.tight_layout()

    st.pyplot(fig3)

st.markdown("---")

# ----------------------------
# TOP CUSTOMERS
# ----------------------------
st.subheader("👑 Top 10 Customers by Spending")

customer_spending = (
    df.groupby('CustomerID')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4, ax4 = plt.subplots(figsize=(10,5))
sns.barplot(data=customer_spending, x='CustomerID', y='Revenue', ax=ax4)
ax4.yaxis.set_major_formatter(mtick.StrMethodFormatter('₹{x:,.0f}'))
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig4)


