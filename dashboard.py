import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load the Excel file
@st.cache_data
def load_data(file_path):
    # Read the data from the first sheet
    df = pd.read_excel(file_path)
    
    # Ensure the 'Amended' column is converted to datetime
    if 'Amended' in df.columns:
        df['Amended'] = df['Amended'].astype(str).str.strip()  # Clean strings
        df['Amended'] = pd.to_datetime(df['Amended'], errors='coerce')  # Convert to datetime
    
    return df
# Set page config
st.set_page_config(page_title="EPG Insurance Coverage Dashboard", layout="wide")

def main():
    try:
        # Load data
        df = load_data(r"C:/Users/noel.bhumana/Documents/Github/Data Extraction/Extracted_Data/Coverage_Sheet_Bible.xlsx")
    
        
        # Title
        st.title("EPG Insurance Coverage Dashboard")
        
        # Sidebar filters
        with st.sidebar:
            st.header("Filters")
            selected_manufacturer = st.multiselect(
                "Select Programs",
                options=sorted(df['Relevant Programme'].unique()),
                default=sorted(df['Relevant Programme'].unique())
            )
            selected_status = st.multiselect(
                "Select Status",
                options=sorted(df['Status'].unique()),
                default=sorted(df['Status'].unique())
            )

        # Filter data
        filtered_df = df[
            (df['Relevant Programme'].isin(selected_manufacturer)) &
            (df['Status'].isin(selected_status))
        ]

        # Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Equipment Types", len(filtered_df))
        with col2:
            st.metric("Average Coverage Levels", round(filtered_df['Coverage_Levels'].mean(), 1))
        with col3:
            st.metric("Documents Needing Review", len(filtered_df[filtered_df['Status'] == 'Draft']))

        # Charts
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(
                filtered_df.groupby('Relevant Programme')['Coverage_Levels'].mean().reset_index(),
                x='Program',
                y='Coverage_Levels',
                title='Average Coverage Levels by Program'
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.pie(
                filtered_df,
                names='Status',
                title='Document Status Distribution',
                hole=0.4
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Timeline
        fig3 = px.scatter(
            filtered_df,
            x='Last_Updated',
            y='Relevant Programme',
            color='Status',
            title='Document Update Timeline',
            size_max=10
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Data table
        st.subheader("Detailed Coverage Information")
        st.dataframe(
            filtered_df.sort_values('Last_Updated', ascending=False)
            .style.format({'Last_Updated': lambda x: x.strftime('%d/%m/%Y')})
        )

        # Download button
        st.download_button(
            "Download Data",
            filtered_df.to_csv(index=False).encode('utf-8'),
            "coverage_data.csv",
            "text/csv"
        )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()