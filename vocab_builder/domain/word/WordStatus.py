import enum


class WordStatus(enum.Enum):

    # TODO change the description
    UNREVIEWED = "Unreviewed"
    KNOWN = "I Know It"
    STUDYING = "Added In Anki"
    IGNORED = "Ignored"
    STUDY_LATER = "Study Later"
