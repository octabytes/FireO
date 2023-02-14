from fireo.fields import TextField
from fireo.managers.managers import Manager
from fireo.models import Model


def test_inherit_meta_fields():
    class CustomManager(Manager):
        pass

    class AbstractModel(Model):
        name = TextField()

        class Meta:
            collection_name = 'first'
            abstract = True
            to_lowercase = True
            missing_field = 'raise_error'
            ignore_none_field = False
            default_manager_cls = CustomManager

    class ActualModel(AbstractModel):
        pass

    assert ActualModel._meta.collection_name != 'first', 'Collection name should not be inherited'
    assert ActualModel._meta.abstract is False, 'Abstract should not be inherited'
    assert ActualModel._meta.to_lowercase is True
    assert ActualModel._meta.missing_field == 'raise_error'
    assert ActualModel._meta.ignore_none_field is False
    assert ActualModel._meta.default_manager_cls == CustomManager
    assert ActualModel.collection.__class__ == CustomManager
