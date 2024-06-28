import streamlit as st
import joblib
import pandas as pd
import os
import datetime
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Set Streamlit page configuration
st.set_page_config(
    page_title="Prediction Page",
    page_icon="📊",
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
    authenticator.logout("Logout", "sidebar") 
    st.title("Customer Churn Prediction")

    # Load trained models
    @st.cache_resource
    def load_LR_pipeline():
        return joblib.load("Models/LR_Pipeline.joblib")

    @st.cache_resource
    def load_GB_pipeline():
        return joblib.load("Models/GB_Pipeline.joblib")

    # Function to select model based on user choice
    def select_model():
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            user_choice = st.selectbox("Select a model to use", options=["Gradient Boosting🚀", "Logistic Regression🛸"])

        # Display metrics based on selected model
        with col2: 
            if user_choice == "Gradient Boosting🚀":
                st.metric(label="Precision🎯✨", value="81%")
            else: 
                st.metric(label="Precision🎯✨", value="82.4%")

        with col3:
            if user_choice == "Gradient Boosting🚀":
                st.metric(label="F1_score⚖️", value="77.5%")
            else: 
                st.metric(label="F1_score⚖️", value="77%")

        with col4: 
            if user_choice == "Gradient Boosting🚀":
                st.metric(label="Optimal Threshold🎚️", value="0.024")
            else:
                st.metric(label="Optimal Threshold🎚️", value="0.284")

        return user_choice

    # Function to make predictions based on selected model and user inputs
    def make_prediction(selected_model):
        # Load the appropriate pipeline based on selected model
        if selected_model == "Gradient Boosting🚀":
            pipeline = load_GB_pipeline()
        else: 
            pipeline = load_LR_pipeline()

        # Gather user inputs
        input_data = {
            "gender": st.session_state["gender"],
            "seniorcitizen": st.session_state["seniorcitizen"],
            "partner": st.session_state["partner"],
            "dependents": st.session_state["dependents"],
            "tenure": st.session_state["tenure"],
            "phoneservice": st.session_state["phoneservice"],
            "multiplelines": st.session_state["multiplelines"],
            "internetservice": st.session_state["internetservice"],
            "onlinesecurity": st.session_state["onlinesecurity"],
            "onlinebackup": st.session_state["onlinebackup"],
            "deviceprotection": st.session_state["deviceprotection"],
            "techsupport": st.session_state["techsupport"],
            "streamingtv": st.session_state["streamingtv"],
            "streamingmovies": st.session_state["streamingmovies"],
            "contract": st.session_state["contract"],
            "paperlessbilling": st.session_state["paperlessbilling"],
            "paymentmethod": st.session_state["paymentmethod"],
            "monthlycharges": st.session_state["monthlycharges"],
            "totalcharges": st.session_state["totalcharges"]
        }

        # Create DataFrame from user inputs
        input_df = pd.DataFrame([input_data])

        # Perform prediction
        pred = pipeline.predict(input_df)
        probability = pipeline.predict_proba(input_df)

        # Store prediction details in session state
        st.session_state["prediction"] = pred[0]
        st.session_state["probability"] = probability

        # Prepare data to save to history.csv
        input_data.update({
            "prediction": "Churn" if pred[0] == 1 else "Not Churn",
            "probability": max(probability[0]),
            "time_of_prediction": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_used": selected_model
        })

        # Convert data to DataFrame
        df = pd.DataFrame([input_data])

        # Specify history.csv file path
        history_path = "Datasets/history.csv"

        # Check if directory exists, create if not
        os.makedirs(os.path.dirname(history_path), exist_ok=True)

        # Save prediction to history.csv
        df.to_csv(history_path, mode="a", header=not os.path.exists(history_path), index=False)

        return pred, probability

    # Function to display input form and process predictions
    def display_form():
        selected_model = select_model()

        with st.form("input-features"):
            col1, col2 = st.columns(2)

            # Display input fields
            with col1:
                st.selectbox("Gender", ["Male", "Female"], key="gender")
                st.select_slider("Senior Citizen", options=[0, 1], key="seniorcitizen")
                st.selectbox("Partner", ["Yes", "No"], key="partner")
                st.selectbox("Dependents", ["Yes", "No"], key="dependents")
                st.select_slider("Tenure", options=range(0, 76), key="tenure")
                st.selectbox("Phone Service", ["Yes", "No"], key="phoneservice")
                st.selectbox("Multiple Lines", ["Yes", "No"], key="multiplelines")
                st.selectbox("Internet Service", ["DSL", "Fiber Optic", "No"], key="internetservice")
                st.selectbox("Online Security", ["Yes", "No"], key="onlinesecurity")

            with col2:
                st.selectbox("Online Backup", ["Yes", "No"], key="onlinebackup")
                st.selectbox("Device Protection", ["Yes", "No"], key="deviceprotection")
                st.selectbox("Tech Support", ["Yes", "No"], key="techsupport")
                st.selectbox("Streaming TV", ["Yes", "No"], key="streamingtv")
                st.selectbox("Streaming Movies", ["Yes", "No"], key="streamingmovies")
                st.selectbox("Contract", ['Month-to-month', 'One year', 'Two year'], key="contract")
                st.selectbox("Paperless Billing", ["Yes", "No"], key="paperlessbilling")
                st.selectbox("Payment Method", [
                    'Electronic check', 'Mailed check', 'Bank transfer (automatic)',
                    'Credit card (automatic)'
                ], key="paymentmethod")
                st.slider("Monthly Charges", min_value=18, max_value=119, key="monthlycharges")
                st.slider("Total Charges", min_value=18, max_value=8672, key="totalcharges")

            # Submit button to make prediction
            st.form_submit_button("Submit", on_click=make_prediction, kwargs=dict(selected_model=selected_model))

    # Initialize session state variables
    if "prediction" not in st.session_state:
        st.session_state["prediction"] = None

    if "probability" not in st.session_state:
        st.session_state["probability"] = None

    # Run the Streamlit application
    if __name__ == "__main__":
        display_form()

        # Display prediction result
        if st.session_state["prediction"] is not None:
            st.divider()
            if st.session_state["prediction"] == 1:
                st.write(f"Prediction: Churn")
                st.write("This customer is likely to churn.")
                st.write(f"Probability of churning: {st.session_state['probability'][0][1]*100:.2f}%")
            else:
                st.write(f"Prediction: Not Churn")
                st.write("This customer is not likely to churn.")
                st.write(f"Probability of not churning: {st.session_state['probability'][0][0]*100:.2f}%")

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
else:
    st.info("Please login to access the website")
    st.write("username: customerchurn")
    st.write("password: 33333")
