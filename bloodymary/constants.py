"""
Constants for bloodymary application
"""

from enum import Enum

DEFAULT_DATE_FORMATS = (
    '%Y%m%dT%H%M%S',
    '%Y-%m-%d',
    '%Y%m%d',
)
DEFAULT_FILE_ENCODING = 'utf-8'
BLOODYMARY_FILE_FORMAT_ENV_VAR = 'BLOODYMARY_FILE_FORMAT'

# Order of columns in exported pandas dataframe
DATAFRAME_COLUMNS = ('Time', 'Systolic', 'Diastolic', 'Pulse')


class FileFormat(Enum):
    """
    Supported file formats for blood pressure export data
    """
    IOS_BLOOD_PRESSURE_EXPORT = 'ios-blood-pressure'
