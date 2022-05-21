import os
import shutil
import tempfile
import uuid
from typing import Optional


def remove_dir_if_exists(directory: str) -> None:
    if os.path.exists(directory):
        shutil.rmtree(directory)


def mkdirs(directory: str) -> None:
    """Create the directory and all the intermediate directories if they don't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def remove_all_files_in_dir(directory: str) -> None:
    shutil.rmtree(directory)
    os.makedirs(directory)


def create_temp_dir(suffix: Optional[str] = None) -> str:
    temp_dir = tempfile.mkdtemp(suffix)
    remove_dir_if_exists(temp_dir)
    mkdirs(temp_dir)
    return temp_dir


def generate_non_existent_temp_file_path() -> str:
    return os.path.join(tempfile.mkdtemp(), str(uuid.uuid4()))
