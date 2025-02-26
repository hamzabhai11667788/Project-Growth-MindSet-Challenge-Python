import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from io import BytesIO

# Page Config
st.set_page_config(page_title="Data Analyzer", layout="wide")

st.title("📊  Data Analizer By Code With Hamza Rehmani")
st.write("Upload CSV/Excel files, clean data, and generate insightful visualizations!")

# File Upload
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_ext == ".xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        st.error("❌ Unsupported file type!")
        st.stop()

    # Display Data
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # Data Cleaning Options
    st.sidebar.header("⚙️ Data Cleaning")
    
    # Remove Duplicates
    if st.sidebar.button("Remove Duplicates"):
        df.drop_duplicates(inplace=True)
        st.sidebar.success("✔️ Duplicates removed!")

    # Fill Missing Values
    fill_missing = st.sidebar.checkbox("Fill Missing Values")
    if fill_missing:
        numeric_cols = df.select_dtypes(include=['number']).columns
        if not numeric_cols.empty:
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.sidebar.success("✔️ Missing values filled!")
        else:
            st.sidebar.warning("⚠️ No numerical columns found to fill missing values!")

    # Select Columns
    st.sidebar.header("📝 Select Columns")
    columns = st.sidebar.multiselect("Choose columns", df.columns, default=df.columns)
    df = df[columns]

    # Data Visualization
    st.subheader("📊 Data Visualizations")

    # Histogram
    numeric_columns = df.select_dtypes(include=['number']).columns
    if not numeric_columns.empty:
        st.write("### 📌 Histogram")
        selected_column = st.selectbox("Select a numerical column", numeric_columns)
        fig, ax = plt.subplots()
        sns.histplot(df[selected_column], kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("⚠️ No numerical columns available for histogram!")

    # Correlation Heatmap
    st.write("### 🔥 Correlation Heatmap")
    numeric_df = df.select_dtypes(include=['number'])  # Filter only numeric columns
    if not numeric_df.empty and len(numeric_df.columns) > 1:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("⚠️ Not enough numerical columns available for correlation heatmap!")

    # Export Processed Data
    st.subheader("📥 Export Data")
    export_format = st.radio("Convert to:", ["CSV", "Excel"])
    
    if st.button("Download Processed Data"):
        buffer = BytesIO()
        if export_format == "CSV":
            df.to_csv(buffer, index=False)
            mime_type = "text/csv"
            file_name = "processed_data.csv"
        else:
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False)
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            file_name = "processed_data.xlsx"

        buffer.seek(0)
        st.download_button("📥 Download File", buffer, file_name, mime_type)

st.success("🚀 Ready to analyze your data!")
