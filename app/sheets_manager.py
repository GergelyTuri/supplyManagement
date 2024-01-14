import gspread

SPREADSHEET = "Supply database"


def get_google_sheets_client():
    """
    Returns a Google Sheets client object authenticated with a service account key.

    :return: Google Sheets client object
    """
    gc = gspread.service_account(
        filename="C:\\Users\\Gergo_PC\\Documents\\code\\service_acct_keys\\elegant-tendril-245600-75201e93f704.json"
    )
    return gc


def get_spreadsheet_data(sheet_name):
    client = get_google_sheets_client()
    sheet = client.open(SPREADSHEET).worksheet(sheet_name)
    data = sheet.get_all_records()
    return data


def get_filtered_spreadsheet_data(sheet_name, filters):
    data = get_spreadsheet_data(sheet_name)

    if filters:
        for key, value in filters.items():
            data = [
                row
                for row in data
                if str(row.get(key, "")).lower() == str(value).lower()
            ]
        return data
    else:
        return data


def get_all_sheet_names():
    client = get_google_sheets_client()
    spreadsheet = client.open(SPREADSHEET)
    sheet_names = [sheet.title for sheet in spreadsheet.worksheets()]
    return sheet_names


def get_all_columns(sheet_name):
    client = get_google_sheets_client()
    spreadsheet = client.open(SPREADSHEET)
    sheet = spreadsheet.worksheet(sheet_name)
    columns = sheet.row_values(1)
    return columns
