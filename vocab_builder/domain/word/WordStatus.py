import enum


class WordStatus(enum.Enum):

    # TODO change the description
    UNREVIEWED = "Unreviewed"
    KNOWN = "KNOWN"
    STUDYING = "STUDYING"
    IGNORED = "IGNORED"
    STUDY_LATER = "STUDY_LATER"
