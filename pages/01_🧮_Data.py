import streamlit as st
import pyodbc
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Customer Churn Database",
    page_icon="🧮",
    layout="wide"
)

st.title("Customer Churn Database 🧮")

# Data Information
data_info = {
    "Column": ["CustomerID", "Gender", "SeniorCitizen", "Partner", "Dependents", "Tenure", 
               "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", 
               "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", 
               "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn"],
    "Values": ["Unique Customer ID", "Male or Female", "0, 1", "Yes or No", "Yes or No", 
               "Number of Years at Company", "Yes or No", "Yes, No, No Phone Service", 
               "DSL, Fiber Optic, No", "Yes, No, No Internet Service", 
               "Yes, No, No Internet Service", "Yes, No, No Internet Service", 
               "Yes, No, No Internet Service", "Yes, No, No Internet Service", 
               "Yes, No, No Internet Service", "One Year, Month to Month, Two years", 
               "Yes or No", "Mailed Check, Credit Card, Electronic Check, Bank Transfer", 
               "Charges per Month", "Total Charges throughout Contract", "Yes or No"]
}

df_info = pd.DataFrame(data_info)

# Display data information
st.markdown("<h2>Data Features</h2>", unsafe_allow_html=True)
st.table(df_info)

# Database connection
@st.cache_resource(show_spinner="Connecting to database...")
def init_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
            + st.secrets["server"]
            + ";DATABASE="
            + st.secrets["database"]
            + ";UID="
            + st.secrets["username"]
            + ";PWD="
            + st.secrets["password"]
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

connection = init_connection()

@st.cache_data(show_spinner="Running query...")
def running_query(query):
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
            return df
        except Exception as e:
            st.error(f"Error running query: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()

def get_all_column():
    sql_query = "SELECT * FROM LP2_Telco_churn_first_3000"
    return running_query(sql_query)

# Main script to display data
st.markdown("<h2>Full Dataset</h2>", unsafe_allow_html=True)
df = get_all_column()

# Column selection
selection = st.selectbox("Select columns to display", options=["All columns", "Numerical columns", "Categorical columns"])

# Define numerical and categorical columns
numerical_columns = ["tenure", "MonthlyCharges", "TotalCharges"]
categorical_columns = ["gender", "Partner", "SeniorCitizen", "Dependents", "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", 
                       "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", 
                       "PaymentMethod", "Churn"]

# Filter the DataFrame based on user selection
if selection == "Numerical columns":
    df_filtered = df[numerical_columns]
elif selection == "Categorical columns":
    df_filtered = df[categorical_columns]
else:
    df_filtered = df

# Display the filtered DataFrame
st.write(df_filtered)

# Option to visualize numerical columns
if selection in ["Numerical columns", "All columns"]:
    st.markdown("<h2>Visualizations</h2>", unsafe_allow_html=True)
    for column in numerical_columns:
        st.write(f"Distribution of {column}")
        st.bar_chart(df[column])




