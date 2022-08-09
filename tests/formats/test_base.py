"""
Unit tests for the bloodymary.formats.base module
"""
from datetime import timedelta

import pytest

from bloodymary.formats.base import BloodPressureLogBaseClass


def test_formats_base_class_attributes():
    """
    Test attributes of the BloodPressureLogBaseClass base class
    """
    obj = BloodPressureLogBaseClass()
    assert obj.__items__ == []  # pylint: disable=use-implicit-booleaness-not-comparison

    with pytest.raises(NotImplementedError):
        obj.load(None)


def test_formats_base_class_add_remove(mock_measurement, mock_minimal_measurement):
    """
    Test adding and removing measurements to the base class directly
    """
    obj = BloodPressureLogBaseClass()
    assert len(obj) == 0
    obj.insert(0, mock_measurement)

    assert len(obj) == 1
    obj.insert(0, mock_measurement)

    assert len(obj) == 2
    assert obj[-1] == mock_measurement

    obj[0] = mock_minimal_measurement
    assert len(obj) == 2

    del obj[0]
    assert len(obj) == 1


def test_formats_base_class_sorting(mock_measurement, mock_minimal_measurement):
    """
    Test sorting of objects in the base class with known ordering
    """
    obj = BloodPressureLogBaseClass()

    # This has current datetime
    obj.append(mock_measurement)
    # This has date one day in past
    obj.append(mock_minimal_measurement)

    # Not sorted by append
    assert obj[0] == mock_measurement
    assert obj[1] == mock_minimal_measurement

    # sort objects, placing latest last
    obj.sort()
    assert obj[0] == mock_minimal_measurement
    assert obj[1] == mock_measurement


def test_formats_base_class_filter_no_params(mock_measurement_series):
    """
    Test filtering without giving filter any parameters
    """
    obj = BloodPressureLogBaseClass(*mock_measurement_series)
    assert len(obj.filter()) == len(mock_measurement_series)


def test_formats_base_class_filter_start_date(mock_measurement_series):
    """
    Test sorting of objects in the base class with known ordering
    """
    obj = BloodPressureLogBaseClass(*mock_measurement_series)
    assert len(obj) == len(mock_measurement_series)

    # Filter with arbitrary old date string
    assert len(obj.filter(start_time='2000-01-01', end_time='3000-01-01')) == len(mock_measurement_series)

    # No matching times with start time after last record
    too_new = mock_measurement_series[-1].time + timedelta(hours=1)
    assert len(obj.filter(start_time=too_new)) == 0

    assert len(obj.filter(start_time=mock_measurement_series[-1].time)) == 1
    assert len(obj.filter(start_time=mock_measurement_series[-2].time)) == 2


def test_formats_base_class_filter_end_date(mock_measurement_series):
    """
    Test sorting of objects in the base class with known ordering
    """
    obj = BloodPressureLogBaseClass(*mock_measurement_series)
    assert len(obj) == len(mock_measurement_series)

    # No matching times with start time after last record
    too_old = mock_measurement_series[0].time - timedelta(hours=1)
    assert len(obj.filter(end_time=too_old)) == 0

    assert len(obj.filter(end_time=mock_measurement_series[0].time)) == 1
    assert len(obj.filter(end_time=mock_measurement_series[1].time)) == 2
