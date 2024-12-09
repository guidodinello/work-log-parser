from dataclasses import dataclass
from datetime import datetime


class TimeParseError(Exception):
    """Custom exception for time parsing errors"""

    pass


@dataclass(frozen=True, slots=True)
class TimeRange:
    """Represents a time period with scheduled and actual times"""

    # in          format: 09:00         (09:15)
    # break       format: 09:00 - 09:05
    # lunch       format: 09:00 - 10:00 (10:05)
    #                     start - s_end (a_end)
    start: datetime
    scheduled_end: datetime
    actual_end: datetime

    def get_overtime(self) -> float:
        """Calculate overtime in minutes"""
        return (self.actual_end - self.scheduled_end).total_seconds() / 60  # type: ignore


class TimeFormatter:
    """Handles time string formatting"""

    @staticmethod
    def format_timedelta(minutes: float) -> str:
        hours, mins = divmod(minutes, 60)
        return f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

    @staticmethod
    def format_time(dt: datetime) -> str:
        return dt.strftime("%H:%M")


class TimeParser:
    """Handles parsing of time strings"""

    @staticmethod
    def parse_time(time_str: str, base_date: None | datetime = None) -> datetime:
        try:
            time = datetime.strptime(time_str.strip(), "%H:%M")
            if base_date:
                return base_date.replace(hour=time.hour, minute=time.minute)
            return time
        except ValueError:
            raise TimeParseError(f"Invalid time format: {time_str}. Expected HH:MM")

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        try:
            current_year = datetime.now().year
            return datetime.strptime(f"{date_str}/{current_year}", "%d/%m/%Y")
        except ValueError:
            raise TimeParseError(f"Invalid date format: {date_str}. Expected DD/MM")
