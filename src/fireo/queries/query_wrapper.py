from fireo.fields import ReferenceField, NestedModel, IDField
from fireo.queries import errors
from fireo.utils import utils
from google.cloud import firestore


class ModelWrapper:
    """Convert query result into Model instance"""
    @classmethod
    def from_query_result(cls, model, doc, nested_doc=False):
        parent_key = None
        if nested_doc:
            doc_dict = doc
        elif doc:
            parent_key = utils.get_parent_doc(doc.reference.path)
            if doc.to_dict():
                doc_dict = doc.to_dict()
            else:
                return None
        else:
            return None

        # instance values is changed according to firestore
        # so mark it modified this will help later for figuring
        # out the updated fields when need to update this document
        setattr(model, '_instance_modified', True)

        for k, v in doc_dict.items():
            field = model._meta.get_field_by_column_name(k)
            # if missing field setting is set to "ignore" then
            # get_field_by_column_name return None So, just skip this field
            if field is None:
                continue
            # Check if it is Reference field
            if isinstance(field, ReferenceField):
                val = ReferenceFieldWrapper.from_doc_ref(model, field, field.field_value(v))
            elif isinstance(field, NestedModel):
                nested_doc_val = field.field_value(v)
                if nested_doc_val:
                    val = NestedModelWrapper.from_model_dict(field, nested_doc_val)
                else:
                    val = None
            else:
                val = field.field_value(v)
            # setattr(model, field.name, val)
            model._set_orig_attr(field.name, val)

        # If parent key is None but here is parent key from doc then set the parent for this model
        # This is case when you filter the documents parent key not auto set just set it
        if not model.parent and parent_key is not None:
            model.parent = parent_key

        # If it is not nested model then set the id for this model
        if not nested_doc:
            # When getting document attach the IDField if there is no user specify 
            # it will prevent to generate new id everytime when document save
            # For more information see issue #45 https://github.com/octabytes/FireO/issues/45
            if model._meta.id is None:
                model._meta.id = ('id', IDField())
                
            # setattr(model, '_id', doc.id)
            model._set_orig_attr('_id', doc.id)

            # save the firestore reference doc so that further actions can be performed (i.e. collections())
            model._meta.set_reference_doc(doc.reference)
            # even though doc.reference currently points to self, there is no guarantee this will be true
            # in the future, therefore we should store the create time and update time separate.
            model._create_time = doc.create_time
            model._update_time = doc.update_time
        return model


class NestedModelWrapper:
    """Get nested document"""
    @classmethod
    def from_model_dict(cls, field, doc):
        model = field.nested_model()
        return ModelWrapper.from_query_result(model, doc, nested_doc=True)


class ReferenceFieldWrapper:
    """Get reference documents

    If auto_load is True then load the document otherwise return `ReferenceDocLoader` object and later user can use
    `get()` method to retrieve the document
    """
    @classmethod
    def from_doc_ref(cls, parent_model, field, ref):
        if not ref:
            return None

        ref_doc = ReferenceDocLoader(parent_model, field, ref)

        if field.auto_load:
            return ref_doc.get()
        return ref_doc


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
