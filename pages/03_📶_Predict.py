import streamlit as st
import os
import joblib
import pandas as pd
import numpy as np
import datetime

st.set_page_config(
    page_title="Prediction Page",
    page_icon="📊",
    layout="wide"
)

st.title("Customer Churn Prediction 📶")

# Cache model loading
@st.cache_resource(show_spinner="Loading Logistic Regression model...")
def load_logistic_pipeline():
    try:
        return joblib.load('./Models/LR_Pipeline.joblib')
    except Exception as e:
        st.error(f"Error loading Logistic Regression model: {e}")
        return None

@st.cache_resource(show_spinner="Loading Gradient Boosting model...")
def load_gradient_pipeline():
    try:
        return joblib.load('./Models/GB_Pipeline.joblib')
    except Exception as e:
        st.error(f"Error loading Gradient Boosting model: {e}")
        return None

def select_model():
    column1, column2 = st.columns(2)
    with column1:
        model_choice = st.selectbox(
            label='**Select the best predictor.**',
            options=['Logistic Regression', 'Gradient Boosting'],
            key='predictor_main'
        )
        st.success("Model selected successfully")
    
    log_pipeline = load_logistic_pipeline()
    grad_pipeline = load_gradient_pipeline()
    
    if model_choice == 'Logistic Regression':
        return log_pipeline
    else:
        return grad_pipeline

def make_prediction(pipeline):
    if not pipeline:
        st.error("No model selected or failed to load.")
        return
    
    data = {
        "gender": st.session_state["gender"],
        "seniorcitizen": st.session_state["senior_citizen"],
        "partner": st.session_state["partner"],
        "dependents": st.session_state["dependents"],
        "tenure": st.session_state["tenure"],
        "phoneservice": st.session_state["phone_service"],
        "multiplelines": st.session_state["multiple_lines"],
        "internetservice": st.session_state["internet_service"],
        "onlinesecurity": st.session_state["online_security"],
        "onlinebackup": st.session_state["online_backup"],
        "deviceprotection": st.session_state["device_protection"],
        "techsupport": st.session_state["tech_support"],
        "streamingtv": st.session_state["streaming_tv"],
        "streamingmovies": st.session_state["streaming_movies"],
        "contract": st.session_state["contract"],
        "paperlessbilling": st.session_state["paperless_billing"],
        "paymentmethod": st.session_state["payment_method"],
        "monthlycharges": st.session_state["monthly_charges"],
        "totalcharges": st.session_state["total_charges"]
    }
    
    df = pd.DataFrame([data])
    
    try:
        pred = pipeline.predict(df)
        probability = pipeline.predict_proba(df)[0]
        
        st.session_state["prediction"] = "Yes" if pred[0] == 1 else "No"
        st.session_state["probability"] = probability
        
        # Log to CSV
        df['Prediction Time'] = datetime.date.today()
        df['Model Used'] = st.session_state['predictor_main']
        df['Prediction'] = st.session_state["prediction"]
        df.to_csv('Datasets/history.csv', mode='a', header=not os.path.exists('Datasets/history.csv'), index=False)
        
        st.write("Prediction:")
        st.write(df)
        
    except Exception as e:
        st.error(f"Error making prediction: {e}")

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
            st.selectbox("Are you subcribed to streaming TV?", options=["Yes", "No"], key="streaming_tv")
            st.selectbox("Are you subscribed to movie streaming?", options=["Yes", "No"], key="streaming_movies")
            st.selectbox("What is your contract duration?", options=['Month-to-month', 'One year', 'Two year'], key="contract")
            st.selectbox("Do you use paperless billing?", options=["Yes", "No"], key="paperless_billing")
            st.selectbox("What payment method do you use?", options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], key="payment_method")
            st.slider("What is your monthly charge?", min_value=18, max_value=119, key="monthly_charges")
            st.slider("What is your total charge?", min_value=18, max_value=8672, key="total_charges")

        st.form_submit_button("Submit", on_click=make_prediction, kwargs=dict(pipeline=pipeline))

# Initialize session state for prediction and probability
if "prediction" not in st.session_state:
    st.session_state["prediction"] = None
if "probability" not in st.session_state:
    st.session_state["probability"] = None

# Run the Streamlit app
if __name__ == "__main__":
    display_form()

    if st.session_state["prediction"] is not None:
        st.divider()
        prediction = st.session_state["prediction"]
        probability = st.session_state["probability"]
        st.write(f"Prediction: {prediction}")
        st.write(f"Probability: {probability[1] * 100:.2f}%")
        
        if prediction == "Yes": 
            st.error("This customer is likely to churn.")
        else:
            st.success("This customer is not likely to churn.")
        
        st.markdown(f"#### Probability of Churn: {probability[1] * 100:.2f}%")
        st.progress(probability[1])



