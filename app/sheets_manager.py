import gspread

SPREADSHEET = "Supply database"
CREDENTIALS_FILE = "C:\\Users\\Gergo_PC\\Documents\\code\\service_acct_keys\\elegant-tendril-245600-75201e93f704.json"


class GoogleSheetsClient:
    def __init__(self):
        self.gc = gspread.service_account(filename=CREDENTIALS_FILE)
        self.spreadsheet = self.gc.open(SPREADSHEET)

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


# Instantiate the client once and use its methods to interact with the spreadsheet
# sheets_client = GoogleSheetsClient()

# Example usage
# data = sheets_client.get_all_records("Sheet1")
# filtered_data = sheets_client.get_filtered_records("Sheet1", {"Vendor": "upenn"})
# sheet_names = sheets_client.get_all_sheet_names()
# columns = sheets_client.get_all_columns("Sheet1")
