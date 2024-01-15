import json
import os

import gspread
from google.cloud import secretmanager

SPREADSHEET = "Supply database"
SECRET_NAME = "projects/elegant-tendril-245600/secrets/supply_manager_service_account/versions/latest"
LOCAL_CREDENTIALS_FILE = "C:\\Users\\Gergo_PC\\Documents\\code\\service_acct_keys\\elegant-tendril-245600-75201e93f704.json"


class GoogleSheetsClient:
    """
    A client for interacting with Google Sheets.

    This class provides methods to access and manipulate data in a Google Sheets spreadsheet.

    Attributes:
        gc: The gspread client instance.
        spreadsheet: The Google Sheets spreadsheet object.
    """

    def __init__(self):
        """
        Initializes a new instance of the GoogleSheetsClient class.

        If the code is running in a cloud environment, it retrieves the credentials from Secret Manager.
        Otherwise, it reads the credentials from a local file.

        Raises:
            FileNotFoundError: If the local credentials file is not found.
            ValueError: If the specified sheet is not found in the spreadsheet.
        """
        if os.getenv("RUNNING_IN_CLOUD"):
            credentials_json = self.get_credentials_from_secret_manager()
        else:
            with open(LOCAL_CREDENTIALS_FILE) as f:
                credentials_json = json.load(f)
        self.gc = gspread.service_account_from_dict(credentials_json)
        self.spreadsheet = self.gc.open(SPREADSHEET)

    def get_credentials_from_secret_manager(self):
        """
        Retrieves the credentials from Secret Manager.

        Returns:
            The credentials JSON as a dictionary.

        Raises:
            google.api_core.exceptions.NotFound: If the specified secret is not found.
        """
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(name=SECRET_NAME)
        return json.loads(response.payload.data.decode("UTF-8"))

    def get_worksheet(self, sheet_name):
        """
        Retrieves a worksheet by its name.

        Args:
            sheet_name: The name of the worksheet.

        Returns:
            The worksheet object.

        Raises:
            ValueError: If the specified sheet is not found in the spreadsheet.
        """
        try:
            return self.spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            raise ValueError(f"Sheet '{sheet_name}' not found in spreadsheet.")

    def get_all_records(self, sheet_name):
        """
        Retrieves all records from a worksheet.

        Args:
            sheet_name: The name of the worksheet.

        Returns:
            A list of dictionaries representing the records.

        Raises:
            ValueError: If the specified sheet is not found in the spreadsheet.
        """
        sheet = self.get_worksheet(sheet_name)
        return sheet.get_all_records()

    def get_filtered_records(self, sheet_name, filters):
        """
        Retrieves filtered records from a worksheet.

        Args:
            sheet_name: The name of the worksheet.
            filters: A dictionary of filters to apply.

        Returns:
            A list of dictionaries representing the filtered records.

        Raises:
            ValueError: If the specified sheet is not found in the spreadsheet.
        """
        data = self.get_all_records(sheet_name)

        for key, value in filters.items():
            data = [
                row
                for row in data
                if str(row.get(key, "")).lower() == str(value).lower()
            ]

        return data

    def get_all_sheet_names(self):
        """
        Retrieves the names of all sheets in the spreadsheet.

        Returns:
            A list of sheet names.
        """
        return [sheet.title for sheet in self.spreadsheet.worksheets()]

    def get_all_columns(self, sheet_name):
        """
        Retrieves the names of all columns in a worksheet.

        Args:
            sheet_name: The name of the worksheet.

        Returns:
            A list of column names.

        Raises:
            ValueError: If the specified sheet is not found in the spreadsheet.
        """
        sheet = self.get_worksheet(sheet_name)
        return sheet.row_values(1)

    def get_column_values(self, sheet_name, column_name):
        """
        Retrieves the values of a specific column in a worksheet.

        Args:
            sheet_name: The name of the worksheet.
            column_name: The name of the column.

        Returns:
            A list of column values.

        Raises:
            ValueError: If the specified sheet is not found in the spreadsheet.
        """
        sheet = self.get_worksheet(sheet_name)
        column_names = sheet.row_values(1)
        column_index = column_names.index(column_name) + 1
        return sheet.col_values(column_index)
