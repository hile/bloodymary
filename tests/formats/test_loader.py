"""
Unit tests for bloodymary.formats.loader module
"""
import pytest

from bloodymary.constants import DATAFRAME_COLUMNS
from bloodymary.exceptions import ConfigurationError
from bloodymary.formats import BloodPressureData
from bloodymary.formats.loader import FileFormat, get_file_format

from ..conftest import INVALID_FILE_FORMAT_NAME, VALID_IOS_DATA_FILE, VALID_IOS_DATA_RECORD_COUNT


# pylint: disable=unused-argument
def test_formats_get_file_format_not_found(no_file_format_env):
    """
    Test get_file_format method when file format can't be detected from string or environment
    """
    with pytest.raises(ConfigurationError):
        get_file_format()


# pylint: disable=unused-argument
def test_formats_get_file_format_invalid_env(invalid_file_format_env):
    """
    Test get_file_format method when file format can't be detected from string and environment
    contains invalid value
    """
    with pytest.raises(ConfigurationError):
        get_file_format()


# pylint: disable=unused-argument
def test_formats_get_file_format_invalid_string_value(no_file_format_env):
    """
    Test get_file_format method when file format specified is not valid value
    """
    with pytest.raises(ConfigurationError):
        get_file_format(INVALID_FILE_FORMAT_NAME)


def test_formats_get_file_format_valid_values(valid_file_format_values):
    """
    Test get_file_format method when file format specified is a valid value
    """
    for value in valid_file_format_values:
        assert isinstance(get_file_format(value), FileFormat)


# pylint: disable=unused-argument
def test_blood_pressure_data_loader_no_file_format(no_file_format_env):
    """
    Test initializing BloodPressureData with no file format detected
    """
    with pytest.raises(ConfigurationError):
        BloodPressureData()


# pylint: disable=unused-argument
def test_blood_pressure_data_loader_invalid_file_format(no_file_format_env):
    """
    Test initializing BloodPressureData with invalid file format passed as argument
    """
    with pytest.raises(ConfigurationError):
        BloodPressureData(INVALID_FILE_FORMAT_NAME)


# pylint: disable=unused-argument
def test_blood_pressure_data_loader_valid_string_file_format_value(valid_file_format_env):
    """
    Test initializing BloodPressureData with valid FileFormat name
    """
    loader = BloodPressureData(FileFormat.IOS_BLOOD_PRESSURE_EXPORT.value)
    assert len(loader.records) == 0


# pylint: disable=unused-argument
def test_blood_pressure_data_loader_valid_environment_variable(valid_file_format_env):
    """
    Test initializing BloodPressureData with valid FileFormat from environment variable
    """
    loader = BloodPressureData()
    assert len(loader.records) == 0


# pylint: disable=unused-argument
def test_blood_pressure_data_loader_valid_explicit_file_format(no_file_format_env):
    """
    Test initializing BloodPressureData with FileFormat object as argument
    """
    loader = BloodPressureData(FileFormat.IOS_BLOOD_PRESSURE_EXPORT)
    assert len(loader.records) == 0


# pylint: disable=unused-argument
def test_blood_pressure_data_loader_dataframe_generate(no_file_format_env):
    """
    Test generating a pandas dataframe from test data
    """
    loader = BloodPressureData(FileFormat.IOS_BLOOD_PRESSURE_EXPORT)
    loader.records.load(VALID_IOS_DATA_FILE)
    assert len(loader.records) == VALID_IOS_DATA_RECORD_COUNT

    dataframe = loader.get_dataframe()
    assert list(dataframe.columns) == list(DATAFRAME_COLUMNS)
    for column in DATAFRAME_COLUMNS:
        assert len(dataframe[column]) == VALID_IOS_DATA_RECORD_COUNT


# pylint: disable=unused-argument
def test_blood_pressure_data_loader_dataframe_generate_filtered(no_file_format_env):
    """
    Test generating a pandas dataframe from test data with filtered record set
    """
    loader = BloodPressureData(FileFormat.IOS_BLOOD_PRESSURE_EXPORT)
    loader.records.load(VALID_IOS_DATA_FILE)
    assert len(loader.records) == VALID_IOS_DATA_RECORD_COUNT

    # Filter by date picks last 2 records from the set
    filtered_records_count = 2
    dataframe = loader.get_dataframe(loader.records.filter(start_time=loader.records[-2].time))
    assert list(dataframe.columns) == list(DATAFRAME_COLUMNS)
    for column in DATAFRAME_COLUMNS:
        assert len(dataframe[column]) == filtered_records_count
