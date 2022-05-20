from ...domain.word.WordStatus import WordStatus


class Operation:
    def __init__(self, word: str, prev_status: WordStatus, next_status: WordStatus):
        self.word = word
        self.prev_status = prev_status
        self.next_status = next_status
