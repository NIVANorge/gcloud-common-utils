# Using gcloud-common-utils v0.5.0 with Metadata Support

## Version Information

**Current Version**: `0.5.0`
- ✨ **New Feature**: Blob metadata support in local helper
- 🔄 **API**: Backward compatible with existing code
- 📦 **Dependencies**: Updated to use Poetry for dependency management

## Installation Options

### Option 1: Install from Git Repository (Recommended for Development)

```bash
# Install directly from the git repository
pip install git+https://github.com/NIVANorge/gcloud-common-utils.git@get-blob-metadata

# Or with Poetry
poetry add git+https://github.com/NIVANorge/gcloud-common-utils.git@get-blob-metadata

# Or in requirements.txt
gcloud-common-utils @ git+https://github.com/NIVANorge/gcloud-common-utils.git@get-blob-metadata
```

### Option 2: Install from Local Development

```bash
# If you're developing locally and want to install from your local copy
pip install -e /path/to/gcloud-common-utils

# Or with Poetry
poetry add --editable /path/to/gcloud-common-utils
```

### Option 3: Build and Install Wheel

```bash
# Build the package
cd /path/to/gcloud-common-utils
poetry build

# Install the built wheel
pip install dist/gcloud_common_utils-0.5.0-py3-none-any.whl
```

## Usage Examples

### Basic Usage (Existing API - Still Works)

```python
from gcloud_common_utils import blob_helper_local
from io import BytesIO

# Upload blob (same as before)
with BytesIO(b"content") as buffer:
    blob_helper_local.upload_blob("bucket", "file.txt", buffer)

# Download blob (same as before)
with BytesIO() as buffer:
    blob_helper_local.download_blob("bucket", "file.txt", buffer)
```

### New Metadata Features (v0.5.0+)

```python
from gcloud_common_utils import blob_helper_local
from io import BytesIO

# Upload with metadata
metadata = {
    "content-type": "application/json",
    "author": "your-app",
    "created": "2025-10-01T12:00:00Z"
}

with BytesIO(b'{"data": "example"}') as buffer:
    blob_helper_local.upload_blob("bucket", "data.json", buffer, metadata=metadata)

# Download with metadata
with BytesIO() as buffer:
    file_obj, retrieved_metadata = blob_helper_local.download_blob(
        "bucket", "data.json", buffer, include_metadata=True
    )
    print(f"Metadata: {retrieved_metadata}")

# Download without metadata (default behavior)
with BytesIO() as buffer:
    file_obj = blob_helper_local.download_blob("bucket", "data.json", buffer)
```

## Version Compatibility

### For New Projects
```python
# pyproject.toml
[tool.poetry.dependencies]
gcloud-common-utils = {git = "https://github.com/NIVANorge/gcloud-common-utils.git", branch = "get-blob-metadata"}

# requirements.txt
gcloud-common-utils @ git+https://github.com/NIVANorge/gcloud-common-utils.git@get-blob-metadata
```

### For Existing Projects (Backward Compatible)
Your existing code will continue to work without any changes:

```python
# This still works exactly the same
blob_helper_local.upload_blob(bucket, filename, buffer)
result = blob_helper_local.download_blob(bucket, filename, buffer)
```

## Publishing Options

### Option A: Merge to Main and Tag

```bash
# After merging the get-blob-metadata branch to main
git checkout main
git tag v0.5.0
git push origin v0.5.0

# Then install with:
pip install git+https://github.com/NIVANorge/gcloud-common-utils.git@v0.5.0
```

### Option B: Publish to PyPI (If Desired)

```bash
# Build the package
poetry build

# Publish to PyPI (requires PyPI credentials)
poetry publish

# Then install with:
pip install gcloud-common-utils==0.5.0
```

### Option C: Publish to Private Package Repository

```bash
# Configure your private repository
poetry config repositories.private-repo https://your-private-repo.com

# Publish
poetry publish -r private-repo

# Install from private repo
pip install --index-url https://your-private-repo.com gcloud-common-utils==0.5.0
```

## Development Workflow

### For Contributors

```bash
# Clone and setup
git clone https://github.com/NIVANorge/gcloud-common-utils.git
cd gcloud-common-utils
git checkout get-blob-metadata
poetry install

# Run tests
poetry run pytest

# Make changes and test
poetry run python test_metadata_demo.py
```

### For Package Users

```bash
# In your project directory
poetry add git+https://github.com/NIVANorge/gcloud-common-utils.git@get-blob-metadata

# Or pin to specific version after tagging
poetry add git+https://github.com/NIVANorge/gcloud-common-utils.git@v0.5.0
```

## Migration Guide

### From v0.4.1 to v0.5.0

✅ **No breaking changes** - all existing code continues to work

### Optional: Adopt New Features

```python
# Before (still works)
blob_helper_local.download_blob(bucket, blob, buffer)

# After (new option)
file_obj, metadata = blob_helper_local.download_blob(bucket, blob, buffer, include_metadata=True)
```

## Troubleshooting

### Import Issues
```python
# Make sure you're importing from the right module
from gcloud_common_utils import blob_helper_local

# Check version
import gcloud_common_utils
print(gcloud_common_utils.__version__)  # Should be 0.5.0
```

### Dependency Conflicts
```bash
# Update dependencies
poetry update
# or
pip install --upgrade gcloud-common-utils
```

### Environment Issues
```bash
# Make sure LOCAL_STORAGE_PATH is set for local development
export LOCAL_STORAGE_PATH="/tmp/local-storage"
```