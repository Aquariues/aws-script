import os
from services.cloudwatch.service import CloudWatchService
from services.s3.service import S3Service
from services.slack.push_message import send_slack_message
from utils.helper import one_day_range, convert_to_readable_time
from settings.config import CONFIG

class AWSJob():

    def __init__(self):
        self.cloudwatch = CloudWatchService()
        self.s3 = S3Service()

    def tracking_rds_error_logs(self, start_time, end_time):
        local_path, total_error = self.cloudwatch.process_rds_logs(start_time, end_time)
        s3_key = self.s3.upload_rds_logs(local_path)
        s3_url = self.s3.generate_presigned_url(s3_key)
        
        if os.path.exists(local_path):
            os.remove(local_path)
            
        return s3_url, total_error
    

    def daily_tracking_rds_error_logs(self):
        message = ":fcb: ---*FCB RDS Daily Tracking*--- :fcb:"
        start_time, end_time = one_day_range()
        s3_url, total_error = self.tracking_rds_error_logs(start_time, end_time)
        
        if total_error > 0:
            formated_message = self.format_message(start_time, end_time, message, s3_url, total_error)
            send_slack_message(formated_message)

        return
        
    def format_message(self, start_time, end_time, message, s3_url, total_error):
        start_date = convert_to_readable_time(start_time)
        end_date = convert_to_readable_time(end_time)

        return f"""{message}\n\nENV: {CONFIG.ENV}\n\nTime Range: {start_date} - {end_date}\n\nError raised {total_error} times\n\nDownload Report: {s3_url}\n\n{message}"""