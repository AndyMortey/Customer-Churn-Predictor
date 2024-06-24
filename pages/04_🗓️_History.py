import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="History Page",
    page_icon="📊",
    layout="wide"
)

st.title("Customer Churn History🗓️")

# Function to show the history of predictions
def show_history():
    csv_path = 'Datasets/history.csv'
    # Check if the CSV file exists
    if os.path.exists(csv_path):
        history_df = pd.read_csv(csv_path)
        # Map the numeric predictions to readable outcomes
        history_df['PredictedOutcome'] = history_df['PredictedOutcome'].map({0: 'Not Churned', 1: 'Churned'})
        st.dataframe(history_df)
    else:
        st.write("No predictions have been made yet.")

if __name__ == "__main__":
    show_history()