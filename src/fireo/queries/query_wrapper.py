from fireo.fields.fields import ReferenceField
from fireo.queries import errors


class ModelWrapper:
    @classmethod
    def from_query_result(cls, model, doc):
        if doc.to_dict() is None:
            return None

        for k, v in doc.to_dict().items():
            field = model._meta.get_field_by_column_name(k)
            # if missing field setting is set to "ignore" then
            # get_field_by_column_name return None So, just skip this field
            if field is None:
                continue
            # Check if it is Reference field
            if isinstance(field, ReferenceField):
                val = ReferenceFieldWrapper.from_doc_ref(field, v)
            else:
                # get field value
                val = field.field_value(v)
            setattr(model, field.name, val)
        setattr(model, '_id', doc.id)
        return model


class ReferenceFieldWrapper:
    @classmethod
    def from_doc_ref(cls, field, ref):
        if not ref:
            return None

        doc = ref.get()
        if not doc.exists:
            raise errors.ReferenceDocNotExist(f'{field.model_ref.collection_name}/{ref.id} not exist')
        return ModelWrapper.from_query_result(field.model_ref(), doc)
