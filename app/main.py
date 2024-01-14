from fastapi import FastAPI, Request

from .sheets_manager import GoogleSheetsClient

app = FastAPI()

sheets_client = GoogleSheetsClient()


@app.get("/data/{sheet_name}")
def read_all_data(sheet_name: str):
    data = sheets_client.get_all_records(sheet_name)
    return data


@app.get("/filtered_data/{sheet_name}")
def read_filtered_data(sheet_name: str, request: Request):
    filters = dict(request.query_params)
    data = sheets_client.get_filtered_records(sheet_name, filters)
    return data


@app.get("/sheets")
def get_sheet_names():
    return sheets_client.get_all_sheet_names()


@app.get("/columns/{sheet_name}")
def get_column_names(sheet_name: str):
    return sheets_client.get_all_columns(sheet_name)


@app.get("/column_values/{sheet_name}/{column_name}")
def get_column_values(sheet_name: str, column_name: str):
    return sheets_client.get_column_values(sheet_name, column_name)


@app.get("/search/{sheet_name}/{query}")
def search_spreadsheet_values(sheet_name: str, query: str):
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
