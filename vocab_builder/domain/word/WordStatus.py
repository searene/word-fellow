import enum


class WordStatus(enum.Enum):

    UNREVIEWED = "Unreviewed"
    KNOWN = "I Know It"
    STUDYING = "Added To Anki"
    IGNORED = "Ignored"
    STUDY_LATER = "Study Later"
