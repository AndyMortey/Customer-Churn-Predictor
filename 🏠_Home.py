import streamlit as st

st.set_page_config(
    page_title = "Home Page",
    page_icon="🏠",
    layout="wide"
)

st.title("Customer Churn Predictor")
st.image("C:\\Users\\AndrewMore\\Downloads\\Home page.jpg", caption="", use_column_width=True)

st.write("This prediction app gives stakeholders the opportunity to predict if customers will churn based on some features")