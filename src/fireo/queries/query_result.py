
class ModelFromResult:
    @classmethod
    def convert(cls, model, doc):
        if doc.to_dict() is None:
            return None

        for k, v in doc.to_dict().items():
            field = model._meta.get_field_by_column_name(k)
            # if missing field setting is set to "ignore" then
            # get_field_by_column_name return None So, just skip this field
            if field is None:
                continue
            # get field value
            val = field.field_value(v)
            setattr(model, field.name, val)
        setattr(model, '_id', doc.id)
        return model