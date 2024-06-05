import streamlit as st
import pyodbc
import pandas as pd

st.set_page_config(
    page_title="Customer Churn Database",
    page_icon="🧮",
    layout="wide"
)

st.title("Customer Churn Database🧮")

# Creating a DataFrame for data information
data_info = {
    "Column": ["CustomerID", "Gender", "SeniorCitizen", "Partner", "Dependents", "Tenure", 
               "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", 
               "Online Backup", "Device Protection", "Tech SUpport", "StreamingTV", "Streaming Movies", "Contract", "Paperless Billing", "Payment Method", "Montly Charges", "Total Charges", "Churn"],
    "Description": ["Unique Customer ID", "Male or Female", "0, 1, 2, 3", "Yes or No", "Yes or No", "Yes or No", "Number of Years at company", "Yes or No", 
                    "Yes or No", "Yes or No", "DSL, Fiber Optic", "Yes or No", "Yes or No", "Yes or No", "Yes or No","One Year, Month to Moth, Two years", "Yes or No", "Mailed Check, Credit card, Electronic check, Bank transfer", 
                    "Charges per month", "total charges throughout contract", "Yes or No"    
                    ]
}

df_info = pd.DataFrame(data_info)

# Displaying the DataFrame as a table
st.text("Data Features")
st.table(df_info)

## Creating a connection to the database 
## Querying the database
@st.cache_resource(show_spinner="Connecting to database...")
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )

connection = init_connection()

@st.cache_data(show_spinner="Running query...")
def running_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
    return df

def get_all_column():
    sql_query = """SELECT * FROM LP2_Telco_churn_first_3000"""
    df = running_query(sql_query)
    return df

st.markdown("<h2 style='font-size:24px;'>Full Dataset</h2>", unsafe_allow_html=True)
# Main script to display the data
df = get_all_column()
#st.write(df)
selection = st.selectbox("Select...", options=["All columns", "Numerical columns", "Categorical columns"])

# Define numerical and categorical columns
numerical_columns = ["tenure", "MonthlyCharges", "TotalCharges"]
categorical_columns = ["customerID", "gender", "Partner", "SeniorCitizen","Dependents", "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", 
                       "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", 
                       "PaymentMethod", "Churn"]

# Filter the DataFrame based on user selection
if selection == "Numerical columns":
    df_filtered = df[numerical_columns]
elif selection == "Categorical columns":
    df_filtered = df[categorical_columns]
else:
    df_filtered = df


st.write(df_filtered)