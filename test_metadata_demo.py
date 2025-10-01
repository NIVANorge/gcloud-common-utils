#!/usr/bin/env python3
"""
Demo script showing the metadata functionality of blob_helper_local.
This demonstrates how the local blob helper can now mimic cloud storage metadata behavior.
"""

import os
import tempfile
import shutil
from io import BytesIO
from gcloud_common_utils import blob_helper_local


def demo_metadata_functionality():
    """Demonstrate the metadata functionality."""
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Set the environment variable for local storage
        os.environ["LOCAL_STORAGE_PATH"] = tmp_dir
        
        print("🚀 Demo: Blob Helper Local with Metadata Support")
        print("=" * 50)
        
        # Test data
        bucket_name = "demo-bucket"
        blob_name = "demo-file.txt"
        content = b"Hello, this is demo content for testing metadata!"
        
        # Metadata to attach to the blob
        metadata = {
            "author": "demo-user",
            "created_by": "metadata_demo",
            "content_type": "text/plain",
            "custom_field": "some_value",
            "timestamp": "2025-10-01T12:00:00Z"
        }
        
        print(f"📦 Uploading blob '{blob_name}' to bucket '{bucket_name}'")
        print(f"📋 With metadata: {metadata}")
        
        # Upload blob with metadata
        with BytesIO(content) as upload_buffer:
            blob_helper_local.upload_blob(bucket_name, blob_name, upload_buffer, metadata=metadata)
        
        print("✅ Upload complete!")
        
        # Download blob without metadata
        print(f"\n📥 Downloading blob without metadata...")
        with BytesIO() as download_buffer:
            result = blob_helper_local.download_blob(bucket_name, blob_name, download_buffer, include_metadata=False)
            download_buffer.seek(0)
            downloaded_content = download_buffer.read()
            
        print(f"📄 Downloaded content: {downloaded_content.decode()}")
        print(f"🔍 Return type: {type(result)}")
        
        # Download blob with metadata
        print(f"\n📥 Downloading blob with metadata...")
        with BytesIO() as download_buffer:
            file_obj, retrieved_metadata = blob_helper_local.download_blob(
                bucket_name, blob_name, download_buffer, include_metadata=True
            )
            download_buffer.seek(0)
            downloaded_content = download_buffer.read()
            
        print(f"📄 Downloaded content: {downloaded_content.decode()}")
        print(f"📋 Retrieved metadata: {retrieved_metadata}")
        print(f"🔍 Return type: {type((file_obj, retrieved_metadata))}")
        
        # Test blob without metadata
        print(f"\n📦 Uploading blob without metadata...")
        blob_name_no_meta = "demo-file-no-meta.txt"
        with BytesIO(content) as upload_buffer:
            blob_helper_local.upload_blob(bucket_name, blob_name_no_meta, upload_buffer)
        
        with BytesIO() as download_buffer:
            file_obj, retrieved_metadata = blob_helper_local.download_blob(
                bucket_name, blob_name_no_meta, download_buffer, include_metadata=True
            )
            
        print(f"📋 Retrieved metadata for blob without metadata: {retrieved_metadata}")
        
        # Test deletion
        print(f"\n🗑️  Deleting blobs...")
        blob_helper_local.delete_blob(bucket_name, blob_name)
        blob_helper_local.delete_blob(bucket_name, blob_name_no_meta)
        print("✅ Deletion complete!")
        
        print(f"\n🎉 Demo completed successfully!")
        print("\nThe local blob helper now supports:")
        print("• Storing and retrieving metadata alongside blob data")
        print("• Optional metadata parameter in upload_blob()")
        print("• Optional include_metadata parameter in download_blob()")
        print("• Automatic metadata cleanup when deleting blobs")
        print("• Same API as the cloud storage version for seamless switching")


if __name__ == "__main__":
    demo_metadata_functionality()