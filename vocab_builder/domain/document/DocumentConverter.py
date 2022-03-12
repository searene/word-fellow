from typing import List, Tuple

from vocab_builder.domain.document.Document import Document


def convert_sql_res_to_document_object(sql_res: List[Tuple]) -> List[Document]:
    res = []
    for document_tuple in sql_res:
        document_id = document_tuple[0]
        name = document_tuple[1]
        contents = document_tuple[2]
        res.append(Document(document_id, name, contents))
    return res
