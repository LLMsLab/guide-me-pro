#import DataUploader class from data_uploader module
from s3_data_uploader import S3DataUploader

#specify parameters to use
# Bucket creation function arguments
bucket_name = 'nyl-pubsite-data'
region = 'us-east-1'

# Uploading to S3 function arguments
data_files_dir = "./data" 
url_to_file_map = "url_to_file_map.csv"
common_sentences = None  #set to none if you do not wish to clean the data
clean_data_dir = "clean"


#provide a list of common sentences to use for cleaning the data 
# common_sentences = [
#     "Understand what people like you typically consider when making their plans",
#     "Being prepared looks different across all phases of life",
#     "Account How-To Videos",
#     "Contact Us We're here to listen: 1 (800) CALL-NYL Monday – Friday",
#     "Receive resources & tools that can help you prepare for the future",
#     "You can cancel anytime",
# ]


#instantiate object of class S3DataUploader
data_uploader = S3DataUploader(region=region)
#create an S3 bucket
data_uploader.create_s3_bucket(bucket_name=bucket_name)
#upload data to the S3 bucket created
data_uploader.clean_n_upload_tos3(data_files_dir=data_files_dir,  url_to_file_map=url_to_file_map, bucket_name=bucket_name, common_sentences=common_sentences, clean_data_dir=clean_data_dir)