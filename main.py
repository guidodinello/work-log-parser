import logging

from time_utils import TimeParseError
from work_log_parser import WorkLogParser
from work_log_reporter import WorkLogReporter

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("worklog")


def main():
    import sys

    if len(sys.argv) != 2:
        logger.error("Usage: python script.py <path_to_worklog_file>")
        sys.exit(1)

    try:
        parser = WorkLogParser(logger=logger)
        workdays = parser.parse_file(sys.argv[1])

        reporter = WorkLogReporter(logger=logger)
        reporter.generate_report(workdays)

    except (TimeParseError, FileNotFoundError) as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
