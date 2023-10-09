import boto3
import json
import logging

from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
s3 = boto3.client("s3")


class Metadata(BaseModel):
    version: str = Field(..., title="Name")


def validate_delivery_pipeline():
    metadata = get_metadata()
    metadata_s3 = get_metadata_s3()

    if metadata.version != metadata_s3.version:
        logging.info(
            f"------------------------------------ A NEW VERSION IS AVAILABLE: {metadata_s3.version} ------------------------------------")


def get_metadata() -> Metadata:
    event_file_name = ".circleci/metadata/metadata.json"
    with open(event_file_name, "r", encoding="UTF-8") as file_metadata:
        return Metadata(**json.load(file_metadata))


def get_metadata_s3() -> Metadata:
    s3.download_fileobj("testcduartebucket", "metadata.json", open("metada_s3.json", "wb"))

    with open("metada_s3.json", "r") as file_metada_s3:
        return Metadata(**json.load(file_metada_s3))


# if __name__ == '__main__':
validate_delivery_pipeline()
