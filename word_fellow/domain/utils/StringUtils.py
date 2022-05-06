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


def split_with_positions(delimiters: [str], text: str) -> [(str, int)]:
    """Split text according to delimiters, returns each word and its start position after splitting.
    Empty strings are excluded

    Parameters:
        delimiters: A list of strings, the length of each one shuold only be one
        text: The text to split

    Returns:
        A list of tuples, each tuple contains:
            1. A word
            2. The starting position of the word

    >>> split_with_positions(["a", "b", "c"], "XXXaYYYbZZZcDDD")
    [('XXX', 0), ('YYY', 4), ('ZZZ', 8), ('DDD', 12)]
    >>> split_with_positions(["a", "b", "c"], "XXXaYYYbc")
    [('XXX', 0), ('YYY', 4)]
    """

    delimiter_set = set(delimiters)
    previous_word = ""
    res = []
    for i in range(len(text)):
        c = text[i]
        if c in delimiter_set:

            # Skip empty words
            if previous_word == "":
                continue

            start_pos_of_previous_word = i - len(previous_word)
            res.append((previous_word, start_pos_of_previous_word))
            previous_word = ""
        else:
            previous_word += c

    if previous_word != "":
        res.append((previous_word, len(text) - len(previous_word)))
    return res


if __name__ == "__main__":
    import doctest
    doctest.testmod()
