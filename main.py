import argparse
from jobs.aws_job import AWSJob

def main():
    parser = argparse.ArgumentParser(description="Run CloudWatch tasks.")
    parser.add_argument("--task", choices=["daily_tracking_rds"], required=True, help="Choose a task to run")

    args = parser.parse_args()
    aws_job = AWSJob()

    if args.task == "daily_tracking_rds":
        aws_job.daily_tracking_rds_error_logs()

if __name__ == "__main__":
    main()

