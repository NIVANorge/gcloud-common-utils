#!/usr/bin/env python3
"""
Example script demonstrating the metadata functionality in blob_helper_local.py
"""
import os
import tempfile
import shutil
from io import BytesIO
from gcloud_common_utils import blob_helper_local

def test_metadata_functionality():
    # Setup temporary directory
    temp_dir = tempfile.mkdtemp()
    os.environ["LOCAL_STORAGE_PATH"] = temp_dir
    
    try:
        # Test data
        test_content = b"Hello, this is test content!"
        test_metadata = {
            "content-type": "text/plain",
            "custom-field": "custom-value",
            "upload-time": "2025-10-01T12:00:00Z"
        }
        
        bucket_name = "test-bucket"
        blob_name = "test-file.txt"
        
        # Upload blob with metadata
        print("1. Uploading blob with metadata...")
        with BytesIO(test_content) as upload_buffer:
            blob_helper_local.upload_blob(bucket_name, blob_name, upload_buffer, metadata=test_metadata)
        
        # Download blob without metadata
        print("2. Downloading blob without metadata...")
        with BytesIO() as download_buffer:
            result = blob_helper_local.download_blob(bucket_name, blob_name, download_buffer, include_metadata=False)
            download_buffer.seek(0)
            downloaded_content = download_buffer.read()
            print(f"   Downloaded content: {downloaded_content}")
            print(f"   Content matches: {downloaded_content == test_content}")
            print(f"   Return type: {type(result)}")
        
        # Download blob with metadata
        print("3. Downloading blob with metadata...")
        with BytesIO() as download_buffer:
            result = blob_helper_local.download_blob(bucket_name, blob_name, download_buffer, include_metadata=True)
            file_obj, metadata = result
            download_buffer.seek(0)
            downloaded_content = download_buffer.read()
            print(f"   Downloaded content: {downloaded_content}")
            print(f"   Content matches: {downloaded_content == test_content}")
            print(f"   Return type: {type(result)}")
            print(f"   Metadata: {metadata}")
            print(f"   Metadata matches: {metadata == test_metadata}")
        
        # Test blob without metadata
        print("4. Testing blob without metadata...")
        blob_name_no_meta = "test-file-no-meta.txt"
        with BytesIO(test_content) as upload_buffer:
            blob_helper_local.upload_blob(bucket_name, blob_name_no_meta, upload_buffer)  # No metadata
        
        with BytesIO() as download_buffer:
            result = blob_helper_local.download_blob(bucket_name, blob_name_no_meta, download_buffer, include_metadata=True)
            file_obj, metadata = result
            print(f"   Metadata for blob without metadata: {metadata}")
            print(f"   Metadata is None: {metadata is None}")
            
    finally:
        # Clean up
        shutil.rmtree(temp_dir)
        print("5. Cleanup completed")

if __name__ == "__main__":
    test_metadata_functionality()