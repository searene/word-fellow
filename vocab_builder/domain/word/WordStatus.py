import enum


class WordStatus(enum.Enum):

    # TODO rename it to unreviewed?
    UNKNOWN = "UNKNOWN"
    KNOWN = "KNOWN"
    STUDYING = "STUDYING"
    IGNORED = "IGNORED"

    # TODO Support it
    STUDY_LATER = "STUDY_LATER"
