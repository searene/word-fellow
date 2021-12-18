class WordContext:
    def __init__(self, contents: str, mark_start_pos: int, mark_end_pos: int):
        self.contents = contents
        self.mark_start_pos = mark_start_pos
        self.mark_end_pos = mark_end_pos

    def __eq__(self, other):
        if not isinstance(other, WordContext):
            return False
        return self.contents == other.contents \
               and self.mark_start_pos == other.mark_start_pos \
               and self.mark_end_pos == other.mark_end_pos
