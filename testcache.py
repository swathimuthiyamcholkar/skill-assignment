import streamlit as st
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Online Retail Dashboard", layout="wide")

st.title("📊 Online Retail Sales Dashboard")

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
def connect_to_sql():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=.\\SQLEXPRESS;"
        "DATABASE=online_retail;"
        "UID=swathi;"
        "PWD=$wathi@04;"
    )
    return pyodbc.connect(conn_str)

@st.cache_data
def load_data():
    conn = connect_to_sql()
    query = "SELECT * FROM dbo.onlineretail WHERE Quantity > 0"
    df = pd.read_sql(query, conn)
    conn.close()

    # Data Cleaning
    df = df.dropna(subset=['CustomerID', 'Description'])
    df = df[df['UnitPrice'] > 0]

    # Feature Engineering
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)

    return df

df = load_data()

# ----------------------------
# KPI SECTION
# ----------------------------
total_revenue = df['Revenue'].sum()
total_orders = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()
avg_order_value = total_revenue / total_orders

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"£{total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Total Customers", f"{total_customers:,}")
col4.metric("Avg Order Value", f"£{avg_order_value:,.2f}")

st.markdown("---")

# ----------------------------
# MONTHLY REVENUE TREND
# ----------------------------
st.subheader("📈 Monthly Revenue Trend")

monthly_sales = df.groupby('YearMonth')['Revenue'].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(10,5))
sns.lineplot(data=monthly_sales, x='YearMonth', y='Revenue', marker='o', ax=ax1)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('£{x:,.0f}'))
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
    ax2.xaxis.set_major_formatter(mtick.StrMethodFormatter('£{x:,.0f}'))
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
ax4.yaxis.set_major_formatter(mtick.StrMethodFormatter('£{x:,.0f}'))
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig4)
