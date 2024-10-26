import pytest
import pandas as pd

from quipus.data_sources.dataframe_data_source import DataFrameDataSource


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": [10, 20, 30, 40],
            "C": ["w", "x", "y", "z"],
        }
    )


@pytest.fixture
def dataframe_source(sample_dataframe):
    return DataFrameDataSource(sample_dataframe)


@pytest.fixture
def dataframe_source_empty():
    return DataFrameDataSource(pd.DataFrame())


def test_fetch_data(dataframe_source, sample_dataframe):
    fetched_data = dataframe_source.fetch_data()
    pd.testing.assert_frame_equal(fetched_data, sample_dataframe)


def test_get_columns(dataframe_source):
    assert dataframe_source.get_columns() == ["A", "B", "C"]


def test_filter_data(dataframe_source):
    filtered_data = dataframe_source.filter_data("A > 2")
    expected_filtered_data = pd.DataFrame(
        {
            "A": [3, 4],
            "B": [30, 40],
            "C": ["y", "z"],
        }
    )

    pd.testing.assert_frame_equal(
        filtered_data.reset_index(drop=True), expected_filtered_data
    )


def test_filter_data_invalid_query(dataframe_source):
    with pytest.raises(TypeError):
        dataframe_source.filter_data(123)

    with pytest.raises(ValueError):
        dataframe_source.filter_data("")

    with pytest.raises(ValueError):
        dataframe_source.filter_data(None)


def test_str(dataframe_source):
    assert (
        str(dataframe_source)
        == "DataFrameDataSource(dataframe with 4 rows and 3 columns)"
    )
