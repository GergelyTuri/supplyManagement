from fastapi import FastAPI, Request

from .sheets_manager import (
    get_all_sheet_names,
    get_filtered_spreadsheet_data,
    get_spreadsheet_data,
)

app = FastAPI()


@app.get("/data/{sheet_name}")
def read_all_data(sheet_name: str):
    data = get_spreadsheet_data(sheet_name)
    return data


@app.get("/filtered_data/{sheet_name}")
def read_filtered_data(sheet_name: str, request: Request):
    filters = dict(request.query_params)
    data = get_filtered_spreadsheet_data(sheet_name, filters)
    return data


@app.get("/sheets")
def get_sheet_names():
    return get_all_sheet_names()


@app.get("/columns/{sheet_name}")
def get_column_names(sheet_name: str):
    # Logic to fetch and return column names for a given sheet
    pass


@app.get("/column_values/{sheet_name}/{column_name}")
def get_column_values(sheet_name: str, column_name: str):
    # Logic to fetch and return values for a given column in a given sheet
    pass
