import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Data Page",
    page_icon="🧮",
    layout="wide"
)

# Load configuration for authentication
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Authentication
name, authentication_status, username = authenticator.login(fields=["Login"], location="sidebar")

if st.session_state["authentication_status"]:
    authenticator.logout("Logout", "sidebar")
    st.title(f"Welcome, {name}!")
    st.write("You're logged in. Navigate using the sidebar to access different sections.")

    # Example dataframe (replace with actual data)
    df = pd.read_csv('data/clean_df.csv')  # Make sure this path is correct
    df_filtered = df[['tenure', 'MonthlyCharges', 'TotalCharges']].dropna()

    # Creating histograms for each numeric column
    st.subheader("Histograms")
    for column in df_filtered.columns:
        st.write(f"Histogram for {column}")
        fig, ax = plt.subplots()
        ax.hist(df_filtered[column], bins=30, alpha=0.7, color='blue')
        ax.set_title(f'Histogram of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
        st.write(" ")

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("**Default Username/Password:**")
    st.write("- Username: customerchurn")
    st.write("- Password: 33333")



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Set page configuration
st.set_page_config(
    page_title="Customer Churn Database",
    page_icon="🧮",
    layout="wide"
)

# Load configuration for authentication
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Authentication
name, authentication_status, username = authenticator.login(fields=["Login"], location="sidebar")

if st.session_state["authentication_status"]:
    authenticator.logout("Logout", "sidebar")
    st.title(f"Welcome, {name}!")
    st.write("You're logged in. Navigate using the sidebar to access different sections.") 

    st.title("Customer Churn Database 🧮")

    # Load dataset
    df = pd.read_csv('Datasets\merged_dataset.csv')

    # Full dataset section
    st.markdown("<h2 style='font-size:24px;'>Full Dataset</h2>", unsafe_allow_html=True)

    # Dataset filtering options
    selection = st.selectbox("Select columns to display:", 
                             options=["All columns", "Numerical columns", "Categorical columns"])

    # Define numerical and categorical columns
    numerical_columns = ["tenure", "MonthlyCharges", "TotalCharges"]
    categorical_columns = ["gender", "Partner", "SeniorCitizen", "Dependents", "PhoneService", "MultipleLines", 
                           "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", 
                           "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod", "Churn"]

    # Filter the DataFrame based on user selection
    if selection == "Numerical columns":
        df_filtered = df[numerical_columns]
    elif selection == "Categorical columns":
        df_filtered = df[categorical_columns]
    else:
        df_filtered = df

    # Display filtered DataFrame
    st.dataframe(df_filtered)

    # Upload CSV file section
    st.markdown("<h2 style='font-size:24px;'>Upload CSV File</h2>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

    if uploaded_file is not None:
        uploaded_df = pd.read_csv(uploaded_file)
        
        st.write("Uploaded Data:")
        st.dataframe(uploaded_df)

        # Save uploaded file option
        if st.button("Save Uploaded Data"):
            uploaded_df.to_csv('Data/uploaded_data.csv', index=False)
            st.success("Uploaded data saved successfully.")

    # Additional Features Section
    st.markdown("<h2 style='font-size:24px;'>Additional Features</h2>", unsafe_allow_html=True)

    # Display statistical summary
    if st.checkbox("Show statistical summary"):
        st.write(df_filtered.describe())

    # Plot histograms for numerical columns
    st.subheader("Histograms")
    for column in df_filtered.columns:
        st.write(f"Histogram for {column}")
        fig, ax = plt.subplots()
        sns.histplot(df_filtered[column], bins=30, kde=False, ax=ax, color='blue')
        ax.set_title(f'Histogram of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
        st.write(" ")


    # Display correlation matrix
    if st.checkbox("Show correlation matrix"):
        st.subheader("Correlation Matrix")
        correlation_matrix = df_filtered.corr()
        st.dataframe(correlation_matrix)

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("**Default Username/Password:**")
    st.write("- username: customerchurn")
    st.write("- password: 33333")

