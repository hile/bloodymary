"""
Common base class for different blood pressure export files
"""

from collections.abc import MutableSequence
from datetime import datetime
from typing import Optional, Sequence

from ..constants import DEFAULT_DATE_FORMATS
from ..measurement import Measurement


class BloodPressureLogBaseClass(MutableSequence):
    """
    Blood pressure records list base class
    """
    __date_formats__ = DEFAULT_DATE_FORMATS

    __record_class__ = Measurement
    __items__: Sequence[Measurement] = []

    def __init__(self,
                 *records: Optional[Sequence[Measurement]]):
        self.__items__ = records if records else []

    @classmethod
    def clone_from_filtered_records(cls, *records):
        """
        Clone summary record from filtered items
        """
        return cls(*records)

    def __delitem__(self, index) -> None:
        """
        Delete specified item from cache
        """
        self.__items__.__delitem__(index)

    def __setitem__(self, index, value) -> None:
        """
        Set specified value to given index
        """
        self.__items__.__setitem__(index, value)

    def __len__(self) -> int:
        """
        Return size of collection
        """
        return len(self.__items__)

    def clear(self) -> None:
        """
        Reset state. This needs to be called when load errors are handled
        """
        self.__items__ = []

    def __getitem__(self, index) -> Measurement:
        """
        Get specified record by index

        Returns
        -------
        Measurement (or a child class) object
        """
        return self.__items__.__getitem__(index)

    def __parse_time__(self, value):
        """
        Parse time value from log output
        """
        for fmt in self.__date_formats__:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass
        raise ValueError(f'Invalid date: {value}')

    @property
    def last(self) -> Optional[Measurement]:
        """
        Return last measurement or None if no data is loaded
        """
        if len(self):
            return self[-1]
        return None

    def insert(self, index, value) -> None:
        """
        insert item to specific index
        """
        self.__items__.insert(index, value)

    def sort(self) -> None:
        """
        Sort loaded measurement values. Items are stored by date
        """
        self.__items__.sort()

    def filter(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
        """
        Filter records matching specified date range
        """
        if start_time is None and end_time is None:
            return self

        if start_time and not isinstance(start_time, datetime):
            start_time = self.__parse_time__(start_time)
        if end_time and not isinstance(end_time, datetime):
            end_time = self.__parse_time__(end_time)

        matches = []
        for record in self:
            if start_time and record.time < start_time:
                continue
            if end_time and record.time > end_time:
                continue
            matches.append(record)
        return self.clone_from_filtered_records(*matches)

    def load(self, path: str) -> None:
        """
        Load records from a file

        This must be implemented in child class
        """
        raise NotImplementedError('load() must be implemented in child class')
