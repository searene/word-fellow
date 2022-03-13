class WordValueObject:

    def __init__(self, text: str, document_id: int, word_to_start_pos_dict: dict[str, [int]], skipped: bool):
        """
        Args:
            text: The word text, e.g. "beautiful", "python", etc.
            document_id: The document to which the word belongs.
            word_to_start_pos_dict: word -> start pos of the word
            skipped: Whether the reader decides to skip the word for the current document.
        """
        self.text = text
        self.document_id = document_id
        self.word_to_start_pos_dict = word_to_start_pos_dict
        self.skipped = skipped
