from tests.base.BaseTestCase import BaseTestCase
from word_fellow.domain.settings.Settings import Settings
from word_fellow.domain.settings.SettingsService import SettingsService


class SettingsServiceTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.__settings_service = SettingsService(self.db)

    def tearDown(self) -> None:
        super().tearDown()

    def test_should_update_settings_when_there_is_no_record_before(self):
        settings = Settings(True, 20, "/test/path")
        self.__settings_service.update_settings(settings)

        obtained_settings = self.__settings_service.get_settings()
        self.assertEqual(settings, obtained_settings)

    def test_should_update_settings_when_there_is_old_record_before(self):
        self.__settings_service.update_settings(Settings(True, 20, "/test/path"))

        new_settings = Settings(False, 0, "")
        self.__settings_service.update_settings(Settings(False, 0, ""))

        obtained_settings = self.__settings_service.get_settings()
        self.assertEqual(new_settings, obtained_settings)

    def test_should_insert_default_data_when_init_database(self):
        settings = self.__settings_service.get_settings()
        self.assertEqual(settings, self.__settings_service._get_default_settings())
