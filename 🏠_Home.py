import streamlit as st
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title = "Home Page",
    page_icon="🏠",
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
name, authentication_status, username = authenticator.login("Login", "sidebar")

if st.session_state["authentication_status"]:
    authenticator.logout("Logout", "sidebar")

    # Main title and banner image
    st.title("Customer Churn Predictor")
    st.image("C:\\Users\\AndrewMore\\Downloads\\Home page.jpg", caption="", use_column_width=True)

    # Set up three columns
    col1, col2, col3 = st.columns([1, 1, 1])

    # About section
    with col1:
        st.subheader("About")
        st.write("""
        In the fast-paced world of telecommunications, where connectivity is the cornerstone of modern life, the challenge of retaining customers amidst fierce competition looms large.
        This application provides a comprehensive solution for deploying a trained model to provide an interactive web application for real-time churn prediction. 
        """)

    # Key Features section
    with col2:
        st.subheader("Key Features")
        st.markdown("""
        - **Data Extraction**: Extract data from a SQL Server database.
        - **External Data**: Option to upload and use external data files.
        - **Churn Prediction**: Predict churn based on customer data.
        - **Data Visualization**: EDA and KPIs visualization.
        - **History Page**: Record and review previous predictions.
        - **Bulk Prediction**: Predict large datasets efficiently.
        """)

    # How to Use section
    with col3:
        st.subheader("How to Use")
        st.markdown("""
        1. **Input Data**: Provide customer data such as demographics and usage.
        2. **Run Predictions**: Click 'Submit' to generate churn predictions.
        3. **Review Results**: Review predictions and take action to retain customers.
        """)

    # Additional Information
    st.subheader("Benefits to Telecom Companies")
    st.markdown("""
    - **Churn Prediction**: Identify likely churners and reduce churn.
    - **Customer Segmentation**: Targeted strategies based on churn likelihood.
    - **Retention Strategies**: Personalize offers to retain customers.
    - **Cost Savings**: Reduce acquisition costs by retaining existing customers.
    - **Customer Satisfaction**: Address needs to increase satisfaction.
    - **Competitive Advantage**: Stand out with personalized service.
    - **Data-Driven Decisions**: Make informed decisions based on insights.
    """)

    # Links section
    st.subheader("Useful Links and Information")
    st.markdown("""
    - [GitHub Repository: Customer Churn Predictor](https://github.com/AndyMortey/Customer-Churn-Predictor)
    - [GitHub Repository: A Classification Project - The Customer Churn Analysis](https://github.com/AndyMortey/A-Classification-Project-The-Customer-Churn-Analysis)
    """)

    # Navigation buttons
    st.markdown("### Navigate to Other Pages")
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    with nav_col1:
        if st.button("Predict Churn"):
            st.write("Navigate to Predict Page")  # Replace with navigation logic if available
    with nav_col2:
        if st.button("Bulk Predictions"):
            st.write("Navigate to Bulk Predictions Page")  # Replace with navigation logic if available
    with nav_col3:
        if st.button("View History"):
            st.write("Navigate to History Page")  # Replace with navigation logic if available

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("**Default Username/Password:**")
    st.write("- Username: customerchurn")
    st.write("- Password: 33333")







