from src.custom_types import Logger
from src.time_utils import TimeFormatter
from src.work_utils import WorkDay


class WorkLogReporter:
    """Handles formatting and displaying work log summaries"""

    def __init__(self, logger: Logger):
        self.logger = logger

    def generate_report(self, workdays: list[WorkDay]) -> None:
        self.logger.info("\n📊 Work Log Summary")
        total_overtime = 0

        for day in workdays:
            self.logger.info(f"\n▸ Date: {day.date.strftime('%d/%m')}")

            actual_start = f"\t[Actual start: {TimeFormatter.format_time(day.start_time.actual_end)}]"

            delay = int(
                (
                    day.start_time.actual_end - day.start_time.scheduled_end
                ).total_seconds()
                / 60
            )
            balance = f"({delay}m debt)" if delay else ""

            msg = f"\tLogged start: {TimeFormatter.format_time(day.start_time.start)} {actual_start} {balance}"
            self.logger.info(msg)

            # Report breaks
            for entry_type, break_time in day.breaks:
                actual_end = (
                    f"[ended {TimeFormatter.format_time(break_time.actual_end)}]"
                    if break_time.actual_end
                    else ""
                )
                overtime = break_time.get_overtime()
                status = (
                    f"({abs(int(overtime))}m {'debt' if overtime > 0 else 'credit'})"
                    if overtime != 0
                    else ""
                )

                self.logger.info(
                    f"\t• {entry_type.value}: {TimeFormatter.format_time(break_time.start)} -"
                    f" {TimeFormatter.format_time(break_time.scheduled_end)}"
                    f" {actual_end}"
                    f" {status}"
                )

            # Report expected out time
            expected_out = day.get_expected_out()
            overtime = int(day.calculate_overtime())

            total_overtime += overtime

            if overtime < 0:
                overtime_type = "credit"
                sign = "-"
            else:
                overtime_type = "debt"
                sign = "+"
            extra = (
                f"({sign}{abs(overtime)}m for 0 day {overtime_type})"
                if overtime != 0
                else ""
            )
            actual_expected_out = day.get_expected_out(work_hours=9 + overtime / 60)
            self.logger.info(
                f"\tExpected out: {TimeFormatter.format_time(expected_out)}"
                f" {extra}"
                f" {TimeFormatter.format_time(actual_expected_out
            )}"
            )

        self.logger.info("\n📈 Overall Summary")
        if total_overtime < 0:
            summary_type = "credit"
            sign = "-"
        else:
            summary_type = "debt"
            sign = "+"

        hours, minutes = divmod(abs(total_overtime), 60)
        time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

        self.logger.info(f"Total accumulated time {summary_type}: {sign}{time_str}")
