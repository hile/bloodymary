"""
Parser for records from IoS Blood Pressure app exports
"""
from typing import Optional, Sequence
from pathlib import Path

from ..constants import DEFAULT_DATE_FORMATS, DEFAULT_FILE_ENCODING
from ..measurement import Measurement

from .base import BloodPressureLogBaseClass

INT_FIELDS = (
    'diastolic',
    'systolic',
    'pulse',
)
NULLABLE_STRING_FIELDS = (
    'notes',
)
DATE_FORMATS = (
    '%d. %B %Y at %H.%M',
)


class IosBloodPressureExportFile(BloodPressureLogBaseClass):
    """
    Parser for IoS Blood Pressure app text export files
    """
    __date_formats__ = list(DATE_FORMATS) + list(DEFAULT_DATE_FORMATS)

    def __init__(self,
                 *records: Optional[Sequence[Measurement]],
                 encoding: str = DEFAULT_FILE_ENCODING) -> None:
        super().__init__(*records)
        self.encoding = encoding

    def load(self, path: str) -> None:
        """
        Load timesheet records from the data export file
        """
        self.clear()
        record = {}
        path = Path(path).expanduser().resolve()
        if not path.is_file():
            raise ValueError(f'No such file: {path}')

        for line in path.read_text(encoding=self.encoding).splitlines():
            if line == '':
                if record:
                    self.append(self.__record_class__(**record))
                    record = {}
                continue
            try:
                key, value = line.split(':', 1)
            except ValueError as error:
                raise ValueError(f'Error parsing line {line}: {error}') from error
            key = key.lower()
            value = value.strip()
            if key == 'date':
                key = 'time'
                value = self.__parse_time__(value)
            elif key in INT_FIELDS:
                value = int(value)
            elif key in NULLABLE_STRING_FIELDS:
                value = value if value else None
            else:
                raise ValueError(f'Unexpected data field: {key}')
            record[key] = value

        if record:
            self.append(self.__record_class__(**record))

        self.sort()
