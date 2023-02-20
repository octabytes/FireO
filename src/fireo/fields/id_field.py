from google.cloud.firestore_v1.base_collection import _auto_id

from fireo.fields.base_field import Field


class IDField(Field):
    """Specify custom id for models

    User can specify model id and will save with the same id in firestore otherwise it will
    return None and generate later from firestore and attached to model

    Example
    --------
    .. code-block:: python
        class User(Mode):
            user_id = IDField()

        u = User()
        u.user_id = "custom_doc_id"
        u.save()

        # After save id will be saved in `user_id`
        print(self.user_id)  # custom_doc_id

    Attributes
    ----------
        include_in_document: bool = False (default) If true then id will be included in FireStore document
    """

    def __init__(self, *args, include_in_document=False, default_factory=_auto_id, **kwargs):
        super().__init__(*args, **kwargs, default_factory=default_factory)
        self.include_in_document = include_in_document

    def contribute_to_model(self, model_cls, name):
        self.name = name
        setattr(model_cls, name, None)
        model_cls._meta.add_model_id(self)
