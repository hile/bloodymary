"""
Unit test configuration for bloodymary module
"""

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from bloodymary.measurement import Measurement


MOCK_DATA = Path(__file__).parent.joinpath('mock')
EMPTY_FILE = MOCK_DATA.joinpath('formats/empty_file.txt')


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
