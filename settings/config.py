import os
from dotenv import load_dotenv
import boto3

load_dotenv()

class Config():
    ENV = os.getenv("ENV")


    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    
    AWS_RDS_LOG_GROUP = os.getenv("AWS_RDS_LOG_GROUP")
    AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

CONFIG = Config()

class Session():
    BOTO3 = boto3.Session(
        aws_access_key_id=CONFIG.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=CONFIG.AWS_SECRET_ACCESS_KEY,
        region_name=CONFIG.AWS_REGION
    )

SESSION = Session()