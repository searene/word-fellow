import json
import os
from typing import Dict, Any

from vocab_builder.domain.settings.Settings import Settings
from vocab_builder.infrastructure import VocabBuilderDB


class SettingsService:

    def __init__(self, db: VocabBuilderDB):
        self.__db = db

    def update_settings(self, settings: Settings) -> None:
        self.__delete_settings_in_db()
        self.__insert_settings_in_db(settings.to_dict())

    def get_settings(self) -> Settings:
        settings_dict = self.__get_settings_dict_in_db()
        return self.__convert_dict_to_settings(settings_dict)

    def init_database(self) -> None:
        self.__db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            contents TEXT NOT NULL
        )
        """)
        settings_in_db = self.__get_settings_dict_in_db()
        if settings_in_db == {}:
            self.update_settings(self._get_default_settings())

    def __get_default_backup_folder(self) -> str:
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, ".anki-vocab-builder-backup")

    def _get_default_settings(self) -> Settings:
        return Settings(
            enable_backup=True,
            backup_count=5,
            backup_folder_path=self.__get_default_backup_folder()
        )

    def __convert_dict_to_settings(self, settings_dict: Dict[str, Any]) -> Settings:
        return Settings(
            settings_dict["enable_backup"],
            settings_dict["backup_count"],
            settings_dict["backup_folder_path"],
        )

    def __insert_settings_in_db(self, settings_dict: Dict[str, Any]) -> None:
        self.__db.execute("""insert into settings (contents) values (?)""", (json.dumps(settings_dict),))

    def __get_settings_dict_in_db(self) -> Dict[str, Any]:
        query_res = self.__db.fetch_one("""select contents from settings limit 1""")
        if query_res is None:
            return {}
        return json.loads(query_res[0])

    def __delete_settings_in_db(self) -> None:
        self.__db.execute("""delete from settings""")