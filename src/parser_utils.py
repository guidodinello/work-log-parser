import re
from abc import ABC, abstractmethod
from datetime import datetime

from src.enums import EntryType
from src.time_utils import TimeParseError, TimeParser, TimeRange


class LogEntryParser(ABC):
    """Abstract base class for parsing different types of log entries"""

    @abstractmethod
    def can_parse(self, line: str) -> bool:
        pass

    @abstractmethod
    def parse(
        self, line: str, base_date: None | datetime = None
    ) -> tuple[EntryType, TimeRange]:
        pass


class StartEntryParser(LogEntryParser):
    """Parses work day start entries"""

    PATTERN = re.compile(
        r"(\d{2}/\d{2})\s*-\s*(\d{1,2}:\d{2})\s*(?:\((\d{1,2}:\d{2})\))?\s*in\."
    )

    def can_parse(self, line: str) -> bool:
        return bool(self.PATTERN.match(line))

    def parse(
        self, line: str, base_date: None | datetime = None
    ) -> tuple[EntryType, TimeRange]:
        match = self.PATTERN.match(line)
        if not match:
            raise TimeParseError("Invalid start entry format")

        date = TimeParser.parse_date(match.group(1))
        scheduled_start = TimeParser.parse_time(match.group(2), date)
        actual_start = (
            TimeParser.parse_time(match.group(3), date)
            if match.group(3)
            else scheduled_start
        )

        return EntryType.START, TimeRange(
            start=scheduled_start,
            scheduled_end=scheduled_start,
            actual_end=actual_start,
        )


class BreakEntryParser(LogEntryParser):
    """Parses break entries"""

    PATTERN = re.compile(
        r"\s*(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})\s*(?:\((\d{1,2}:\d{2})\))?\s*(break|lunch)\."
    )

    def can_parse(self, line: str) -> bool:
        return bool(self.PATTERN.match(line))

    def parse(
        self, line: str, base_date: None | datetime = None
    ) -> tuple[EntryType, TimeRange]:
        if not base_date:
            raise TimeParseError("Base date required for break entries")

        match = self.PATTERN.match(line)
        if not match:
            raise TimeParseError("Invalid break entry format")

        start = TimeParser.parse_time(match.group(1), base_date)

        entry_type = EntryType.LUNCH if match.group(4) == "lunch" else EntryType.BREAK

        if entry_type == EntryType.BREAK:
            scheduled_end = start
            actual_end = TimeParser.parse_time(match.group(2), base_date)
        elif entry_type == EntryType.LUNCH:
            scheduled_end = TimeParser.parse_time(match.group(2), base_date)
            actual_end = (
                TimeParser.parse_time(match.group(3), base_date)
                if match.group(3)
                else scheduled_end
            )
        else:
            raise

        return entry_type, TimeRange(
            start=start,
            scheduled_end=scheduled_end,
            actual_end=actual_end,
        )
