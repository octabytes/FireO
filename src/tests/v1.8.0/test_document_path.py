from fireo.fields import TextField
from fireo.models import Model


def test_model_document_path():
    class Doc(Model):
        doc_id = TextField()

    class SubDoc(Model):
        doc_id = TextField()

    doc = Doc(doc_id="parent")
    doc.save()

    sub_doc = SubDoc(doc_id="child")
    sub_doc.parent = doc.key
    sub_doc.save()

    assert doc.document_path == '/'.join([
        doc.collection_name,
        doc.id,
    ])
    assert sub_doc.document_path == '/'.join([
        doc.collection_name,
        doc.id,
        sub_doc.collection_name,
        sub_doc.id
    ])
