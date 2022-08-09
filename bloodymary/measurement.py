"""
Blood pressure measurement data record
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(order=True)
class Measurement:
    """
    Blood pressure measurement
    """
    time: datetime = field(default_factory=datetime.now)
    systolic: int = None
    diastolic: int = None
    pulse: int = None
    notes: str = None

    def __repr__(self):
        return f'{self.time} {self.systolic}/{self.diastolic} {self.pulse}'
