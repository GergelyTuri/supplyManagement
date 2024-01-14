import requests
import streamlit as st


# Function to fetch data from your FastAPI backend
def fetch_data(sheet, column, value):
    response = requests.get(
        f"http://127.0.0.1:8000/filtered_data/{sheet}?{column}={value}"
    )
    return response.json()


def fetch_sheet_names():
    response = requests.get("http://127.0.0.1:8000/sheets")
    return response.json()


def fetch_column_names(sheet_name):
    response = requests.get(f"http://127.0.0.1:8000/columns/{sheet_name}")
    return response.json()


def fetch_column_values(sheet_name, column_name):
    response = requests.get(
        f"http://127.0.0.1:8000/column_values/{sheet_name}/{column_name}"
    )
    return response.json()


# Streamlit UI
st.title("Supply Management Dashboard")

# Use the helper functions to fetch data for dropdowns
# Dropdown for sheets
sheet_names = fetch_sheet_names()
selected_sheet = st.selectbox("Select a Sheet", sheet_names)

# Dropdown for columns, show only if sheet is selected
if selected_sheet:
    column_names = fetch_column_names(selected_sheet)
    selected_column = st.selectbox("Select a Column", column_names)

    # Dropdown for values, show only if column is selected
    if selected_column:
        column_values = fetch_column_values(selected_sheet, selected_column)
        selected_value = st.selectbox("Select a Value", column_values)

        # Button to fetch data
        if st.button("Get Data"):
            data = fetch_data(selected_sheet, selected_column, selected_value)
            st.write(data)
