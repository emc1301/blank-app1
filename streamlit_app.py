import streamlit as st

st.title("🎈 Ella's App")
st.write(
    "I hope this works."
)

import pandas as pd
pip install -r requirements.txt

# Function to load and combine multiple CSVs into a single DataFrame
def load_data(uploaded_files):
    dataframes = []
    for file in uploaded_files:
        df = pd.read_csv(file)
        dataframes.append(df)
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df

# Function to check calculations and identify outliers
def analyze_data(df):
    # Example: Check if 'Total Cost' equals 'Price' * 'Area'
    df['Calculated Total Cost'] = df['Price'] * df['Area']
    df['Cost Mismatch'] = df['Calculated Total Cost'] != df['Total Cost']

    # Identify outliers using standard deviation
    price_mean = df['Price'].mean()
    price_std = df['Price'].std()
    df['Price Outlier'] = (df['Price'] < price_mean - 2 * price_std) | (df['Price'] > price_mean + 2 * price_std)
    
    return df

# Function to display recommendations based on the analysis
def recommend(df):
    recommendations = df[df['Cost Mismatch'] | df['Price Outlier']]
    return recommendations

# Streamlit App
st.title('Construction Job Quotes Analysis')

st.markdown("""
    Upload multiple CSV files containing quote information for analysis.
    The CSV files should have columns for **Item**, **Price**, **Area**, and **Total Cost**.
""")

uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True, type="csv")

if uploaded_files:
    st.write("## Uploaded Data")
    data = load_data(uploaded_files)
    st.write(data)

    st.write("## Analysis")
    analyzed_data = analyze_data(data)
    st.write(analyzed_data)

    st.write("## Recommendations")
    recommendations = recommend(analyzed_data)
    st.write(recommendations)

    st.write("## Download Combined Data")
    csv = analyzed_data.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Combined CSV", data=csv, file_name='analyzed_quotes.csv', mime='text/csv')

streamlit run app.py
