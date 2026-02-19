#pip install pandas sqlalchemy pyodbc streamlit plotly dash

import pandas as pd
from sqlalchemy import create_engine

# Replace with your credentials
server = '.\\SQLEXPRESS'
database = 'online_retail'
username = 'swathi'
password = '$wathi@04'

connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
print("connection string :: " , connection_string)
engine = create_engine(connection_string)

query = "SELECT * FROM OnlineRetail;"
df = pd.read_sql(query, engine)

print(df.head())
