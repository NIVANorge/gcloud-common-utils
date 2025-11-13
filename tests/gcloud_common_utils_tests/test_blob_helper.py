import os
import shutil
import logging
from io import BytesIO
import random

import pytest

from gcloud_common_utils import blob_helper_local


@pytest.fixture
def make_and_delete_temp_folder(monkeypatch, caplog):
    caplog.set_level(logging.INFO)
    tmp_folder = f"/tmp/stream-data{random.randint(1,1000)}"
    monkeypatch.setenv("LOCAL_STORAGE_PATH", tmp_folder)
    os.makedirs(tmp_folder, exist_ok=True)
    yield
    shutil.rmtree(tmp_folder)


def test_local_blob_helper_upload_and_download(make_and_delete_temp_folder):
    byte_string = b'yada yada yada\nmore yadas!!\n'

    with BytesIO() as some_bytes:
        some_bytes.write(byte_string)
        blob_helper_local.upload_blob('a_test_bucket', 'a_test_file.txt', some_bytes)

    with BytesIO() as receiving_buffer:
        blob_helper_local.download_blob('a_test_bucket', 'a_test_file.txt', receiving_buffer)
        receiving_buffer.seek(0)
        assert receiving_buffer.read() == byte_string


def test_local_blob_helper_metadata(make_and_delete_temp_folder):
    """Test metadata upload and download functionality"""
    byte_string = b'test content with metadata'
    test_metadata = {
        "content-type": "text/plain",
        "custom-field": "test-value",
        "upload-time": "2025-10-01T12:00:00Z",
        "x-goog-meta-up-app-user": "test@niva.no",
        "x-goog-meta-up-app-processing-type": 'Marine',
        "x-goog-meta-up-app-instrument": 'Cary300',
        "x-goog-meta-up-app-has-metadata-file": "True"
    }

    # Upload blob with metadata
    with BytesIO() as upload_buffer:
        upload_buffer.write(byte_string)
        blob_helper_local.upload_blob('test_bucket', 'test_file_with_metadata.txt', upload_buffer, metadata=test_metadata)

    # Download blob with metadata
    with BytesIO() as download_buffer:
        result = blob_helper_local.download_blob('test_bucket', 'test_file_with_metadata.txt', download_buffer, include_metadata=True)
        file_obj, metadata = result
        download_buffer.seek(0)
        downloaded_content = download_buffer.read()
        
        assert downloaded_content == byte_string
        assert metadata == test_metadata
        assert isinstance(result, tuple)
        assert len(result) == 2

    # Download blob without metadata
    with BytesIO() as download_buffer:
        result = blob_helper_local.download_blob('test_bucket', 'test_file_with_metadata.txt', download_buffer, include_metadata=False)
        download_buffer.seek(0)
        downloaded_content = download_buffer.read()
        
        assert downloaded_content == byte_string
        assert not isinstance(result, tuple)  # Should return just the file object


def test_local_blob_helper_no_metadata(make_and_delete_temp_folder):
    """Test download when no metadata exists"""
    byte_string = b'test content without metadata'

    # Upload blob without metadata
    with BytesIO() as upload_buffer:
        upload_buffer.write(byte_string)
        blob_helper_local.upload_blob('test_bucket', 'test_file_no_metadata.txt', upload_buffer)

    # Download blob with metadata flag (should return None for metadata)
    with BytesIO() as download_buffer:
        result = blob_helper_local.download_blob('test_bucket', 'test_file_no_metadata.txt', download_buffer, include_metadata=True)
        file_obj, metadata = result
        download_buffer.seek(0)
        downloaded_content = download_buffer.read()
        
        assert downloaded_content == byte_string
        assert metadata is None
        assert isinstance(result, tuple)
        assert len(result) == 2


def test_delete_blob_with_metadata(make_and_delete_temp_folder):
    """Test that deleting a blob also removes its metadata"""
    byte_string = b'test content for deletion'
    test_metadata = {"test": "metadata"}

    # Upload blob with metadata
    with BytesIO() as upload_buffer:
        upload_buffer.write(byte_string)
        blob_helper_local.upload_blob('test_bucket', 'test_file_delete.txt', upload_buffer, metadata=test_metadata)

    # Verify files exist
    blob_path = blob_helper_local._get_path('test_bucket', 'test_file_delete.txt')
    metadata_path = blob_helper_local._get_metadata_path('test_bucket', 'test_file_delete.txt')
    
    assert os.path.exists(blob_path)
    assert os.path.exists(metadata_path)

    # Delete blob
    blob_helper_local.delete_blob('test_bucket', 'test_file_delete.txt')

    # Verify both files are deleted
    assert not os.path.exists(blob_path)
    assert not os.path.exists(metadata_path)
