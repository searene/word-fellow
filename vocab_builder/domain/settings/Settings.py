from vocab_builder.infrastructure import VocabBuilderDB


class Settings:

    def __init__(self, enable_backup: bool, backup_count: int, backup_folder_path: str):
        self.__enable_backup = enable_backup
        self.__backup_count = backup_count
        self.__backup_folder_path = backup_folder_path

    @staticmethod
    def init_database(db: VocabBuilderDB) -> None:
        db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            contents TEXT NOT NULL
        )
        """)
