import os
import sys
from google.cloud import storage

# Check if the user name argument is provided
if len(sys.argv) < 2:
    print("Usage: python script_name.py [YOUR_NAME]")
    sys.exit(1)

user_name = sys.argv[1]

storage_client = storage.Client(project='solutions-engineering')
bucket = storage_client.get_bucket('josh-seldon')
location = 'models'

for directory in os.listdir(location):
    sub_dir = os.path.join(location, directory)
    if os.path.isdir(sub_dir) and directory != '__pycache__':
        for file in os.listdir(sub_dir):
            if file != '__pycache__':
                print(f'Uploading {directory}/{file}')
                blob = bucket.blob(f'llm/chat-memory/{user_name}/{directory}/{file}')
                blob.upload_from_filename(f'./{location}/{directory}/{file}')
