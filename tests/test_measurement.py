"""
Unit tests for bloodymary.measurement class
"""

INT_ATTRIBUTES = (
    'systolic',
    'diastolic',
    'pulse',
)
OPTIONAL_STR_ATTRIBUTES = (
    'notes',
)


def test_measurement_properties(mock_measurement):
    """
    Test basic properties of mocked measurement object
    """
    for attr in INT_ATTRIBUTES:
        assert isinstance(getattr(mock_measurement, attr), int)
    for attr in OPTIONAL_STR_ATTRIBUTES:
        value = getattr(mock_measurement, attr)
        assert value is None or isinstance(getattr(mock_measurement, attr), str)
    assert isinstance(mock_measurement.__repr__(), str)
