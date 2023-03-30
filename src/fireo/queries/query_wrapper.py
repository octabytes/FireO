from fireo.fields import  IDField
from fireo.queries import errors
from fireo.utils import utils


class ModelWrapper:
    """Convert query result into Model instance"""
    @classmethod
    def from_query_result(cls, mutable_instance, doc):
        mutable_instance.populate_from_doc(doc)

        if not doc or not doc.to_dict():
            return None

        return mutable_instance


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
