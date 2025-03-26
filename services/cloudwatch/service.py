import json
from datetime import datetime, timezone
from utils.helper import one_day_range, generate_filename
from settings.config import CONFIG, SESSION
class CloudWatchService():

    # Set the log group and stream (Modify these values)
    RDS_LOG_GROUP = CONFIG.AWS_RDS_LOG_GROUP
    LOG_STREAM_NAME = None  # Optional, can be None to fetch all streams
    LOCAL_LOG_PATH = "logs/"

    def __init__(self):
        self.cloudwatch = SESSION.BOTO3.client("logs")

    def get_log_events(self, log_group, start_time, end_time):
        """Fetch CloudWatch log events with pagination."""
        
        kwargs = {
            "logGroupName": log_group,
            "startTime": start_time,
            "endTime": end_time,
            "limit": 10000,
        }

        all_logs = []
        while True:
            response = self.cloudwatch.filter_log_events(**kwargs)
            all_logs.extend(response.get("events", []))

            next_token = response.get("nextToken")
            if not next_token:
                break
            kwargs["nextToken"] = next_token
        
        error_logs = [event for event in all_logs if not (":LOG:" in event["message"] or ":FATAL:" in event["message"])]

        return error_logs

    def group_logs_by_timestamp(self, logs, round_to='second'):
        grouped_logs = {}

        for log in logs:
            timestamp = int(log["timestamp"])  # CloudWatch timestamps are in milliseconds
            dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)

            # Round timestamp for grouping
            if round_to == 'second':
                rounded_ts = dt.replace(microsecond=0)
            elif round_to == 'minute':
                rounded_ts = dt.replace(second=0, microsecond=0)
            else:
                rounded_ts = dt  # No rounding

            str_timestamp = rounded_ts.isoformat()

            if str_timestamp not in grouped_logs:
                grouped_logs[str_timestamp] = []

            grouped_logs[str_timestamp].append(log["message"])

        return grouped_logs
    
    def save_logs_to_local(self, logs, local_path):
        with open(local_path, "w") as f:
            json.dump( logs, f, indent=4)

        print(f"saved logs on {local_path}")

        return

    def process_rds_logs(self, start_time, end_time):
        
        logs = self.get_log_events(self.RDS_LOG_GROUP, start_time, end_time)
        grouped_logs = self.group_logs_by_timestamp(logs)
        
        local_path = self.LOCAL_LOG_PATH + generate_filename("json")
        self.save_logs_to_local(grouped_logs, local_path)

        return local_path
    
    def process_daily_rds_logs(self):
        start_time, end_time = one_day_range()
        local_path = self.process_rds_logs(start_time, end_time)

        return local_path
        

