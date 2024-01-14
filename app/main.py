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
    # Logic to fetch and return column names for a given sheet
    pass


@app.get("/column_values/{sheet_name}/{column_name}")
def get_column_values(sheet_name: str, column_name: str):
    # Logic to fetch and return values for a given column in a given sheet
    pass
