import streamlit as st
import joblib
import pandas as pd
import os
import datetime
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Prediction Page",
    page_icon="📊",
    layout="wide"
)

st.title("Customer Churn Prediction 📶")

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
name, authentication_status, username = authenticator.login(location="sidebar")

if st.session_state["authentication_status"]:
    authenticator.logout("Logout", "sidebar") 
    st.title("Customer Churn Prediction")

    @st.cache_resource
    def load_LR_pipeline():
        return joblib.load("Models\LR_Pipeline.joblib")

    @st.cache_resource
    def load_GB_pipeline():
        return joblib.load("Models\GB_Pipeline.joblib")

    def select_model():
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            user_choice = st.selectbox("Select a model to use", options=["Gradient Boosting🚀", "Logistic Regression🛸"], key="selected_model")
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
            
        if st.session_state["selected_model"] == "Gradient Boosting🚀":
            pipeline = load_GB_pipeline()
        else: 
            pipeline = load_LR_pipeline()

        st.success("Model loaded successfully")
        return pipeline
        

    def make_prediction(pipeline):
        data = [[
            st.session_state["gender"],
            st.session_state["senior_citizen"],
            st.session_state["partner"],
            st.session_state["dependents"],
            st.session_state["tenure"],
            st.session_state["phone_service"],
            st.session_state["multiple_lines"],
            st.session_state["internet_service"],
            st.session_state["online_security"],
            st.session_state["online_backup"],
            st.session_state["device_protection"],
            st.session_state["tech_support"],
            st.session_state["streaming_tv"],
            st.session_state["streaming_movies"],
            st.session_state["contract"],
            st.session_state["paperless_billing"],
            st.session_state["payment_method"],
            st.session_state["monthly_charges"],
            st.session_state["total_charges"]
        ]]
        
        columns = [
            "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService",
            "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
            "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
            "PaymentMethod", "MonthlyCharges", "TotalCharges"
        ]

        df = pd.DataFrame(data, columns=columns)
        pred = pipeline.predict(df)
        probability = pipeline.predict_proba(df)
        

        st.session_state["prediction"] = pred[0]
        st.session_state["probability"] = probability

        probability_of_yes = st.session_state["probability"][0][1]
        probability_of_no = st.session_state["probability"][0][0]

        df["prediction"] = pred[0]
        df["probability"] = max(probability_of_yes, probability_of_no)
        df["time_of_prediction"] = datetime.date.today()
        df["model_used"] = st.session_state["selected_model"]

        # Save to history.csv
        history_path = "Datasets\history.csv"
        df.to_csv(history_path, mode="a", header=not os.path.exists(history_path), index=False)

        return pred, probability

    def display_form():
        pipeline = select_model()

        with st.form("input-features"):
            col1, col2 = st.columns(2)
        
            with col1:
                st.selectbox("Gender", ["Male", "Female"], key="gender")
                st.select_slider("Senior Citizen", options=[0, 1], key="senior_citizen")
                st.selectbox("Partner", ["Yes", "No"], key="partner")
                st.selectbox("Dependents", ["Yes", "No"], key="dependents")
                st.select_slider("Tenure", options=range(0, 76), key="tenure")
                st.selectbox("Phone Service", ["Yes", "No"], key="phone_service")
                st.selectbox("Multiple Lines", ["Yes", "No"], key="multiple_lines")
                st.selectbox("Internet Service", ["DSL", "Fiber Optic", "No"], key="internet_service")
                st.selectbox("Online Security", ["Yes", "No"], key="online_security")
            
            with col2:
                st.selectbox("Online Backup", ["Yes", "No"], key="online_backup")
                st.selectbox("Device Protection", ["Yes", "No"], key="device_protection")
                st.selectbox("Tech Support", ["Yes", "No"], key="tech_support")
                st.selectbox("Streaming TV", ["Yes", "No"], key="streaming_tv")
                st.selectbox("Streaming Movies", ["Yes", "No"], key="streaming_movies")
                st.selectbox("Contract", ['Month-to-month', 'One year', 'Two year'], key="contract")
                st.selectbox("Paperless Billing", ["Yes", "No"], key="paperless_billing")
                st.selectbox("Payment Method", [
                    'Electronic check', 'Mailed check', 'Bank transfer (automatic)',
                    'Credit card (automatic)'
                ], key="payment_method")
                st.slider("Monthly Charges", min_value=18, max_value=119, key="monthly_charges")
                st.slider("Total Charges", min_value=18, max_value=8672, key="total_charges")

            st.form_submit_button("Submit", on_click=make_prediction, kwargs=dict(pipeline=pipeline))

    # Initialize session state for prediction and probability
    if "prediction" not in st.session_state:
        st.session_state["prediction"] = None
    if "probability" not in st.session_state:
        st.session_state["probability"] = None

    # Run the Streamlit app
    if __name__ == "__main__":
        display_form()

        # Display prediction result
        if st.session_state["prediction"] is not None:
            st.divider()
            if st.session_state["prediction"] == "Yes": 
                st.write(f"Prediction: {st.session_state['prediction']}")
                st.write("This customer is likely to churn.")
                st.write(f"Probability of churning: {st.session_state['probability'][0][1]*100:.2f}%")
            else:
                st.write(f"Prediction: {st.session_state['prediction']}")
                st.write("This customer is not likely to churn.")
                st.write(f"Probability of not churning: {st.session_state['probability'][0][0]*100:.2f}%")

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("username: customerchurn")
    st.write("password: 33333")