import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv

class BlobHelper:
    data_container="whystars-data"

    def __init__(self, connect_str):
        self.blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    def upload_file(self, file_path, upload_folder_name=None):
        blob_name = f"{upload_folder_name}/{os.path.basename(file_path)}" if upload_folder_name else os.path.basename(file_path)
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.data_container, blob=blob_name)
            print("Uploading to Azure Storage as blob:\n\t" + file_path)
            # Upload the created file
            with open(file=file_path, mode="rb") as data:
                blob_client.upload_blob(data)
        except Exception as ex:
            print('Exception:')
            print(ex)

    def upload_folder(self, folder_path, upload_folder_name=None):
        for root, dirs, files in os.walk(folder_path):
            if files:
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_file_path = os.path.relpath(file_path, folder_path)
                    rel_path_dir = os.path.dirname(rel_file_path)
                    if rel_path_dir =="": # if file is in the root of the folder
                        self.upload_file(file_path, upload_folder_name)

                    blob_name = f"{upload_folder_name}/{rel_path_dir}" if upload_folder_name else rel_path_dir
                    self.upload_file(file_path, blob_name)

    def list_blobs(self, container_name):
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            print(f"Listing blobs in container: {container_name}")
            blob_list = container_client.list_blobs()
            for blob in blob_list:
                print("\t" + blob.name)
        except Exception as ex:
            print('Exception:')
            print(ex)