import re
from typing import Tuple


def split(delimiters: Tuple[str, ...], text: str) -> [str]:
    """Split text according to delimiters.

    >>> split(("a", "b", "c"), "XXXaYYYbZZZcDDD")
    ['XXX', 'YYY', 'ZZZ', 'DDD']

    >>> split(("a", "b", "c"), "XXXaYYYbZZZc")
    ['XXX', 'YYY', 'ZZZ', '']
    """
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, text)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
