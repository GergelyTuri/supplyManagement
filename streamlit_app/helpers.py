"""
Helper functions for the supply management dashboard.
"""

import pandas as pd
import requests
import streamlit as st


class FastAPIClient:
    """
    A class that provides methods to interact with a FastAPI server for fetching data from a supply management system.
    """

    BASE_URL = st.secrets.get("PRODUCTION_URL", "http://127.0.0.1:8000")
    TIMEOUT_SECONDS = 10

    @staticmethod
    def fetch_all_data(sheet_name):
        """
        Fetches all data from a specific sheet in the supply management system.

        Args:
            sheet_name (str): The name of the sheet.

        Returns:
            dict: The fetched data as a dictionary.
        """
        response = requests.get(
            f"{FastAPIClient.BASE_URL}/data/{sheet_name}",
            timeout=FastAPIClient.TIMEOUT_SECONDS,
        )
        return response.json()

    @staticmethod
    def fetch_data(sheet_name, column_name, value):
        """
        Fetches data from a specific sheet in the supply management system based on a column name and value.

        Args:
            sheet_name (str): The name of the sheet.
            column_name (str): The name of the column.
            value: The value to filter the data.

        Returns:
            dict: The fetched data as a dictionary.
        """
        response = requests.get(
            f"{FastAPIClient.BASE_URL}/filtered_data/{sheet_name}?{column_name}={value}",
            timeout=FastAPIClient.TIMEOUT_SECONDS,
        )
        return response.json()

    @staticmethod
    def fetch_sheet_names():
        """
        Fetches the names of all sheets in the supply management system.

        Returns:
            list: The list of sheet names.
        """
        response = requests.get(
            f"{FastAPIClient.BASE_URL}/sheets", timeout=FastAPIClient.TIMEOUT_SECONDS
        )
        return response.json()

    @staticmethod
    def fetch_column_names(sheet_name):
        """
        Fetches the names of all columns in a specific sheet of the supply management system.

        Args:
            sheet_name (str): The name of the sheet.

        Returns:
            list: The list of column names.
        """
        response = requests.get(
            f"{FastAPIClient.BASE_URL}/columns/{sheet_name}",
            timeout=FastAPIClient.TIMEOUT_SECONDS,
        )
        return response.json()

    @staticmethod
    def fetch_column_values(sheet_name, column_name):
        """
        Fetches the values of a specific column in a specific sheet of the supply management system.

        Args:
            sheet_name (str): The name of the sheet.
            column_name (str): The name of the column.

        Returns:
            list: The list of column values.
        """
        response = requests.get(
            f"{FastAPIClient.BASE_URL}/column_values/{sheet_name}/{column_name}",
            timeout=FastAPIClient.TIMEOUT_SECONDS,
        )
        return response.json()

    @staticmethod
    def fetch_search_results(sheet_name, query):
        """
        Fetches the search results from a specific sheet in the supply management system based on a query.

        Args:
            sheet_name (str): The name of the sheet.
            query (str): The search query.

        Returns:
            list: The list of search results.
        """
        response = requests.get(
            f"{FastAPIClient.BASE_URL}/search/{sheet_name}/{query}",
            timeout=FastAPIClient.TIMEOUT_SECONDS,
        )
        return response.json()


class Styling:
    """
    A class that provides methods for styling data in the supply management dashboard.
    """

    @staticmethod
    def style_data(df):
        """
        Applies conditional formatting or other styling to a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to style.

        Returns:
            pd.DataFrame: The styled DataFrame.
        """
        styled_df = df
        return styled_df

    @staticmethod
    def render_home_page():
        """
        Renders the home page of the supply management dashboard.
        """
        st.title("Welcome to the Supply Management Dashboard")
        st.write("Select an option from the sidebar to get started.")

    @staticmethod
    def render_databases_page(client):
        """
        Renders the databases page of the supply management dashboard.

        Args:
            client (FastAPIClient): The FastAPIClient instance.
        """
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
        """
        Renders the value search page of the supply management dashboard.

        Args:
            client (FastAPIClient): The FastAPIClient instance.
        """
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
        """
        Renders the string search page of the supply management dashboard.

        Args:
            client (FastAPIClient): The FastAPIClient instance.
        """
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
