from datetime import datetime

from src.custom_types import Logger
from src.enums import EntryType
from src.parser_utils import BreakEntryParser, LogEntryParser, StartEntryParser
from src.time_utils import TimeRange
from src.work_utils import WorkDay


class WorkLogParser:
    """Main parser class that coordinates parsing of work log files"""

    def __init__(self, logger: Logger):
        self.logger = logger
        self.parsers: list[LogEntryParser] = [StartEntryParser(), BreakEntryParser()]

    def parse_line(
        self, line: str, base_date: None | datetime = None
    ) -> None | tuple[EntryType, TimeRange]:
        """Parse a single line using appropriate parser"""
        line = line.strip()
        if not line:
            return None

        for parser in self.parsers:
            if parser.can_parse(line):
                return parser.parse(line, base_date)
        return None

    def parse_file(self, file_path: str) -> list[WorkDay]:
        """Parse entire work log file"""
        workdays: list[WorkDay] = []
        current_day = None

        try:
            with open(file_path, "r") as file:
                for line in file:
                    result = self.parse_line(
                        line, current_day.date if current_day else None
                    )
                    if not result:
                        continue

                    entry_type, time_range = result

                    if entry_type == EntryType.START:
                        if current_day:
                            workdays.append(current_day)
                        current_day = WorkDay(
                            date=time_range.scheduled_end, start_time=time_range
                        )
                    elif current_day and entry_type in (
                        EntryType.BREAK,
                        EntryType.LUNCH,
                    ):
                        current_day.breaks.append((entry_type, time_range))

                if current_day:
                    workdays.append(current_day)

            return workdays

        except FileNotFoundError:
            self.logger.error(f"Could not find file: {file_path}")
            raise
