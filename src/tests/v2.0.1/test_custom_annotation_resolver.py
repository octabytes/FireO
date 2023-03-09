from functools import partial

from fireo.fields import Field, TextField
from fireo.typedmodels import TypedModel
from fireo.typedmodels.resolver import AnnotationResolver, SimpleFieldResolver


class CustomField(Field):
    pass


class CustomType:
    pass


class CustomResolver(AnnotationResolver):
    resolvers = [
        *AnnotationResolver.resolvers,
        partial(SimpleFieldResolver, supported_field_type=CustomType, field_class=CustomField, field_kwargs=dict()),
    ]


class MyModel(TypedModel):
    class Meta:
        annotation_resolver_cls = CustomResolver

    my_custom_field: CustomType


def test_custom_resolver():
    fields = MyModel._meta.field_list

    assert fields['my_custom_field'].__class__ is CustomField
