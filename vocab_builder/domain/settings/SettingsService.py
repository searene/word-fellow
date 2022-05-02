from vocab_builder.infrastructure import VocabBuilderDB


class SettingsService:

    def __init__(self, db: VocabBuilderDB):
        self.__db = db
