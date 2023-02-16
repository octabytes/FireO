from fireo.fields import  IDField
from fireo.queries import errors
from fireo.utils import utils


class ModelWrapper:
    """Convert query result into Model instance"""
    @classmethod
    def from_query_result(cls, model, doc):
        if not doc:
            return None

        parent_key = utils.get_parent_doc(doc.reference.path)
        doc_dict = doc.to_dict()
        if not doc_dict:
            return None

        model.populate_from_doc_dict(doc_dict, stored=True, by_column_name=True)

        # If parent key is None but here is parent key from doc then set the parent for this model
        # This is case when you filter the documents parent key not auto set just set it
        if not model.parent and parent_key is not None:
            model.parent = parent_key

        # setattr(model, '_id', doc.id)
        model._set_orig_attr('_id', doc.id)

        # even though doc.reference currently points to self, there is no guarantee this will be true
        # in the future, therefore we should store the create time and update time separate.
        model._create_time = doc.create_time
        model._update_time = doc.update_time

        return model


class ReferenceDocLoader:
    """Get reference doc and Convert into model instance"""
    def __init__(self, parent_model, field, ref):
        self.parent_model = parent_model
        self.field = field
        self.ref = ref

    def get(self):
        doc = self.ref.get()
        if not doc.exists:
            raise errors.ReferenceDocNotExist(f'{self.field.model_ref.collection_name}/{self.ref.id} not exist')
        model = ModelWrapper.from_query_result(self.field.model_ref(), doc)

        # if on_load method is defined then call it
        if self.field.on_load:
            method_name = self.field.on_load
            getattr(self.parent_model, method_name)(model)
        return model
