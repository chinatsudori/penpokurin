from datetime import datetime, timedelta
import re
import pytz
from dateutil.relativedelta import relativedelta

dt = datetime
from config import LOG_CHANNEL_ID

async def send_log_message(self, message):
    log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(message)
    else:
        print(f"Log channel {LOG_CHANNEL_ID} not found.")

async def calculate_cb_number(current_date=None, bot=None):
    """
    Calculate the CB number based on the number of months since February 2018.

    :param current_date: The date for which to calculate the CB number (defaults to now)
    :type current_date: datetime, optional
    :return: The current CB number
    :rtype: int
    """
    # Set the starting point (February 2018)
    start_date = datetime(2018, 2, 1)

    # Use the provided date or the current date if none is provided
    if current_date is None:
        current_date = datetime.now()

    # Calculate the number of months since the start date
    months_passed = (current_date.year - start_date.year) * 12 + current_date.month - start_date.month

    # Calculate the current CB number
    cb_number = 1 + months_passed

    if bot:
        await send_log_message(bot, "CB Number Calculated", f"Calculated CB number: {cb_number}")

    return cb_number

async def get_current_time(bot=None):
    current_time = datetime.now()
    if bot:
        await send_log_message(bot, "Current Time Retrieved", f"Current time: {current_time}")
    return current_time

async def get_start_of_next_day(bot=None):
    now = await get_current_time(bot)
    next_run = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    if bot:
        await send_log_message(bot, "Start of Next Day", f"Start of next day: {next_run}")
    return next_run

def get_time_difference(start_time, end_time):
    return (end_time - start_time).total_seconds()

def add_hours_to_time(start_time, hours):
    return start_time + timedelta(hours=hours)

def parse_date(date_str):
    # Assume the current year and set time to 8:00 PM GMT
    current_year = datetime.now().year
    datetime_str = f"{date_str}/{current_year} 20:00"
    return datetime.strptime(datetime_str, "%m/%d/%Y %H:%M").replace(tzinfo=pytz.utc)

def format_date(date):
    return date.strftime("%m/%d/%Y %H:%M")

def get_next_month_date():
    now = datetime.now()
    next_month = (now.month % 12) + 1
    return datetime(now.year, next_month, 1)

def add_days_to_date(date, days):
    return date + timedelta(days=days)

def get_current_utc_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def convert_timestamp_to_iso8601(timestamp):
    return datetime.utcfromtimestamp(timestamp).isoformat()

def extract_timestamp_from_line(line):
    # This function needs to be implemented based on the format of your input data
    # Example: Extract a Unix timestamp from the line (simplified example)
    match = re.search(r"\d{10}", line)  # Regex for a 10-digit timestamp
    if match:
        return int(match.group(0))
    raise ValueError("Timestamp not found in line")

def utc_from_timestamp(timestamp):
    """Convert a Unix timestamp to a UTC datetime object."""
    return datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)

def parse_date_str(date_str):
    """Parse a date string into a timezone-aware datetime object. Handles multiple formats."""
    if date_str is None:
        raise ValueError("Date string is None")

    try:
        # Try parsing ISO 8601 format first
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.replace(tzinfo=pytz.utc)
    except ValueError:
        pass

    try:
        # Try parsing a common format: 'day month year hour:minute'
        dt = datetime.strptime(date_str, '%d %B %Y %H:%M')
        return dt.replace(tzinfo=pytz.utc)
    except ValueError:
        pass

    # Add more formats if needed
    raise ValueError(f"Date format is incorrect: {date_str}")

def iso_format(dt):
    """Return ISO 8601 format of a datetime object."""
    return dt.isoformat()

def parse_duration_from_title(title):
    """Extracts duration in days from the event title."""
    match = re.search(r'\((\d+) days?\)', title)
    if match:
        return int(match.group(1))
    return 0

def calculate_end_time(start_time, duration_days):
    """Calculates the end time of an event based on the start time and duration."""
    return start_time + timedelta(days=duration_days)
