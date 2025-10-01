# Blob Helper Local - Metadata Support Implementation

## Overview

The `blob_helper_local.py` module has been enhanced to support blob metadata, mimicking the behavior of Google Cloud Storage's blob metadata functionality for local development and testing.

## Changes Made

### 1. Enhanced Function Signatures

#### `upload_blob`
```python
@typechecked
def upload_blob(bucket_name: str, destination_blob_name: str, file_like_object, metadata: Optional[Dict[str, Any]] = None):
```
- Added optional `metadata` parameter
- Metadata is stored as JSON file alongside the blob data

#### `download_blob`
```python
@typechecked
def download_blob(bucket_name: str, source_blob_name: str, file_like_object: IOBase, include_metadata: bool = False) -> Union[IOBase, Tuple[IOBase, Optional[Dict[str, Any]]]]:
```
- Added `include_metadata` parameter (default: False)
- Returns tuple `(file_like_object, metadata)` when `include_metadata=True`
- Returns just `file_like_object` when `include_metadata=False`
- Matches the signature and behavior of the cloud version

### 2. New Helper Functions

#### `_get_metadata_path(bucket_name, file_path) -> str`
- Returns the path for the metadata JSON file corresponding to a blob
- Metadata files have `.metadata.json` extension

#### `_save_metadata(bucket_name: str, file_path: str, metadata: Optional[Dict[str, Any]])`
- Saves metadata to a JSON file alongside the blob
- Creates necessary directories if they don't exist

#### `_load_metadata(bucket_name: str, file_path: str) -> Optional[Dict[str, Any]]`
- Loads metadata from JSON file
- Returns `None` if metadata file doesn't exist or can't be loaded
- Handles JSON decode errors gracefully

### 3. Enhanced Delete Functionality

#### `delete_blob`
- Now also removes associated metadata files when deleting blobs
- Ensures cleanup of both data and metadata

## Usage Examples

### Upload with Metadata
```python
metadata = {
    "content-type": "text/plain",
    "author": "user@example.com",
    "custom-field": "value"
}

with BytesIO(content) as buffer:
    upload_blob("my-bucket", "my-file.txt", buffer, metadata=metadata)
```

### Download with Metadata
```python
with BytesIO() as buffer:
    file_obj, metadata = download_blob("my-bucket", "my-file.txt", buffer, include_metadata=True)
    # metadata will be a dict or None
```

### Download without Metadata
```python
with BytesIO() as buffer:
    file_obj = download_blob("my-bucket", "my-file.txt", buffer, include_metadata=False)
    # Returns just the file object
```

## Metadata Storage Format

Metadata is stored as JSON files with the naming convention:
```
{blob_path}.metadata.json
```

Example:
- Blob: `/path/to/bucket/folder/file.txt`
- Metadata: `/path/to/bucket/folder/file.txt.metadata.json`

## Testing

Comprehensive tests have been added:
- `test_local_blob_helper_metadata`: Tests upload/download with metadata
- `test_local_blob_helper_no_metadata`: Tests behavior when no metadata exists
- `test_delete_blob_with_metadata`: Tests metadata cleanup on deletion

## Compatibility

- **Backward Compatible**: Existing code continues to work without changes
- **Cloud Parity**: Same API as Google Cloud Storage blob operations
- **Type Safe**: Full type annotations with typeguard decorators
- **Error Handling**: Graceful handling of missing or corrupted metadata files

## Environment Setup

The project now uses Poetry for dependency management:

```bash
# Install dependencies
poetry install

# Run tests
poetry run python -m pytest tests/ -v

# Run demo
poetry run python test_metadata_demo.py
```

## Dependencies

- `google-cloud-storage`: For cloud parity
- `typeguard`: Type checking at runtime
- `pytest`: Testing framework
- Standard library: `json`, `os`, `shutil`, etc.