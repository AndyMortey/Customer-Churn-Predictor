
import streamlit as st
import os
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="History Page",
    page_icon="🗓️",
    layout="wide"
)

# Load configuration for authentication
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize Streamlit authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Authenticate user and handle session states
name, authentication_status, username = authenticator.login(location="sidebar")

if st.session_state["authentication_status"]:
    authenticator.logout("Logout", location="sidebar") 

# Function to load history data
@st.cache_data(persist=True)
def load_history():
    csv_path = "Datasets/history.csv"  # Adjust the path accordingly
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if file doesn't exist

def display_history_of_all_predictions():
    st.title("Prediction History 🗓️")

    # Load history data
    history = load_history()

    if not history.empty:
        # Display filters
        st.sidebar.header("Filters")
        model_filter = st.sidebar.multiselect("Select Model Used", options=history['model_used'].unique())

        # Apply filters
        filtered_history = history.copy()
        if model_filter:
            filtered_history = filtered_history[filtered_history['model_used'].isin(model_filter)]

        # Display filtered data
        st.dataframe(filtered_history)

        # Data visualization (optional)
        st.subheader("Data Visualization")
        # Add your visualization code here as per your requirements

        # Download option
        st.subheader("Download Data")
        st.download_button(
            label="Download history as CSV",
            data=filtered_history.to_csv(index=False).encode('utf-8'),
            file_name='prediction_history.csv',
            mime='text/csv'
        )
    else:
        st.write("No history of predictions yet.")

# Run the Streamlit application
if __name__ == "__main__":
    display_history_of_all_predictions()  

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("username: customerchurn")
    st.write("password: 33333")
