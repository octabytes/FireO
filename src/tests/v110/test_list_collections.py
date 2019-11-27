import fireo
from fireo.fields import IDField
from fireo.models import Model


class Doc(Model):
    doc_id = IDField(db_name='id')

def _create_collections(count: int):
    collections = []
    for c in range(count):
        collection = f"collection_{c}"
        collections.append(collection)
        doc = Doc(doc_id=f"{c}_1", collection_name=collection)
        doc.save()
    
    return collections


def test_list_collections():
    created_collections = _create_collections(10)
    collections = fireo.list_collections()
    assert collections == created_collections
