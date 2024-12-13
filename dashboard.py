import streamlit as st
import pandas as pd
from openpyxl import load_workbook

# Filepath for the Excel file
FILE_PATH = r"Coverage_Sheet_Bible.xlsx"

# Title and description
st.set_page_config(
    page_title="Coverage Sheet Dashboard",
    # page_icon=":bar_chart:",
    layout="wide"
)

# Rest of your Streamlit app code
st.title("Coverage Sheet Dashboard")
st.markdown(
    """This dashboard provides tools to filter, edit, add, and sort the coverage sheet data.
    Updated changes will reflect directly in the Excel file."""
)

# Load the Excel file and cache the data
@st.cache_data
def load_data():
    return pd.read_excel(FILE_PATH)

# Save updated data back to the Excel file
def save_data(data):
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        data.to_excel(writer, index=False)

# Load initial data
data = load_data()



# Filter by "Relevant Program" column
st.sidebar.header("Filter Options")
program_filter = st.sidebar.selectbox(
    "Select Relevant Program", ["All"] + list(data["Relevant Programme"].dropna().unique())
)

if program_filter != "All":
    filtered_data = data[data["Relevant Programme"] == program_filter]
else:
    filtered_data = data

st.subheader("Filtered Data")
st.write(filtered_data)

# Sort by "Checked" column
if "Checked" in data.columns:
    st.subheader("Latest Coverage Sheets Sorted by Checked Column")
    # Convert "Checked" column to datetime, coercing errors to NaT
    data["Checked"] = pd.to_datetime(data["Checked"], errors="coerce")
    sorted_data = data.sort_values(by="Checked", ascending=False, na_position="last")
    if program_filter != "All":
        filtered_data_by_Date = sorted_data[sorted_data["Relevant Programme"] == program_filter]
    else:
        filtered_data_by_Date = sorted_data
    st.write(filtered_data_by_Date)



# Edit rows
st.subheader("Edit Rows")
row_to_edit = st.number_input(
    "Enter the row index to edit:", min_value=0, max_value=len(data) - 1, step=1
)

data_to_edit = filtered_data.iloc[row_to_edit]
edit_columns = st.multiselect("Columns to edit", data.columns.tolist())

if edit_columns:
    for column in edit_columns:
        new_value = st.text_input(f"Enter new value for {column}", value=str(data_to_edit[column]))
        data.at[row_to_edit, column] = new_value

    # Save changes to the Excel file
    if st.button("Save Changes"):
        save_data(data)
        st.success("Changes saved successfully.")

# Add new row
st.subheader("Add New Row")
if st.button("Add Row"):
    new_row = {col: st.text_input(f"Enter value for {col}") for col in data.columns}
    data = data.append(new_row, ignore_index=True)
    save_data(data)
    st.success("New row added successfully.")

# Additional functionality: Download updated data
st.subheader("Download Updated Data")
st.download_button(
    "Download Data as CSV",
    data.to_csv(index=False),
    file_name="updated_coverage_sheets_list.csv",
    mime="text/csv"
)

# Footer
st.markdown("Powered by Streamlit. Data is saved directly to the Excel file.")
