class Range:
    """
    A class to represent a range, including a start position and an end position.
    """
    def __init__(self, start: int, end: int):
        """
        Parameters
        ----------
            start: The start position (Inclusive, counting from 0 instead of 1).
            end: The end position (Exclusive)
        """
        self.start = start
        self.end = end
