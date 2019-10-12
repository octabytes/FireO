
class ModelFromResult:
    @classmethod
    def convert(cls, model, doc):
        if doc.to_dict() is None:
            return None

        for k, v in doc.to_dict().items():
            field = model._meta.get_field_by_column_name(k)
            if field is None:
                continue
            val = field.field_value(v)
            setattr(model, field.name, val)
        setattr(model, '_id', doc.id)
        return model