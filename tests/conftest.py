"""
Unit test configuration for bloodymary module
"""
import os

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from bloodymary.constants import BLOODYMARY_FILE_FORMAT_ENV_VAR, FileFormat
from bloodymary.measurement import Measurement


MOCK_DATA = Path(__file__).parent.joinpath('mock')
EMPTY_FILE = MOCK_DATA.joinpath('formats/empty_file.txt')

INVALID_FILE_FORMAT_NAME = 'this-is-wrong'


@pytest.fixture
def no_file_format_env(monkeypatch):
    """
    Mock environment without file format environment variable
    """
    if BLOODYMARY_FILE_FORMAT_ENV_VAR in os.environ:
        monkeypatch.delenv(BLOODYMARY_FILE_FORMAT_ENV_VAR)
    yield None


@pytest.fixture
def invalid_file_format_env(monkeypatch):
    """
    Mock environment with invalid file format environment variable
    """
    monkeypatch.setenv(BLOODYMARY_FILE_FORMAT_ENV_VAR, INVALID_FILE_FORMAT_NAME)
    yield INVALID_FILE_FORMAT_NAME


@pytest.fixture
def valid_file_format_env(monkeypatch):
    """
    Mock environment with invalid file format environment variable
    """
    monkeypatch.setenv(BLOODYMARY_FILE_FORMAT_ENV_VAR, FileFormat.IOS_BLOOD_PRESSURE_EXPORT.value)
    yield FileFormat.IOS_BLOOD_PRESSURE_EXPORT.value


@pytest.fixture
def valid_file_format_values():
    """
    Mock environment with invalid file format environment variable
    """
    yield [file_format.value for file_format in FileFormat]


@pytest.fixture
def mock_minimal_measurement():
    """
    Initialize a mock measurement object for tests with very small values indeed
    and time one day backwards
    """
    yield Measurement(systolic=70, diastolic=35, time=datetime.now() - timedelta(days=1))


@pytest.fixture
def mock_measurement():
    """
    Initialize a mock measurement object for tests, with current timestamp as time
    """
    yield Measurement(systolic=100, diastolic=60, pulse=40, notes='Well Done')


@pytest.fixture
def mock_measurement_series():
    """
    Initialize a mock measurement object for tests, with current timestamp as time
    """
    yield [
        Measurement(systolic=116, diastolic=76, time=datetime.now() - timedelta(days=3)),
        Measurement(systolic=118, diastolic=78, time=datetime.now() - timedelta(days=2)),
        Measurement(systolic=120, diastolic=80, time=datetime.now() - timedelta(days=1)),
    ]
