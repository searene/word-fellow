import enum


class WordStatus(enum.Enum):

    # TODO rename it to unreviewed?
    # TODO change the description
    UNKNOWN = "UNKNOWN"
    KNOWN = "KNOWN"
    STUDYING = "STUDYING"
    IGNORED = "IGNORED"
    STUDY_LATER = "STUDY_LATER"
