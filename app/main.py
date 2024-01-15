"""
This is the main module of the FastAPI application. It manages the API endpoints and
the Google Sheets client.
"""
from fastapi import FastAPI, Request

from .sheets_manager import GoogleSheetsClient

app = FastAPI()

sheets_client = GoogleSheetsClient()


@app.get("/")
def read_root():
    """
    Returns a JSON response with the message "Hello World".
    """
    return {"Hello": "World"}


@app.get("/data/{sheet_name}")
def read_all_data(sheet_name: str):
    """
    Retrieves all records from the specified sheet in the Google Sheets document.

    Parameters:
    - sheet_name (str): The name of the sheet to retrieve data from.

    Returns:
    - data (list): A list of dictionaries representing the records in the sheet.
    """
    data = sheets_client.get_all_records(sheet_name)
    return data


@app.get("/filtered_data/{sheet_name}")
def read_filtered_data(sheet_name: str, request: Request):
    """
    Retrieves filtered records from the specified sheet in the Google Sheets document.

    Parameters:
    - sheet_name (str): The name of the sheet to retrieve data from.
    - request (Request): The FastAPI Request object containing the query parameters.

    Returns:
    - data (list): A list of dictionaries representing the filtered records in the sheet.
    """
    filters = dict(request.query_params)
    data = sheets_client.get_filtered_records(sheet_name, filters)
    return data


@app.get("/sheets")
def get_sheet_names():
    """
    Retrieves the names of all sheets in the Google Sheets document.

    Returns:
    - sheet_names (list): A list of strings representing the names of the sheets.
    """
    return sheets_client.get_all_sheet_names()


@app.get("/columns/{sheet_name}")
def get_column_names(sheet_name: str):
    """
    Retrieves the names of all columns in the specified sheet of the Google Sheets document.

    Parameters:
    - sheet_name (str): The name of the sheet to retrieve column names from.

    Returns:
    - column_names (list): A list of strings representing the names of the columns.
    """
    return sheets_client.get_all_columns(sheet_name)


@app.get("/column_values/{sheet_name}/{column_name}")
def get_column_values(sheet_name: str, column_name: str):
    """
    Retrieves the values of a specific column in the specified sheet of the Google Sheets document.

    Parameters:
    - sheet_name (str): The name of the sheet to retrieve column values from.
    - column_name (str): The name of the column to retrieve values from.

    Returns:
    - column_values (list): A list of values from the specified column.
    """
    return sheets_client.get_column_values(sheet_name, column_name)


@app.get("/search/{sheet_name}/{query}")
def search_spreadsheet_values(sheet_name: str, query: str):
    """
    Searches for records in the specified sheet of the Google Sheets document that match the given query.

    Parameters:
    - sheet_name (str): The name of the sheet to search in.
    - query (str): The query string to search for.

    Returns:
    - filtered_data (list): A list of dictionaries representing the filtered records that match the query.
    """
    data = sheets_client.get_all_records(sheet_name)
    query_lower = query.lower()
    # Filter data and handle empty cells or non-list items
    filtered_data = []
    for row in data:
        for key, value in row.items():
            if query_lower in str(value).lower():
                filtered_data.append(row)
                break  # Break to avoid adding the same row multiple times
    return filtered_data
