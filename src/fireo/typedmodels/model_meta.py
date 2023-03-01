from fireo.models.model_meta import Meta, ModelMeta
from fireo.typedmodels.resolver import AnnotationResolver


class TypedMeta(Meta):
    """Meta class for TypedModel.

    This class adds support for the `annotation_resolver_cls` attribute
        that can be used to customize the annotation resolver.

    Example:
        >>> class CustomAnnotationResolver(AnnotationResolver):
        ...     resolvers = [*AnnotationResolver.resolvers, MyCustomTypeResolver]
        >>>
        >>> class MyModel(TypedModel):
        ...    class Meta:
        ...        annotation_resolver_cls = CustomAnnotationResolver
        ...    my_field: MyCustomType
    """
    supported_fields = [
        *Meta.supported_fields,
        'annotation_resolver_cls',
    ]
    inherited_fields = [
        *Meta.inherited_fields,
        'annotation_resolver_cls',
    ]

    annotation_resolver_cls = AnnotationResolver


class TypedModelMeta(ModelMeta):
    """Meta class for TypedModel.

    This class adds support for the automatic field generated from type annotations.
    """
    _meta_cls = TypedMeta

    def __new__(mcs, name, base, attrs):
        # Check if the model is not base TypedModel by its path and name:
        if not (name == 'TypedModel' and mcs.__module__ == 'fireo.models.models'):
            annotation_resolver = AnnotationResolver(attrs)
            attrs.update(annotation_resolver.resolve_fields())

        cls = super().__new__(mcs, name, base, attrs)
        return cls
