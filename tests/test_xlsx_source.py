import pytest
import polars as pl
import pandas as pd

from quipus import XLSXDataSource

def test_xlsx_data_source_valid_initialization(tmp_path):
    xlsx_file = tmp_path / "test.xlsx"
    data = pl.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    data.write_excel(xlsx_file)

    data_source = XLSXDataSource(file_path=str(xlsx_file), sheet_name="Sheet1")

    assert str(data_source.file_path) == str(xlsx_file)
    assert data_source.sheet_name == "Sheet1"
    assert data_source.dataframe is not None

def test_xlsx_data_source_invalid_file_path_type():
    with pytest.raises(TypeError):
        XLSXDataSource(file_path=123, sheet_name="Sheet1")

def test_xlsx_data_source_empty_file_path():
    with pytest.raises(FileNotFoundError):
        XLSXDataSource(file_path="", sheet_name="Sheet1")

def test_xlsx_data_source_file_not_found():
    with pytest.raises(FileNotFoundError):
        XLSXDataSource(file_path="nonexistent.xlsx", sheet_name="Sheet1")

def test_xlsx_data_source_fetch_data(tmp_path):
    xlsx_file = tmp_path / "test.xlsx"
    data = pl.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    data.write_excel(xlsx_file)

    data_source = XLSXDataSource(file_path=str(xlsx_file), sheet_name="Sheet1")
    df = data_source.fetch_data()

    df.equals(data)

def test_xlsx_data_source_get_columns(tmp_path):
    xlsx_file = tmp_path / "test.xlsx"
    data = pl.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    data.write_excel(xlsx_file)

    data_source = XLSXDataSource(file_path=str(xlsx_file), sheet_name="Sheet1")
    columns = data_source.get_columns()

    assert columns == ["col1", "col2"]

def test_xlsx_data_source_filter_data(tmp_path):
    xlsx_file = tmp_path / "test.xlsx"
    data = pl.DataFrame({"col1": [1, 3, 5], "col2": [2, 4, 6]})
    data.write_excel(xlsx_file)

    data_source = XLSXDataSource(file_path=str(xlsx_file), sheet_name="Sheet1")
    filtered_df = data_source.filter_data("SELECT * FROM self WHERE col1 > 2")

    expected_df = pl.DataFrame({"col1": [3, 5], "col2": [4, 6]})
    filtered_df.equals(expected_df)

def test_xlsx_data_source_invalid_sheet_name(tmp_path):
    xlsx_file = tmp_path / "test.xlsx"
    data = pl.DataFrame({"col1": [1], "col2": [2]})
    data.write_excel(xlsx_file, worksheet="Sheet1")

    with pytest.raises(ValueError):
        XLSXDataSource(file_path=str(xlsx_file), sheet_name="InvalidSheet")

def test_xlsx_data_source_no_data_loaded(tmp_path):
    xlsx_file = tmp_path / "test.xlsx"
    pl.DataFrame({"col1": [1], "col2": [2]}).write_excel(xlsx_file)

    data_source = XLSXDataSource(file_path=str(xlsx_file), sheet_name="Sheet1")
    data_source.dataframe = None

    with pytest.raises(RuntimeError, match="No data loaded from the Excel file."):
        data_source.fetch_data()

def test_xlsx_data_source_invalid_query(tmp_path):
    xlsx_file = tmp_path / "test.xlsx"
    data = pl.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    data.write_excel(xlsx_file)

    data_source = XLSXDataSource(file_path=str(xlsx_file), sheet_name="Sheet1")

    with pytest.raises(ValueError):
        data_source.filter_data("invalid query")

def test_xlsx_data_source_str(tmp_path):
    xlsx_file = tmp_path / "test.xlsx"
    data = pl.DataFrame({"col1": [1], "col2": [2]})
    data.write_excel(xlsx_file)

    data_source = XLSXDataSource(file_path=str(xlsx_file), sheet_name="Sheet1")
    expected_str = f"XLSXDataSource(file_path={str(xlsx_file)}, sheet_name=Sheet1)"
    assert str(data_source) == expected_str
