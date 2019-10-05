
class ModelFromDict:
    @classmethod
    def convert(cls, model, doc):
        for k, v in doc.to_dict().items():
            field = model._meta.get_field_by_column_name(k)
            val = field.field_value(v)
            setattr(model, field.name, val)
        setattr(model, '_id', doc.id)
        return doc.id