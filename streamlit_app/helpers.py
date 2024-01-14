import pandas as pd
import requests
import streamlit as st


class FastAPIClient:
    BASE_URL = "http://127.0.0.1:8000"

    @staticmethod
    def fetch_all_data(sheet_name):
        response = requests.get(f"{FastAPIClient.BASE_URL}/data/{sheet_name}")
        return response.json()

    @staticmethod
    def fetch_data(sheet_name, column_name, value):
        response = requests.get(
            f"{FastAPIClient.BASE_URL}/filtered_data/{sheet_name}?{column_name}={value}"
        )
        return response.json()

    @staticmethod
    def fetch_sheet_names():
        response = requests.get(f"{FastAPIClient.BASE_URL}/sheets")
        return response.json()

    @staticmethod
    def fetch_column_names(sheet_name):
        response = requests.get(f"{FastAPIClient.BASE_URL}/columns/{sheet_name}")
        return response.json()

    @staticmethod
    def fetch_column_values(sheet_name, column_name):
        response = requests.get(
            f"{FastAPIClient.BASE_URL}/column_values/{sheet_name}/{column_name}"
        )
        return response.json()

    @staticmethod
    def fetch_search_results(sheet_name, query):
        response = requests.get(f"{FastAPIClient.BASE_URL}/search/{sheet_name}/{query}")
        return response.json()


class Styling:
    @staticmethod
    def style_data(df):
        # Apply conditional formatting or other styling here
        styled_df = df
        return styled_df

    @staticmethod
    def render_home_page():
        st.title("Welcome to the Supply Management Dashboard")
        st.write("Select an option from the sidebar to get started.")

    @staticmethod
    def render_databases_page(client):
        st.title("Supply Databases")
        st.write("Select a database from the sidebar to view its contents.")

        # Use the helper functions to fetch data for dropdowns
        # Dropdown for sheets
        sheet_names = client.fetch_sheet_names()
        selected_sheet = st.selectbox("Select a Sheet", sheet_names)

        # Button to fetch data
        if st.button("Get Data"):
            data = client.fetch_all_data(selected_sheet)
            df = pd.DataFrame(data)
            styled_df = Styling.style_data(df)
            st.dataframe(styled_df)

    @staticmethod
    def render_value_search_page(client):
        st.title("Search the Supply Database by given values")
        st.write("Use the dropdowns below to search the supply database.")

        # Use the helper functions to fetch data for dropdowns
        # Dropdown for sheets
        sheet_names = client.fetch_sheet_names()
        selected_sheet = st.selectbox("Select a Sheet", sheet_names)

        # Dropdown for columns, show only if sheet is selected
        if selected_sheet:
            column_names = client.fetch_column_names(selected_sheet)
            selected_column = st.selectbox("Select a Column", column_names)

            # Dropdown for values, show only if column is selected
            if selected_column:
                column_values = client.fetch_column_values(
                    selected_sheet, selected_column
                )
                selected_value = st.selectbox("Select a Value", column_values)

                # Button to fetch data
                if st.button("Get Data"):
                    data = client.fetch_data(
                        selected_sheet, selected_column, selected_value
                    )
                    df = pd.DataFrame(data)
                    styled_df = Styling.style_data(df)
                    st.dataframe(styled_df)

    @staticmethod
    def render_string_search_page(client):
        st.title("Search the Supply Database by strings")
        st.write("Use the input boxes below to search the supply database.")

        # Dropdown for sheets
        sheet_names = client.fetch_sheet_names()
        selected_sheet = st.selectbox("Select a Sheet", sheet_names)

        query = st.text_input("Enter search query")
        if st.button("Search"):
            search_results = client.fetch_search_results(selected_sheet, query)

            if search_results:  # Check if the search results are not empty
                df = pd.DataFrame.from_records(search_results)
                st.write(f"Found {len(df)} results.")
                styled_df = Styling.style_data(df)
                st.dataframe(styled_df)
            else:
                st.write("No results found.")
