import fireo
from fireo.fields import TextField
from fireo.models import Model
from pprint import pprint

def _create_collections(count: int):
    collections = []

    for c in range(count):
        collection = f"collection_{c}"

        class Doc(Model):
            doc_id = TextField()
            class Meta:
                collection_name = collection

        collections.append(collection)
        doc = Doc(doc_id=f"{c}_1")
        doc.save()
    
    return collections


def test_list_collections():
    collections_before = fireo.list_collections()
    created_collections = _create_collections(10)
    collections_after = fireo.list_collections()

    assert set(created_collections).isdisjoint(collections_before)
    assert set(created_collections).issubset(collections_after)


def test_list_subcollections():
    class Doc(Model):
        doc_id = TextField()
        class Meta:
            collection_name = "subcollection_test"

    doc = Doc(doc_id="parent")
    doc.save()

    class SubDoc(Model):
        doc_id = TextField()
        class Meta:
            collection_name = "child"

    sub_doc = SubDoc(doc_id="child")
    sub_doc.parent = doc.key
    sub_doc.save()

    subcollections =  doc.list_subcollections()


    assert subcollections != ""
    assert subcollections == ["child"]

