import os


class ResetService:

    def __init__(self, db_path: str):
        self.__db_path = db_path

    def reset(self) -> None:
        os.remove(self.__db_path)
