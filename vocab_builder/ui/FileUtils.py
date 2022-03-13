import os


def get_base_name_without_ext(file_path: str) -> str:
    """
    >>> get_base_name_without_ext("/Users/Joey/Downloads/test.txt")
    'test'
    """
    return os.path.splitext(os.path.basename(file_path))[0]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
