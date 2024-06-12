import streamlit as st
import os
import joblib
import pandas as pd
import numpy as np
import datetime
import time
from sklearn.preprocessing import OneHotEncoder

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
@st.cache_resource
def load_log():
    log_reg = joblib.load('./Models/best_LR_model_and_threshold.pkl')  # Load logistic regression model
    return log_reg

@st.cache_resource
def load_tool():
    encoder = joblib.load('./Models/encoder.joblib')  # Load encoder
    return encoder

def model_pick():
    column1, column2 = st.columns(2)
    with column1:
        st.selectbox(label='**Select the best predictor.**', options=['Logistic Regression'], key='predictor_main')

def feature_inputs():
    st.write('**Provide the following details.**')

    with st.form('Customer_information'):
        column1, column2, column3, column4, column5 = st.columns(5)
        with column1:
            st.write('##### **Personal Details**')
            st.number_input('Enter your age', key='age', min_value=18, max_value=65, step=1)
            st.number_input('SeniorCitizen [Yes = 1 and No = 0]:', min_value=0, max_value=1, step=1, key='senior_citizen')
            st.selectbox('Partner:', options=['Yes', 'No'], key='partner')
            st.selectbox('Dependents:', options=['Yes', 'No'], key='dependents')

        with column2:
            st.write('##### **Products And Services**')
            st.selectbox('TechSupport:', options=['Yes', 'No', 'No Internet Service'], key='tech_support')
            st.selectbox('PhoneService:', options=['Yes', 'No'], key='phone_service')
            st.selectbox('MultipleLines:', options=['Yes', 'No', 'No Phone Service'], key='multiple_lines')
            st.selectbox('InternetService:', options=['DSL', 'Fiber Optic', 'No'], key='internet_service')
            st.selectbox('DeviceProtection:', options=['Yes', 'No', 'No Internet Service'], key='device_protection')

        with column3:
            st.write('##### **Online Services**')
            st.selectbox('OnlineSecurity:', options=['Yes', 'No', 'No Internet Service'], key='online_security')
            st.selectbox('OnlineBackup:', options=['Yes', 'No', 'No Internet Service'], key='online_backup')
            st.selectbox('StreamingTv:', options=['Yes', 'No', 'No Internet Service'], key='streaming_tv')
            st.selectbox('StreamingMovies:', options=['Yes', 'No', 'No Internet Service'], key='streaming_movies')

        with column4:
            st.write('##### **Contract And Billing**')
            st.selectbox('Contract:', options=['Month-to-month', 'One year', 'Two years'], key='contract')
            st.selectbox('PaperlessBilling:', options=['Yes', 'No'], key='paperless_billing')
            st.selectbox('PaymentMethod:', options=['Mailed check', 'Electronic check', 'Bank transfer (automatic)', 'Credit card (automatic)'], key='payment_method')

        with column5:
            st.write('##### **Financials**')
            st.number_input('Tenure:', min_value=1, max_value=100, step=1, key='tenure')
            st.number_input('MonthlyCharges:', key='monthly_charges')
            st.number_input('TotalCharges:', key='total_charges')

        global submit
        submit = st.form_submit_button(label='Predict', on_click=input_save)

def input_save():
    age = st.session_state['age']
    senior_citizen = st.session_state['senior_citizen']
    partner = st.session_state['partner']
    dependents = st.session_state['dependents']
    tenure = st.session_state['tenure']
    phone_service = st.session_state['phone_service']
    multiple_lines = st.session_state['multiple_lines']
    internet_service = st.session_state['internet_service']
    online_security = st.session_state['online_security']
    online_backup = st.session_state['online_backup']
    device_protection = st.session_state['device_protection']
    tech_support = st.session_state['tech_support']
    streaming_tv = st.session_state['streaming_tv']
    streaming_movies = st.session_state['streaming_movies']
    contract = st.session_state['contract']
    paperless_billing = st.session_state['paperless_billing']
    payment_method = st.session_state['payment_method']
    monthly_charges = st.session_state['monthly_charges']
    total_charges = st.session_state['total_charges']
    
    # Save inputs to history.csv
    test_data = [age, senior_citizen, partner, dependents, tenure, phone_service, multiple_lines, internet_service, online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies, contract, paperless_billing, payment_method, monthly_charges, total_charges]
    test_df = pd.DataFrame([test_data], columns=['age', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges'])

    # Save DataFrame to history.csv
    test_df.to_csv('./history.csv', mode='a', header=not os.path.exists('./history.csv'), index=False)

def predict_and_display():
    log_reg = load_log()
    encoder = load_tool()

    if 'make_predictions' not in st.session_state:
        st.session_state['make_predictions'] = None 
    if 'churn_probability' not in st.session_state:
        st.session_state['churn_probability'] = None

    if st.session_state['predictor_main'] == 'Logistic Regression':
        # Prepare test data for prediction
        age = st.session_state['age']
        senior_citizen = st.session_state['senior_citizen']
        partner = st.session_state['partner']
        dependents = st.session_state['dependents']
        tenure = st.session_state['tenure']
        phone_service = st.session_state['phone_service']
        multiple_lines = st.session_state['multiple_lines']
        internet_service = st.session_state['internet_service']
        online_security = st.session_state['online_security']
        online_backup = st.session_state['online_backup']
        device_protection = st.session_state['device_protection']
        tech_support = st.session_state['tech_support']
        streaming_tv = st.session_state['streaming_tv']
        streaming_movies = st.session_state['streaming_movies']
        contract = st.session_state['contract']
        paperless_billing = st.session_state['paperless_billing']
        payment_method = st.session_state['payment_method']
        monthly_charges = st.session_state['monthly_charges']
        total_charges = st.session_state['total_charges']
        
        test_data = [[age, senior_citizen, partner, dependents, tenure, phone_service, multiple_lines, internet_service, online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies, contract, paperless_billing, payment_method, monthly_charges, total_charges]]
        test_df = pd.DataFrame(test_data, columns=['age', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges'])

        # Apply LabelEncoder to categorical columns
        encoded_categories_df = pd.DataFrame()

        categorical_cols = ['Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']

        for col in categorical_cols:
            encoded_categories = encoder.transform(test_df[col])
            encoded_df = pd.DataFrame(encoded_categories, columns=[f'{col}_encoded'])
            encoded_categories_df = pd.concat([encoded_categories_df, encoded_df], axis=1)

        # Concatenate encoded columns with the numerical columns
        numerical_cols = ['age', 'SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']
        test_df = pd.concat([encoded_categories_df, test_df[numerical_cols].reset_index(drop=True)], axis=1)

        # Make prediction
        prediction_probabilities = log_reg.predict_proba(test_df)
        churn_probability = prediction_probabilities[0][1]
        make_predictions = log_reg.predict(test_df)

        st.session_state['make_predictions'] = make_predictions[0]
        st.session_state['churn_probability'] = churn_probability

        display_results()

def display_results():
    col6, col7 = st.columns(2)
    prediction = st.session_state['make_predictions']
    probability = st.session_state['churn_probability']
    
    with col6:
        st.write(f'Prediction: {prediction}')

    with col7:
        if prediction == 1:  # Assuming 1 indicates churn
            st.write(f'This customer will churn with a probability of {probability * 100:.2f}%')
        else:
            st.write(f'This customer will not churn with a probability of {probability * 100:.2f}%')

if __name__ == "__main__":
    load_log()
    load_tool()
    model_pick()
    feature_inputs()
    
    if 'submit' in globals() and submit:
        input_save()
        predict_and_display()
