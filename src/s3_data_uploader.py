import logging
import boto3
from botocore.exceptions import ClientError
import os
from text_cleaner import TextCleaner
import spacy
import csv


class S3DataUploader:
    def __init__(self, region):
        self.region = region
        self.s3_client = boto3.client('s3', region_name=self.region)

    def create_s3_bucket(self, bucket_name):
        location = {'LocationConstraint': self.region}
        print("creating bucket in region:", self.region)

        try:
            if self.region == 'us-east-1':
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            print(f"Bucket '{bucket_name}' created successfully in region '{self.region}'.")
        except Exception as e:
            print(f"Error creating bucket '{bucket_name}': {e}")

    def clean_n_upload_tos3(self, data_files_dir, url_to_file_map, bucket_name=None, common_sentences=None,
                            clean_data_dir="clean_data"):
        with open(f"{data_files_dir}/{url_to_file_map}", "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            url_to_file_map = {rows[0]: rows[1] for rows in reader}

        for filename in url_to_file_map.values():
            data_files_path = "./" + filename

            if common_sentences is not None:
                nlp = spacy.load("en_core_web_lg")
                cleaner = TextCleaner(common_sentences, nlp)

                with open(data_files_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    cleaned_text = cleaner.remove_common_sentences(text)
                    print(f"{data_files_path}: successfully cleaned")

                clean_data_files_dir = data_files_dir + "/" + clean_data_dir
                if not os.path.exists(clean_data_files_dir):
                    os.makedirs(clean_data_files_dir)

                data_files_path = clean_data_files_dir + "/" + "/".join(filename.strip("/").split('/')[1:])
                with open(data_files_path, "w+", encoding="utf-8") as f:
                    f.write(cleaned_text)
                    print(f"{data_files_path}: temporarily saved to disk")

            if bucket_name is not None:
                object_name = filename
                s3 = boto3.client('s3')
                with open(data_files_path, "rb") as f:
                    try:
                        s3.upload_fileobj(f, bucket_name, object_name)
                        print(f'{filename}: Successfully uploaded to {bucket_name} S3 Bucket')
                    except ClientError as e:
                        logging.error(e)
                        return print(f"Failed to upload {filename} to S3 Bucket")

        return print(f"All files uploaded to S3 Bucket {bucket_name}")
