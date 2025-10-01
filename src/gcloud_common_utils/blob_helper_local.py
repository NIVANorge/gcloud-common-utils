import os
import glob
import json
import logging
import datetime as dt
import shutil
from typing import Set, Optional, Dict, Any, Union, Tuple
from io import IOBase
from typeguard import typechecked


TEMP_BUCKET_NAME = "temp_file_upload"


def _get_path(bucket_name, file_path) -> str:
    root_dir = os.path.join(os.environ["LOCAL_STORAGE_PATH"], bucket_name)
    return os.path.join(root_dir, file_path)


def _get_metadata_path(bucket_name, file_path) -> str:
    """Get the path for the metadata file corresponding to a blob."""
    blob_path = _get_path(bucket_name, file_path)
    return blob_path + ".metadata.json"


def _save_metadata(bucket_name: str, file_path: str, metadata: Optional[Dict[str, Any]]):
    """Save metadata for a blob to a JSON file."""
    if metadata is None:
        return
    
    metadata_path = _get_metadata_path(bucket_name, file_path)
    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
    
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)


def _load_metadata(bucket_name: str, file_path: str) -> Optional[Dict[str, Any]]:
    """Load metadata for a blob from a JSON file."""
    metadata_path = _get_metadata_path(bucket_name, file_path)
    
    if not os.path.exists(metadata_path):
        return None
    
    try:
        with open(metadata_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logging.warning(f"Failed to load metadata from {metadata_path}: {e}")
        return None


@typechecked
def upload_blob(bucket_name: str, destination_blob_name: str, file_like_object, metadata: Optional[Dict[str, Any]] = None):
    """
    writes files to local filesystem instead of cloud storage. Intended for local dev usage
    Also publishes a message to pubsub using the
    topic_name <bucket-name>-updates as a convention (emulating storage notifications)
    """
    logging.info(f"Writing file={destination_blob_name} to local filesystem")
    _, filename = os.path.split(destination_blob_name)

    # Appending microsecond timestamp to filename for uniqueness in temp folder
    file_path = _get_path(TEMP_BUCKET_NAME, filename + dt.datetime.now().strftime('_%H_%M_%S_%f'))
    logging.debug(f"Writing first to a temporary location {file_path}")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as file:
        file_like_object.seek(0)
        shutil.copyfileobj(file_like_object, file)

    destination_path = _get_path(bucket_name, destination_blob_name)
    logging.debug(f"Moving to final destination {destination_path}")
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    os.rename(file_path, destination_path)
    
    # Save metadata if provided
    if metadata is not None:
        _save_metadata(bucket_name, destination_blob_name, metadata)


@typechecked
def list_blobs(bucket_name: str, prefix: str) -> Set[str]:
    """Lists files from local filesystem instead of cloud storage. Intended for local dev usage. Should imitate
    Google's list_blobs cloud storage function"""
    path = _get_path(bucket_name, prefix)
    paths = glob.glob(path + '*', recursive=True)

    logging.info(f"Found {len(paths)} existing files in local directory {path}")

    return set(os.path.split(path)[1] for path in paths)


def blob_exists(bucket_name: str, partial_file_path: str) -> bool:
    logging.info(f"Checking if file={partial_file_path} exists in dir={bucket_name}")
    # partial_file_path can also be a full file name, the glob will work correctly
    path = _get_path(bucket_name, f'{partial_file_path}*')
    return any(os.path.isfile(file) for file in glob.glob(path))


@typechecked
def download_blob(bucket_name: str, source_blob_name: str, file_like_object: IOBase, include_metadata: bool = False) -> Union[IOBase, Tuple[IOBase, Optional[Dict[str, Any]]]]:
    """
    Downloads a blob from the local filesystem (mimicking cloud storage behavior).
    
    Args:
        bucket_name (str): Name of the bucket.
        source_blob_name (str): Name of the blob to download.
        file_like_object: A file-like object to write the blob's contents to.
        include_metadata (bool, optional): If True, also returns the blob's metadata. Defaults to False.
    
    Returns:
        file_like_object: The file-like object containing the downloaded data.
        If include_metadata is True, returns a tuple (file_like_object, metadata), where metadata may be None if the blob has no metadata.
    """
    path = _get_path(bucket_name, source_blob_name)
    logging.info(f"Reading local file {path}")
    with open(path, "rb") as file:
        shutil.copyfileobj(file, file_like_object)
    
    if include_metadata:
        metadata = _load_metadata(bucket_name, source_blob_name)
        return file_like_object, metadata
    
    return file_like_object


@typechecked
def delete_blob(bucket_name: str, destination_blob_name: str):
    file_path = _get_path(bucket_name, destination_blob_name)
    logging.info(f"Deleting file={file_path} from local filesystem")
    os.remove(file_path)
    
    # Also remove metadata file if it exists
    metadata_path = _get_metadata_path(bucket_name, destination_blob_name)
    if os.path.exists(metadata_path):
        os.remove(metadata_path)
        logging.debug(f"Deleted metadata file {metadata_path}")
