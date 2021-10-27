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
