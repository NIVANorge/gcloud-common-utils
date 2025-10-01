# Example: Using gcloud-common-utils v0.5.0 in Another Project

## Project Structure
```
my-other-project/
├── pyproject.toml  (or requirements.txt)
├── main.py
└── ...
```

## Installation

### Option 1: Using Poetry (Recommended)
```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.9"
gcloud-common-utils = {git = "https://github.com/NIVANorge/gcloud-common-utils.git", branch = "get-blob-metadata"}
```

### Option 2: Using pip/requirements.txt
```txt
# requirements.txt
gcloud-common-utils @ git+https://github.com/NIVANorge/gcloud-common-utils.git@get-blob-metadata
```

### Option 3: Local Development
```bash
# Install from local wheel
pip install /path/to/gcloud-common-utils/dist/gcloud_common_utils-0.5.0-py3-none-any.whl
```

## Usage Example

```python
# main.py
import os
import tempfile
from io import BytesIO
from gcloud_common_utils import blob_helper_local

def main():
    # Set up local storage path
    os.environ["LOCAL_STORAGE_PATH"] = tempfile.gettempdir()
    
    # Example data
    bucket_name = "my-app-bucket"
    blob_name = "user-data.json"
    content = b'{"user_id": 123, "name": "John Doe"}'
    
    # Metadata for the blob
    metadata = {
        "content-type": "application/json",
        "app-version": "1.0.0",
        "uploaded-by": "user-service",
        "timestamp": "2025-10-01T12:00:00Z"
    }
    
    print("🚀 Using gcloud-common-utils v0.5.0 with metadata support")
    
    # Upload with metadata (NEW in v0.5.0)
    print("📤 Uploading blob with metadata...")
    with BytesIO(content) as upload_buffer:
        blob_helper_local.upload_blob(bucket_name, blob_name, upload_buffer, metadata=metadata)
    
    # Download with metadata (NEW in v0.5.0)
    print("📥 Downloading blob with metadata...")
    with BytesIO() as download_buffer:
        file_obj, retrieved_metadata = blob_helper_local.download_blob(
            bucket_name, blob_name, download_buffer, include_metadata=True
        )
        download_buffer.seek(0)
        downloaded_content = download_buffer.read()
        
    print(f"✅ Content: {downloaded_content.decode()}")
    print(f"📋 Metadata: {retrieved_metadata}")
    
    # Traditional usage (still works - backward compatible)
    print("📥 Downloading blob without metadata (traditional way)...")
    with BytesIO() as download_buffer:
        file_obj = blob_helper_local.download_blob(bucket_name, blob_name, download_buffer)
        download_buffer.seek(0)
        downloaded_content = download_buffer.read()
        
    print(f"✅ Content: {downloaded_content.decode()}")
    print("🎉 All operations completed successfully!")

if __name__ == "__main__":
    main()
```

## Installation Commands

```bash
# Using Poetry
poetry add git+https://github.com/NIVANorge/gcloud-common-utils.git@get-blob-metadata
poetry install

# Using pip
pip install git+https://github.com/NIVANorge/gcloud-common-utils.git@get-blob-metadata

# Run the example
python main.py
```

## Version Checking

```python
# Check which version you have installed
import gcloud_common_utils
print(f"gcloud-common-utils version: {gcloud_common_utils.__version__}")

# Should output: gcloud-common-utils version: 0.5.0
```