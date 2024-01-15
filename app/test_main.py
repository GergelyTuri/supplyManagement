"""
Copilot-generated FastAPI app tests.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    """
    Test case for reading the root endpoint.

    Returns:
        None
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_all_data():
    """
    Test case for reading all data from a specific sheet.

    Returns:
        None
    """
    response = client.get("/data/sheet1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_filtered_data():
    """
    Test case for reading filtered data from a specific sheet.

    Returns:
        None
    """
    response = client.get("/filtered_data/sheet1?filter1=value1&filter2=value2")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_sheet_names():
    """
    Test case for getting the names of all sheets.

    Returns:
        None
    """
    response = client.get("/sheets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_column_names():
    """
    Test case for getting the names of all columns in a specific sheet.

    Returns:
        None
    """
    response = client.get("/columns/sheet1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_column_values():
    """
    Test case for getting the values of a specific column in a specific sheet.

    Returns:
        None
    """
    response = client.get("/column_values/sheet1/column1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_spreadsheet_values():
    """
    Test case for searching values in a specific sheet.

    Returns:
        None
    """
    response = client.get("/search/sheet1/query")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
