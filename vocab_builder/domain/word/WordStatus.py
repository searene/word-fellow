import enum


class WordStatus(enum.Enum):

    UNREVIEWED = "Unreviewed"
    KNOWN = "I Know It"
    STUDYING = "Added In Anki"
    IGNORED = "Ignored"
    STUDY_LATER = "Study Later"
