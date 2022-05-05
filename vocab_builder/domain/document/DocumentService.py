from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentConverter import convert_sql_res_to_document_object
from vocab_builder.domain.document.analyzer import IDocumentAnalyzer
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


class DocumentService:

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

    def get_document_id_and_name_list(self) -> [(int, str)]:
        return self.db.fetch_all("""
            select id, name
            from documents
        """)

    def get_document_name(self, doc_id: int) -> str:
        return self.db.fetch_one("""
            select name
            from documents
            where id = ?
        """, (doc_id,))[0]

    def get_document_list(self) -> [Document]:
        query_res = self.db.fetch_all("""
            select id, name, contents
            from documents
        """)
        return convert_sql_res_to_document_object(query_res)

    def get_doc_by_id(self, doc_id: int) -> Document:
        query_res = self.db.fetch_all("""
            select id, name, contents
            from documents
            where id = ?
        """, (doc_id,))
        return convert_sql_res_to_document_object(query_res)[0]

    def remove_all_documents_and_words(self) -> None:
        self.db.execute("delete from documents")
        self.db.execute("delete from words")
        self.db.execute("delete from global_word_status")

    def delete_doc_and_words(self, doc_id: int) -> None:
        """Delete document and all words in it."""
        self.db.execute("delete from documents where id = ?", (doc_id,))
        self.db.execute("delete from words where document_id = ?", (doc_id,))

    def init_database(self):
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            name TEXT,
            contents TEXT
        )
        """)
