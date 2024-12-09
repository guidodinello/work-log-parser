from dataclasses import dataclass, field
from datetime import datetime, timedelta

from enums import EntryType
from time_utils import TimeRange


@dataclass
class WorkDay:
    """Represents a work day with all its entries"""

    date: datetime
    start_time: TimeRange
    breaks: list[tuple[EntryType, TimeRange]] = field(default_factory=list)

    def calculate_overtime(self) -> float:
        """Calculate total overtime including late start and breaks"""
        # Add start time delay
        total_minutes = (
            self.start_time.actual_end - self.start_time.scheduled_end
        ).total_seconds() / 60
        # Add break overtimes
        total_minutes += sum(time_range.get_overtime() for _, time_range in self.breaks)
        return total_minutes

    def get_expected_out(self, work_hours: float = 9) -> datetime:
        """Calculate expected out time including any overtime"""
        start = self.start_time.start
        expected = start + timedelta(hours=work_hours)
        return expected
