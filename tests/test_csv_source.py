from pathlib import Path

import pytest
import polars as pl
import pandas as pd

from quipus import CSVDataSource


def test_csv_data_source_valid_initialization(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")

    data_source = CSVDataSource(file_path=csv_file)

    assert str(data_source.file_path) == str(csv_file)
    assert data_source.delimiter == ","
    assert data_source.encoding == "utf8"
    assert data_source.dataframe is not None


def test_csv_data_source_invalid_file_path_type():
    with pytest.raises(TypeError):
        CSVDataSource(file_path=123)


def test_csv_data_source_empty_file_path():
    with pytest.raises(FileNotFoundError):
        CSVDataSource(file_path="")


def test_csv_data_source_file_not_found():
    with pytest.raises(FileNotFoundError):
        CSVDataSource(file_path="nonexistent.csv")


def test_csv_data_source_fetch_data(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_content = "col1,col2\n1,2\n3,4"
    csv_file.write_text(csv_content)

    data_source = CSVDataSource(file_path=str(csv_file))

    df = data_source.fetch_data()

    expected_df = pl.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    df.equals(expected_df)


def test_csv_data_source_fetch_data_no_data(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")

    data_source = CSVDataSource(file_path=str(csv_file))

    data_source.dataframe = None

    with pytest.raises(RuntimeError, match="No data loaded from the CSV file."):
        data_source.fetch_data()


def test_csv_data_source_get_columns(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")

    data_source = CSVDataSource(file_path=str(csv_file))

    columns = data_source.get_columns()

    assert columns == ["col1", "col2"]


def test_csv_data_source_get_columns_no_data(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")

    data_source = CSVDataSource(file_path=str(csv_file))

    data_source.dataframe = None

    with pytest.raises(RuntimeError, match="No data loaded from the CSV file."):
        data_source.get_columns()


def test_csv_data_source_filter_data(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_content = "col1,col2\n1,2\n3,4\n5,6"
    csv_file.write_text(csv_content)

    data_source = CSVDataSource(file_path=str(csv_file))

    filtered_df = data_source.filter_data("SELECT * FROM self WHERE col1 > 2")

    expected_df = pl.DataFrame({"col1": [3, 5], "col2": [4, 6]})
    filtered_df.equals(expected_df)


def test_csv_data_source_filter_data_invalid_query(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_content = "col1,col2\n1,2\n3,4\n5,6"
    csv_file.write_text(csv_content)

    data_source = CSVDataSource(file_path=str(csv_file))

    with pytest.raises(ValueError):
        data_source.filter_data("invalid query")


def test_csv_data_source_filter_data_no_data(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")

    data_source = CSVDataSource(file_path=str(csv_file))

    data_source.dataframe = None

    with pytest.raises(RuntimeError, match="No data loaded from the CSV file."):
        data_source.filter_data("SELECT * FROM self WHERE col1 > 2")


def test_csv_data_source_str(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")

    data_source = CSVDataSource(
        file_path=str(csv_file), delimiter=";", encoding="latin1"
    )
    expected_str = (
        f"CSVDataSource(file_path={str(csv_file)}, delimiter=;, encoding=latin1)"
    )
    assert str(data_source) == expected_str


def test_csv_data_source_invalid_delimiter(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")

    data_source = CSVDataSource(file_path=str(csv_file))
    with pytest.raises(TypeError):
        data_source.delimiter = 123


def test_csv_data_source_invalid_encoding(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")

    data_source = CSVDataSource(file_path=str(csv_file))
    with pytest.raises(TypeError):
        data_source.encoding = 123


def test_csv_data_source_invalid_delimiter_init(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")
    with pytest.raises(TypeError):
        CSVDataSource(file_path=csv_file, delimiter=123)


def test_csv_data_source_invalid_encoding_init(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")
    with pytest.raises(TypeError):
        CSVDataSource(file_path=csv_file, encoding=123)


def test_csv_data_source_empty_csv(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")

    with pytest.raises(pl.exceptions.NoDataError):
        CSVDataSource(file_path=str(csv_file))


def test_csv_data_source_invalid_csv(tmp_path):
    csv_file = tmp_path / "invalid.csv"
    csv_content = "not,a,csv,content,without,proper,format\n1,2,3,4,5,6,7"
    csv_file.write_text(csv_content)

    data_source = CSVDataSource(file_path=str(csv_file))

    df = data_source.fetch_data()

    assert df is not None
    assert not df.is_empty()
    assert df.shape == (1, 7)
