import os

class S3Sync:

    def sync_folder_to_s3(self, folder, bucket_url):
        command = f"aws s3 sync {folder} {bucket_url}"
        os.system(command)

    def sync_file_from_s3(self, folder, aws_bucket_url):
        command = f"aws s3 sync {aws_bucket_url} {folder}"
        os.system(command)