import json
import os

import gspread
from google.cloud import secretmanager

SPREADSHEET = "Supply database"
SECRET_NAME = "projects/elegant-tendril-245600/secrets/supply_manager_service_account/versions/latest"
LOCAL_CREDENTIALS_FILE = "C:\\Users\\Gergo_PC\\Documents\\code\\service_acct_keys\\elegant-tendril-245600-75201e93f704.json"


class GoogleSheetsClient:
    def __init__(self):
        if os.getenv("RUNNING_IN_CLOUD"):
            credentials_json = self.get_credentials_from_secret_manager()
        else:
            with open(LOCAL_CREDENTIALS_FILE) as f:
                credentials_json = json.load(f)
        self.gc = gspread.service_account_from_dict(credentials_json)
        self.spreadsheet = self.gc.open(SPREADSHEET)

    def get_credentials_from_secret_manager(self):
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(name=SECRET_NAME)
        return json.loads(response.payload.data.decode("UTF-8"))

    def get_worksheet(self, sheet_name):
        try:
            return self.spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            raise ValueError(f"Sheet '{sheet_name}' not found in spreadsheet.")

    def get_all_records(self, sheet_name):
        sheet = self.get_worksheet(sheet_name)
        return sheet.get_all_records()

    def get_filtered_records(self, sheet_name, filters):
        data = self.get_all_records(sheet_name)

        for key, value in filters.items():
            data = [
                row
                for row in data
                if str(row.get(key, "")).lower() == str(value).lower()
            ]

        return data

    def get_all_sheet_names(self):
        return [sheet.title for sheet in self.spreadsheet.worksheets()]

    def get_all_columns(self, sheet_name):
        sheet = self.get_worksheet(sheet_name)
        return sheet.row_values(1)

    def get_column_values(self, sheet_name, column_name):
        sheet = self.get_worksheet(sheet_name)
        column_names = sheet.row_values(1)
        column_index = column_names.index(column_name) + 1
        return sheet.col_values(column_index)
