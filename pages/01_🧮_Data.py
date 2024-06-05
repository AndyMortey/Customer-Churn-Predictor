import streamlit as st
import pyodbc
import pandas as pd
import _thread 
import weakref
from sqlalchemy import create_engine

st.set_page_config(
    page_title= 'Data Page',
    page_icon= '🧮',
    layout= 'wide'
)

st.title('Customer Churn Database 🧮')

#Create a connection with database
#Query the database
# Custom hash function for weakref.WeakMethod objects
def hash_weakref_WeakMethod(obj):
    return hash(obj.__self__) 

# Database connection string
connection_str = (
    f"mssql+pyodbc://{st.secrets['username']}:{st.secrets['password']}@"
    f"{st.secrets['server']}/{st.secrets['database']}?driver=ODBC+Driver+17+for+SQL+Server"
)

# Create SQLAlchemy engine
engine = create_engine(connection_str)

def get_columns(column_type):
    if column_type == 'Numerical Columns':
        # Replace 'numerical_columns' with your actual numerical columns
        numerical_columns = ['column1', 'column2', 'column3']
        sql_query = f"SELECT {', '.join(numerical_columns)} FROM dbo.LP2_Telco_churn_first_3000"
    elif column_type == 'Categorical Columns':
        # Replace 'categorical_columns' with your actual categorical columns
        categorical_columns = ['column4', 'column5', 'column6']
        sql_query = f"SELECT {', '.join(categorical_columns)} FROM dbo.LP2_Telco_churn_first_3000"
    else:
        sql_query = "SELECT * FROM dbo.LP2_Telco_churn_first_3000"
    df = pd.read_sql(sql_query, engine)
    return df

def show_columns(column_type):
    df = get_columns(column_type)
    st.write(df)

selected_option = st.selectbox('Select..', options=['All Columns', 'Numerical Columns', 'Categorical Columns'])

if selected_option == 'All Columns':
    show_columns(selected_option)
elif selected_option == 'Numerical Columns':
    show_columns(selected_option)
elif selected_option == 'Categorical Columns':
    show_columns(selected_option)
