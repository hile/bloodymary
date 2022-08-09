"""
Map loader classes to data formats
"""
import os

from typing import Optional

import pandas

from ..constants import BLOODYMARY_FILE_FORMAT_ENV_VAR, DATAFRAME_COLUMNS, FileFormat
from ..exceptions import ConfigurationError

from .ios_blood_pressure import IosBloodPressureExportFile

FILE_FORMAT_LOADERS = {
    FileFormat.IOS_BLOOD_PRESSURE_EXPORT: IosBloodPressureExportFile,
}


def get_file_format(file_format: Optional[str] = None) -> FileFormat:
    """
    Get file format by string value or from environment variable
    """
    if file_format is None:
        file_format = os.environ.get(BLOODYMARY_FILE_FORMAT_ENV_VAR, None)
    if file_format is not None:
        try:
            return FileFormat(file_format)
        except ValueError as error:
            raise ConfigurationError(f'Unexpected file format: {file_format}') from error
    raise ConfigurationError('Bloody mary file format not specified')


# pylint: disable=too-few-public-methods
class BloodPressureData:
    """
    Blood pressure data loader for named file format
    """
    def __init__(self, file_format: Optional[str] = None) -> None:
        if not isinstance(file_format, FileFormat):
            file_format = get_file_format(file_format)
        self.file_format = file_format
        self.records = FILE_FORMAT_LOADERS[self.file_format]()

    @property
    def dataframe(self):
        """
        Return a pandas dataframe for the measurement records
        """
        data = {}
        for column in DATAFRAME_COLUMNS:
            attr = column.lower()
            data[column] = [
                getattr(measurement, attr)
                for measurement in self.records
            ]
        return pandas.DataFrame(data, columns=DATAFRAME_COLUMNS)
