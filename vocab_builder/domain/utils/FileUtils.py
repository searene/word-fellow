import os
import shutil


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
