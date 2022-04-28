from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.analyzer import IDocumentAnalyzer
from vocab_builder.domain.utils.StringUtils import split_with_positions
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordService import batch_insert
from vocab_builder.domain.word.WordValueObject import WordValueObject
from vocab_builder.infrastructure import VocabBuilderDB


class DefaultDocumentAnalyzer(IDocumentAnalyzer):
    def __init__(self, db: VocabBuilderDB):
        self.db = db

    def import_words(self, document: Document) -> [Word]:
        word_value_objects = self.__split_document_contents_into_words(document)
        batch_insert(word_value_objects, self.db)
        return document.get_words(self.db)

    @staticmethod
    def __split_document_contents_into_words(doc: Document) -> [WordValueObject]:
        delimiters = (",", " ", "\t", "\"", "'", "`", ".", "!", "(", ")", "@", "#", "?", "\n")
        word_with_start_pos_list = split_with_positions(delimiters, doc.contents)
        word_to_value_object_dict = {}
        for word_with_start_pos in word_with_start_pos_list:
            word = word_with_start_pos[0]
            start_pos = word_with_start_pos[1]
            if word in word_to_value_object_dict:
                word_to_value_object_dict[word].word_to_start_pos_dict[word].append(start_pos)
            else:
                word_to_start_pos_dict = {word: [start_pos]}
                word_to_value_object_dict[word] = WordValueObject(word, doc.document_id, word_to_start_pos_dict)
        return [word_value_object for word_value_object in word_to_value_object_dict.values()]