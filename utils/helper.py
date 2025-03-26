import uuid
from datetime import datetime, timezone, timedelta

def one_day_range():
    # Define UTC+7 timezone offset
    utc7_offset = timedelta(hours=7)

    end_time_utc7 = datetime.now(timezone.utc).astimezone(timezone.utc) + utc7_offset
    end_time_utc7 = end_time_utc7.replace(hour=0, minute=0, second=0, microsecond=0)

    end_time = int(end_time_utc7.astimezone(timezone.utc).timestamp() * 1000)
    start_time = end_time - (24 * 60 * 60 * 1000)

    return start_time, end_time

def convert_to_readable_time(timestamp_ms):
    utc7_offset = timedelta(hours=7)
    dt_utc = datetime.utcfromtimestamp(timestamp_ms / 1000)  # Convert to seconds
    dt_utc7 = dt_utc.replace(tzinfo=timezone.utc) + utc7_offset  # Convert to UTC+7
    return dt_utc7.strftime("%Y-%m-%d %H:%M:%S %Z (UTC+7)")

def generate_date_based_path(extension="txt"):
    now = datetime.now()

    return f"{now.year}/{str(now.month).zfill(2)}/{str(now.day).zfill(2)}.{extension}"

def generate_filename(extension="txt"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_id = uuid.uuid4().hex[:6]  

    return f"{timestamp}_{random_id}.{extension}"