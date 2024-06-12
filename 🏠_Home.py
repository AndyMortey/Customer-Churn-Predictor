import streamlit as st

st.set_page_config(
    page_title = "Home Page",
    page_icon="🏠",
    layout="wide"
)

st.title("Customer Churn Predictor")
st.image("C:\\Users\\AndrewMore\\Downloads\\Home page.jpg", caption="", use_column_width=True)


st.write("This prediction app gives stakeholders the opportunity to predict if customers will churn based on some features")

def detail():        
    col1, col2, col3 = st.columns([1,2,2])
    with col1:
        st.subheader('🎯Info:')
        st.markdown('- Customer churn refers to the rate at which customers stop doing business with a company. dataset typically includes customer information, behavior, and usage patterns leading up to their decision to leave.')
        st.markdown('- The Dataset has **21 columns**.')
        st.markdown('- **3** numerical columns')            
        st.markdown('- **5** boolean features')              
        st.markdown('- **13** object features')
    with col2:
        st.markdown('''### 📚Columns Description:
- **Gender** - Specifies the sex of the customer
- **SeniorCitizen** - Specifies if the customer is a senior citizen or not
- **Partner** - Specifies whether the customer has a partner or not
- **Dependents** - Specifies whether the customer has dependents or not
- **Tenure** -  Duration of subscription in months
- **Phone Service** - if the customer has a phone service or not
- **MultipleLines** - If the customer has multiple lines or not
- **InternetService** - Customer's internet service provider 
- **OnlineSecurity** - If the customer has online security or not
- **OnlineBackup** - If the customer has online backup or not.''') 

    with col3:
        st.subheader('')
        st.subheader('')
        st.markdown('''
- **DeviceProtection** - If the customer has device protection or not
- **TechSupport** - If the customer has tech support or not
- **StreamingTV** - Whether the customer has streaming TV or not
- **StreamingMovies** - Whether the customer has streaming movies or not
- **Contract** - The contract term of the customer
- **PaperlessBilling** - Whether the customer has paperless billing or not
- **Payment Method** - The customer's payment method
- **MonthlyCharges** - Monthly charges to the customer 
- **TotalCharges** - Total amount charged to the customer
- **Churn** - Whether the customer churned or not. ''')
