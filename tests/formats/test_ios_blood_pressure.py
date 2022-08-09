"""
Unit tests for bloodymary.formats.ios_blood_pressure module
"""

from pathlib import Path

import pytest

from bloodymary.formats.ios_blood_pressure import IosBloodPressureExportFile

from ..conftest import MOCK_DATA, EMPTY_FILE, VALID_IOS_DATA_FILE, VALID_IOS_DATA_RECORD_COUNT

# Test file with an unexpected data field
UNEXPECTED_FIELD_DATA_FILE = MOCK_DATA.joinpath('formats/ios_blood_pressure_unexpected_field.txt')
# Test file with an unexpected line
UNEXPECTED_LINE_DATA_FILE = MOCK_DATA.joinpath('formats/ios_blood_pressure_unexpected_line.txt')

INVALID_TIME_VALUE = '2021-02-29T01:02:03'


def test_formats_ios_blood_pressure_parse_time_invalid():
    """
    Test parsing of invalid time value
    """
    obj = IosBloodPressureExportFile()
    with pytest.raises(ValueError):
        obj.__parse_time__(INVALID_TIME_VALUE)


def test_formats_ios_blood_pressure_load_empty_file():
    """
    Test loading empty text file
    """
    obj = IosBloodPressureExportFile()
    obj.load(EMPTY_FILE)
    assert len(obj) == 0


def test_formats_ios_blood_pressure_load_unexpected_field_file():
    """
    Test loading file with unexpected field, raising ValueError
    """
    obj = IosBloodPressureExportFile()
    with pytest.raises(ValueError):
        obj.load(UNEXPECTED_FIELD_DATA_FILE)


def test_formats_ios_blood_pressure_load_unexpected_line_file():
    """
    Test loading file with unexpected line, raising ValueError
    """
    obj = IosBloodPressureExportFile()
    with pytest.raises(ValueError):
        obj.load(UNEXPECTED_LINE_DATA_FILE)


def test_formats_ios_blood_pressure_load_missing_file(tmpdir):
    """
    Test loading a valid text file for IoS Blood Pressure app exports
    """
    path = Path(tmpdir.strpath).joinpath('missing.txt')
    obj = IosBloodPressureExportFile()
    with pytest.raises(ValueError):
        obj.load(str(path))
    assert len(obj) == 0


def test_formats_ios_blood_pressure_load_valid_file():
    """
    Test loading a valid text file for IoS Blood Pressure app exports
    """
    obj = IosBloodPressureExportFile()
    obj.load(VALID_IOS_DATA_FILE)
    assert len(obj) == VALID_IOS_DATA_RECORD_COUNT
