import streamlit as st
import os
import joblib
import pandas as pd
import numpy as np
import datetime
import time

st.set_page_config(
    page_title = "Prediction Page",
    page_icon="📊",
    layout="wide"
)

st.title("Customer Churn Prediction📶")

#load prediction model
#Cache churn prediction model
#Load logistic regression model and encoder
# Cache loading functions for model and encoder
# Cache model and encoder loading
# Load models with caching
@st.cache_resource
def load_logistic_pipeline():
    return joblib.load('./Models/Logistic_Regression_Pipeline.joblib')

@st.cache_resource
def load_gradient_pipeline():
    return joblib.load('./Models/Gradient_Boosting_Pipeline.joblib')

def select_model():
    column1, column2 = st.columns(2)
    with column1:
        model_choice = st.selectbox(
            label='**Select the best predictor.**',
            options=['Logistic Regression', 'Gradient Boosting'],
            key='predictor_main'
        )
        st.success("Model loaded successfully")
    
    log_pipeline = load_logistic_pipeline()
    grad_pipeline = load_gradient_pipeline()
    
    if model_choice == 'Logistic Regression':
        return log_pipeline
    else:
        return grad_pipeline

def make_prediction(pipeline, encoder):
    data = {
        "gender": st.session_state["gender"],
        "SeniorCitizen": st.session_state["senior_citizen"],
        "Partner": st.session_state["partner"],
        "Dependents": st.session_state["dependents"],
        "tenure": st.session_state["tenure"],
        "PhoneService": st.session_state["phone_service"],
        "MultipleLines": st.session_state["multiple_lines"],
        "InternetService": st.session_state["internet_service"],
        "OnlineSecurity": st.session_state["online_security"],
        "OnlineBackup": st.session_state["online_backup"],
        "DeviceProtection": st.session_state["device_protection"],
        "TechSupport": st.session_state["tech_support"],
        "StreamingTV": st.session_state["streaming_tv"],
        "StreamingMovies": st.session_state["streaming_movies"],
        "Contract": st.session_state["contract"],
        "PaperlessBilling": st.session_state["paperless_billing"],
        "PaymentMethod": st.session_state["payment_method"],
        "MonthlyCharges": st.session_state["monthly_charges"],
        "TotalCharges": st.session_state["total_charges"]
    }
    
    df = pd.DataFrame([data])
    
    pred = pipeline.predict(df)
    pred_int = int(pred[0])
    prediction = encoder.inverse_transform([pred_int])
    probability = pipeline.predict_proba(df)[0]
    
    st.session_state["prediction"] = prediction
    st.session_state["probability"] = probability

    # Log to CSV
    df['Prediction Time'] = datetime.date.today()
    df['Model Used'] = st.session_state['predictor_main']
    df.to_csv('./history.csv', mode='a', header=not os.path.exists('./history.csv'), index=False)

    st.write(df)

def display_form():
    pipeline = select_model()
    
    with st.form("input-features"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("What is your Gender?", options=["Male", "Female"], key="gender")
            st.selectbox("What is your senior citizen level?", options=[0, 1], key="senior_citizen")
            st.selectbox("Do you have a Partner?", options=["Yes", "No"], key="partner")
            st.selectbox("Have you got any dependents?", options=["Yes", "No"], key="dependents")
            st.select_slider("How many years have you spent at the company?", options=range(0, 76), key="tenure")
            st.selectbox("Do you have any phone service?", options=["Yes", "No"], key="phone_service")
            st.selectbox("Have you got multiple lines?", options=["Yes", "No"], key="multiple_lines")
            st.selectbox("Do you have internet service?", options=["DSL", "Fiber Optic", "No"], key="internet_service")
            st.selectbox("Do you have Online Security?", options=["Yes", "No"], key="online_security")
        
        with col2:
            st.selectbox("Do you have online backup?", options=["Yes", "No"], key="online_backup")
            st.selectbox("Is your device protected?", options=["Yes", "No"], key="device_protection")
            st.selectbox("Do you have Tech support?", options=["Yes", "No"], key="tech_support")
            st.selectbox("Are you subcribed to streaming tv?", options=["Yes", "No"], key="streaming_tv")
            st.selectbox("Are you subscribed to movie streaming?", options=["Yes", "No"], key="streaming_movies")
            st.selectbox("What is your contract duration?", options=['Month-to-month', 'One year', 'Two year'], key="contract")
            st.selectbox("Do you use paperless billing?", options=["Yes", "No"], key="paperless_billing")
            st.selectbox("What payment method do you use?", options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], key="payment_method")
            st.slider("What is your monthly charge?", min_value=18, max_value=119, key="monthly_charges")
            st.slider("What is your total charge?", min_value=18, max_value=8672, key="total_charges")

        st.form_submit_button("Submit", on_click=make_prediction, kwargs=dict(pipeline=pipeline, encoder=encoder))

# Initialize session state for prediction and probability
if "prediction" not in st.session_state:
    st.session_state["prediction"] = None
if "probability" not in st.session_state:
    st.session_state["probability"] = None

# Run the Streamlit app
if __name__ == "__main__":
    display_form()

    final_prediction = st.session_state["prediction"]

    if final_prediction is not None:
        st.divider()
        if final_prediction[0] == "Yes": 
            st.write(f"Prediction: {final_prediction[0]}")
            st.write(' This customer is likely to Churn')
        st.write(f"Probability: {st.session_state['probability'][1] * 100:.2f}%")
