import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np

# Load the model, scaler, and label encoder
rf_model = joblib.load("rf_balanced_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Set up Streamlit page
st.title("Customer Churn Prediction and Segmentation")
st.write("This demo uses a trained model to predict customer churn and classify customers into segments.")

# Helper function to preprocess user data


def preprocess_data(df):
    # Drop unnecessary columns
    df = df.drop(columns=['RowNumber', 'CustomerId',
                 'Surname', 'Exited'], errors='ignore')

    # One-Hot Encoding for Geography with missing categories handled
    df = pd.get_dummies(df, columns=['Geography'], drop_first=True)

    # Ensure columns match trained model
    for col in ['Geography_Germany', 'Geography_Spain']:
        if col not in df.columns:
            df[col] = 0

    # Label encode Gender
    df['Gender'] = label_encoder.transform(df['Gender'])

    # Standardize continuous variables
    df[['CreditScore', 'Age', 'Balance', 'EstimatedSalary']] = scaler.transform(
        df[['CreditScore', 'Age', 'Balance', 'EstimatedSalary']])

    return df

# Define function to assign customer segment


def assign_segment(df):
    df['ChurnRisk'] = rf_model.predict_proba(df)[:, 1]
    df['CustomerSegment'] = 'Unknown'
    high_value_threshold = df['Balance'].quantile(0.5)
    high_risk_threshold = 0.5
    df.loc[(df['ChurnRisk'] < high_risk_threshold) & (df['Balance']
                                                      >= high_value_threshold), 'CustomerSegment'] = 'Maintain'
    df.loc[(df['ChurnRisk'] < high_risk_threshold) & (df['Balance']
                                                      < high_value_threshold), 'CustomerSegment'] = 'Cultivate'
    df.loc[(df['ChurnRisk'] >= high_risk_threshold) & (
        df['Balance'] < high_value_threshold), 'CustomerSegment'] = 'Divest'
    df.loc[(df['ChurnRisk'] >= high_risk_threshold) & (df['Balance'] >=
                                                       high_value_threshold), 'CustomerSegment'] = 'Aggressively Retain'
    return df


# Upload data file
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file is not None:
    # Read CSV
    data = pd.read_csv(uploaded_file)
    st.write("### Data Overview", data.head())

    # Preprocess and predict
    data_processed = preprocess_data(data.copy())
    data_segmented = assign_segment(data_processed)

    # Merge original data with segmentation results
    full_data = data.copy()
    full_data[['ChurnRisk', 'CustomerSegment']
              ] = data_segmented[['ChurnRisk', 'CustomerSegment']]

    # Mapping color codes to each segment for display
    segment_colors = {
        'Maintain': 'background-color: green; color: white;',
        'Cultivate': 'background-color: blue; color: white;',
        'Divest': 'background-color: orange; color: black;',
        'Aggressively Retain': 'background-color: red; color: white;'
    }

    # Apply color coding based on CustomerSegment
    def highlight_segments(row):
        color = segment_colors.get(row['CustomerSegment'], '')
        return [color] * len(row)

    # Display full table with color coding and download option
    st.write("### Full Customer Data with Churn Risk and Segmentation")
    styled_full_data = full_data.style.apply(highlight_segments, axis=1)
    st.write(styled_full_data)

    # Option to download the entire table with segmentation results as CSV
    st.download_button(
        label="Download CSV",
        data=full_data.to_csv(index=False),
        file_name="segmentation_results.csv",
        mime="text/csv"
    )

    # Display segment counts
    st.write("### Customer Segment Counts")
    segment_counts = full_data['CustomerSegment'].value_counts()
    st.bar_chart(segment_counts)

    # Display average ChurnRisk by segment
    st.write("### Average Churn Risk by Customer Segment")
    avg_churn_risk_by_segment = full_data.groupby('CustomerSegment')[
        'ChurnRisk'].mean()
    st.bar_chart(avg_churn_risk_by_segment)

    # Display additional statistics
    st.write("### Additional Statistics")
    churn_risk_summary = full_data['ChurnRisk'].describe()
    balance_summary = full_data['Balance'].describe()

    st.write("**Churn Risk Statistics:**")
    st.write(churn_risk_summary)

    st.write("**Balance Statistics:**")
    st.write(balance_summary)

else:
    st.write("Please upload a CSV file to proceed.")
