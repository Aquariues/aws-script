from settings.config import CONFIG, SESSION
from utils.helper import generate_date_based_path

class S3Service():
    EXPIRATION_TIME = 12 * 60 * 60  # 12 hours in seconds
    RDS_LOG_PATH = "RDS/LOGS/"
    def __init__(self):
        self.s3 = SESSION.BOTO3.client("s3")
        self.bucket = CONFIG.AWS_S3_BUCKET_NAME

    def upload_file(self, file_path, s3_key):
        try:
            self.s3.upload_file(file_path, self.bucket, s3_key)
            print(f"File uploaded successfully to s3://{self.bucket}/{s3_key}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def upload_rds_logs(self, file_path):
        s3_key = self.RDS_LOG_PATH + generate_date_based_path("json")
        self.upload_file(file_path, s3_key)

        return s3_key

    def generate_presigned_url(self, object_key, expiration=EXPIRATION_TIME):
        """Generate a pre-signed S3 URL valid for a given expiration time."""
        url = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": object_key},
            ExpiresIn=expiration
        )

        return url