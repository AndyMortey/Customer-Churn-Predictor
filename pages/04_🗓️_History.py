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

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

name, authentication_status, username = authenticator.login(location="sidebar")

if st.session_state["authentication_status"]:
    authenticator.logout("Logout", location="sidebar") 

    def display_history_of_all_predictions():
        csv_path = "Datasets\history.csv"
        csv_exists = os.path.exists(csv_path)

        if csv_exists:
            history = pd.read_csv(csv_path)
            
            # Filter options
            st.sidebar.subheader("Filter Options")
            model_filter = st.sidebar.multiselect("Select Model Used", options=history['model_used'].unique())
            date_filter = st.sidebar.date_input("Select Date Range", [])
            prediction_filter = st.sidebar.selectbox("Select Prediction", options=["All", "Yes", "No"], index=0)

            # Apply filters
            if model_filter:
                history = history[history['model_used'].isin(model_filter)]
            if date_filter:
                if len(date_filter) == 2:
                    start_date, end_date = date_filter
                    history = history[(pd.to_datetime(history['time_of_prediction']) >= pd.to_datetime(start_date)) &
                                      (pd.to_datetime(history['time_of_prediction']) <= pd.to_datetime(end_date))]
            if prediction_filter != "All":
                history = history[history['prediction'] == prediction_filter]
            
            st.write("### Prediction History")
            st.dataframe(history)

            # Data visualization
            st.write("### Data Visualization")
            if not history.empty:
                st.bar_chart(history['model_used'].value_counts())
                st.line_chart(history.groupby('time_of_prediction').size())

            # Download option
            st.write("### Download Data")
            st.download_button(
                label="Download history as CSV",
                data=history.to_csv(index=False).encode('utf-8'),
                file_name='prediction_history.csv',
                mime='text/csv'
            )
        else:
            st.write("No history of predictions yet.")

    if __name__ == "__main__":
        st.title("Prediction History")
        display_history_of_all_predictions()

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("username: customerchurn")
    st.write("password: 33333")
