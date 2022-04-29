import enum


class WordStatus(enum.Enum):
    # TODO Maybe we need to new status called unchecked
    UNKNOWN = "UNKNOWN"
    KNOWN = "KNOWN"
    STUDYING = "STUDYING"
    IGNORED = "IGNORED"
