import enum


class WordStatus(enum.Enum):
    UNKNOWN = "UNKNOWN"
    KNOWN = "KNOWN"
    STUDYING = "STUDYING"
    SKIPPED = "SKIPPED"