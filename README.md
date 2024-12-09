# Work Log Parser

A Python tool for parsing and analyzing work logs to track working hours, breaks, and calculate overtime.

## Overview

This tool processes work log files containing daily work entries including start times, breaks, and lunch periods. It calculates overtime, expected end times, and provides a formatted summary report.

## Usage

```bash
python main.py <path_to_worklog_file>
```

## Work Log Format

The work log file should contain daily entries in the following formats:

### Start of Day Entry

```
DD/MM - HH:MM [(HH:MM)] in.
```

-   `DD/MM`: Date in day/month format
-   First `HH:MM`: Scheduled start time
-   Optional `(HH:MM)`: Actual start time if different from scheduled
-   Must end with "in."

Examples:

```
09/12 - 09:00 (09:15) in.    # Late start
10/11 - 08:00 in.            # On-time start
```

### Break Entry

```
HH:MM - HH:MM break.
```

-   First `HH:MM`: Break start time
-   Second `HH:MM`: Break end time
-   Must end with "break."

Example:

```
10:00 - 10:05 break.
```

### Lunch Entry

```
HH:MM - HH:MM [(HH:MM)] lunch.
```

-   First `HH:MM`: Lunch start time
-   Second `HH:MM`: Scheduled lunch end time
-   Optional `(HH:MM)`: Actual lunch end time if different from scheduled
-   Must end with "lunch."

Examples:

```
12:00 - 13:00 (13:05) lunch.    # Extended lunch
12:00 - 13:00 lunch.            # Regular lunch
```

## Output Format

The tool generates a formatted report with the following information:

### Daily Summary

For each day:

-   Date
-   Logged start time with actual start if different
-   Break and lunch periods with overtime calculations
-   Expected end time based on standard 9-hour workday
-   Daily overtime/debt calculation

Example daily output:

```
📊 Work Log Summary

▸ Date: 09/12
    Logged start: 09:00 [Actual start: 09:15] (15m debt)
    • break: 10:00 - 10:05
    • lunch: 12:00 - 13:00 [ended 13:05] (5m debt)
    Expected out: 18:00 (+20m for 0 day debt) 18:20
```

### Overall Summary

After all daily entries, an overall summary is provided showing accumulated time:

```
📈 Overall Summary
Total accumulated time debt: +1h 45m
```

or

```
📈 Overall Summary
Total accumulated time credit: -30m
```

## Time Calculations

-   Standard workday is 9 hours
-   Overtime is calculated for:
    -   Late starts
    -   Extended breaks
    -   Extended lunches
-   All overtime is accumulated to:
    -   Adjust the expected end time for each day
    -   Calculate total time debt/credit across all logged days

## Error Handling

The tool will report errors for:

-   Invalid time formats (expected HH:MM)
-   Invalid date formats (expected DD/MM)
-   Missing or malformed log entries
-   File not found
