from dataclasses import dataclass
import logging
from azure.storage.blob import BlobServiceClient




LOGGER = logging.getLogger(__name__)
IMAGES_CONTAINER = "miwifischeduler"
DB_FILE = "data.json"

@dataclass
class FileUploadData():
    url: str
    identidier: str

class BlobManager:
    def __init__(self, azure_storage_connection_string) -> None:
        self.blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(azure_storage_connection_string)

        # get file drom blob
        self.blob_service_client.get_container_client(IMAGES_CONTAINER).upload_blob
        if self.blob_service_client.get_blob_client(container=IMAGES_CONTAINER, blob=DB_FILE).exists() is False:
            self.blob_service_client.get_container_client(IMAGES_CONTAINER).upload_blob(DB_FILE, str(dict()))

    def get_db(self) -> dict:
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=IMAGES_CONTAINER, blob=DB_FILE)
            data = blob_client.download_blob().readall().decode("utf-8")
            return eval(data)
        except Exception as e:
            LOGGER.error(e)
            raise e

    def drop_db(self):
        try:
            self.blob_service_client.get_container_client(IMAGES_CONTAINER).delete_blob(DB_FILE)
        except Exception as e:
            LOGGER.error(e)
            raise e

    def set_db(self, db_file: dict):
        try:
            self.upload_data_to_blob(DB_FILE, bytes(str(db_file), "utf-8"))
        except Exception as e:
            LOGGER.error(e)
            raise e
    def upload_file_to_blob(self, file_name: str, file_path: str):
        try:
            with open(file_path, "rb") as data:
                self.upload_data_to_blob(file_name, data)
        except Exception as e:
            LOGGER.error(e)
            raise e

    def upload_data_to_blob(self, file_name: str, file_content: bytes) -> FileUploadData:
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=IMAGES_CONTAINER, blob=file_name)
            blob_client.upload_blob(file_content, overwrite=True)
            f = FileUploadData(blob_client.url, file_name)
            return f
        except Exception as e:
            LOGGER.error(e)
            raise e

if __name__ == "__main__":
    b= BlobManager("DefaultEndpointsProtocol=https;AccountName=miwifischeduler;AccountKey=Ecv3jdmwtMVTsw3MgL5ZXBoakMI5LNmi8b0WFFAb+I0uO9e2jn/RWsP+E6ynlPvH0ohLpyUdYW6J+AStQl+ylg==;EndpointSuffix=core.windows.net")
    d = b.get_db()
    d["test"] = "test3"
    b.set_db(d)
    d = b.get_db()

    pass