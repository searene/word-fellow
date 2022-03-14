from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentConverter import convert_sql_res_to_document_object
from vocab_builder.domain.document.analyzer import IDocumentAnalyzer
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


class DocumentFactory:

    def __init__(self, db: VocabBuilderDB):
        self.db = db

    def create_new_document(self, name: str, contents: str) -> Document:
        document_id = self.db.insert("""
            insert into documents (name, contents) values (?, ?)
        """, (name, contents))
        document = Document(document_id, name=name, contents=contents)
        return document

    def import_document(self, name, contents, document_analyzer: IDocumentAnalyzer) -> Document:
        doc = self.create_new_document(name, contents)
        document_analyzer.import_words(doc)
        return doc

    def get_document_list(self) -> [Document]:
        query_res = self.db.all("""
            select id, name, contents
            from documents
        """)
        return convert_sql_res_to_document_object(query_res)