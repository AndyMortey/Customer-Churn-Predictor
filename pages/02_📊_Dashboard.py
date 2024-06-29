import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title = "Dashboard Page",
    page_icon="📊",
    layout="wide"
)
st.title("Customer Churn Dashboard")
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

    df = pd.read_csv('Datasets/merged_dataset.csv')
    df.dropna(inplace=True)

    dashboard_selection = st.sidebar.selectbox("Select Dashboard", ['EDA Dashboard', 'KPI Dashboard'])

    selected_gender = st.sidebar.selectbox("Select Gender", ['All'] + df['gender'].unique().tolist())
    selected_churn = st.sidebar.selectbox("Select Churn Status", ['All'] + df['churn'].unique().tolist())
    selected_contract = st.sidebar.selectbox("Select Contract Type", ['All'] + df['contract'].unique().tolist())
    selected_tenure = st.sidebar.slider("Select Tenure Range", int(df['tenure'].min()), int(df['tenure'].max()), (int(df['tenure'].min()), int(df['tenure'].max())))

    filtered_df = df.copy()
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
    if selected_churn != 'All':
        filtered_df = filtered_df[filtered_df['churn'] == selected_churn]
    if selected_contract != 'All':
        filtered_df = filtered_df[filtered_df['contract'] == selected_contract]
    if selected_tenure:
        filtered_df = filtered_df[(filtered_df['tenure'] >= selected_tenure[0]) & (filtered_df['tenure'] <= selected_tenure[1])]

    palette_dict = {False: "grey", True: "brown", "Yes": "brown", "No": "grey"}

    if dashboard_selection == 'EDA Dashboard':
        st.subheader("Exploratory Data Analysis (EDA) Dashboard")
        st.write("Welcome to the Customer Churn Dashboard! 📊 Explore insightful visualizations and uncover trends in customer churn and behavior. Use the filters to dive deeper into contract types, gender distribution, and more. Let's discover valuable insights together! 📊")

        fig, ax = plt.subplots(figsize=(5, 3))
        sns.countplot(data=filtered_df, x="contract", hue="churn", palette=palette_dict, ax=ax)
        ax.set_title('Contract Type by Churn', fontsize=10)
        ax.set_xlabel('Contract Type', fontsize=8)
        ax.set_ylabel('Count', fontsize=8)
        st.pyplot(fig)
        st.write(" ")

        col1, col2 = st.columns(2)
        with col1:
            fig1, ax1 = plt.subplots()
            churn_counts = filtered_df['churn'].value_counts()
            explode = tuple([0.05] * len(churn_counts))
            ax1.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', explode=explode, colors=['brown', 'grey'])
            ax1.set_title('Churn Distribution', fontsize=10)
            st.pyplot(fig1)
            st.write(" ")

            fig4, ax4 = plt.subplots()
            sns.countplot(data=df, x="seniorcitizen", hue="churn", palette={"No": "grey", "Yes": "Brown"}, ax=ax4)
            ax4.set_title('Churn by Senior Citizen', fontsize=10)
            ax4.set_xlabel('Senior Citizen', fontsize=8)
            ax4.set_ylabel('Count', fontsize=8)
            st.pyplot(fig4)

        with col2:
            fig2, ax2 = plt.subplots()
            gender_churn_counts = filtered_df.groupby("gender")["churn"].value_counts().unstack().fillna(0)
            gender_churn_counts.plot(kind='bar', stacked=True, ax=ax2, color=['brown','grey'])
            ax2.set_title('Churn Distribution by Gender', fontsize=10)
            ax2.set_xlabel('Gender', fontsize=8)
            ax2.set_ylabel('Count', fontsize=8)
            st.pyplot(fig2)

            fig3, ax3 = plt.subplots()
            sns.countplot(data=df, x="paymentmethod", hue="churn", palette={"No": "grey", "Yes": "brown"}, ax=ax3)
            ax3.set_title('Payment Method Distribution by Churn', fontsize=10)
            ax3.set_xlabel('Payment Method', fontsize=8)
            ax3.set_ylabel('Count', fontsize=8)
            plt.xticks(rotation=45)
            st.pyplot(fig3)

        st.write(" ")
        st.write("### Correlation Heatmap")
        numeric_cols = df.select_dtypes(include=["int", "float"])
        corr_matrix = numeric_cols.corr()
        fig5, ax5 = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", square=True, ax=ax5)
        ax5.set_title("Correlation of Numerical Columns", fontsize=12)
        st.pyplot(fig5)

        st.write("### Histograms for Numerical Features")
        num_features = ['tenure', 'monthlycharges', 'totalcharges']
        fig6, axs = plt.subplots(1, len(num_features), figsize=(15, 5))
        for i, feature in enumerate(num_features):
            sns.histplot(filtered_df[feature], kde=True, ax=axs[i], color='brown')
            axs[i].set_title(f'Histogram of {feature}', fontsize=10)
            axs[i].set_xlabel(feature, fontsize=8)
            axs[i].set_ylabel('Frequency', fontsize=8)
        st.pyplot(fig6)

    else:
        st.subheader("Key Performance Indicators (KPI) Dashboard")
        st.write("This KPI Dashboard provides a comprehensive overview of the model's performance. It includes confusion matrices, ROC curves, and analyses of threshold effects. By fine-tuning these thresholds, we aim to enhance the model's ability to accurately predict the number of customers likely to churn, thereby improving overall prediction accuracy and business decision-making.")

        col3, col4, col5, col6 = st.columns(4)
        with col3: 
            st.write("###### Gradient Boosting Metrics🚀✨")
            st.metric(label= "Precision🎯✨", value="81%" )
        with col4:
            st.write("")
            st.write("")
            st.metric(label="F1 Score⚖️", value="77%")
        with col5:
            st.write("##### Logistic Regression Metrics🛸")
            st.metric(label= "Precision🎯✨", value="82.4%" )
        with col6:
            st.write("")
            st.write(" ")
            st.metric(label = "F1 Score⚖️", value="76.9%")

        image = Image.open("assets/ROC Curve.png")
        st.image(image, caption="ROC Curve", use_column_width=True)

        st.write("### Confusion Matrices")
        col1, col2 = st.columns(2)
        with col1:
            image1 = Image.open('assets/Confusion Matrix LR.png')
            st.image(image1, caption="Logistic Regression", use_column_width=True)
        with col2:
            image3 = Image.open('assets/Confusion Matrix GB.png')
            st.image(image3, caption="Gradient Boosting", use_column_width=True)

        st.write("#### Confusion Matrices after Tuning")
        col7, col8 = st.columns(2)
        with col7:
            image1 = Image.open('assets/Confusion Matrix Tuned LR.png')
            st.image(image1, caption="Logistic Regression @ LR_threshold = 0.22", use_column_width=True)
        with col8:
            image3 = Image.open('assets/Confusion Matrix Tuned GB.png')
            st.image(image3, caption="Gradient Boosting @ gradient_threshold = 0.25", use_column_width=True)

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("username: customerchurn")
    st.write("password: 33333")
