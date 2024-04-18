import os
from google.cloud import storage

storage_client = storage.Client(project='solutions-engineering')
bucket = storage_client.get_bucket('josh-seldon')
location = 'deployment/models'

for directory in os.listdir(location):
    sub_dir = os.path.join(location, directory)
    if os.path.isdir(sub_dir) and directory != '__pycache__':
        for file in os.listdir(sub_dir):
            if file != '__pycache__':
                print(f'Uploading {directory}/{file}')
                blob = bucket.blob(f'llm/new-rag/{directory}/{file}')
                blob.upload_from_filename(f'./{location}/{directory}/{file}')
