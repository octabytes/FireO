from fireo.models.model_meta import Meta, ModelMeta
from fireo.typedmodels.resolver import AnnotationResolver
from fireo.typedmodels.utils import resolve_meta_attr


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

    def __new__(mcs, name, bases, attrs):
        # Check if the model is not base TypedModel by its path and name:
        if not (attrs['__qualname__'] == 'TypedModel' and attrs['__module__'] == 'fireo.typedmodels.model'):
            annotation_resolver_cls = resolve_meta_attr('annotation_resolver_cls', bases, attrs)
            annotation_resolver = annotation_resolver_cls(attrs)
            attrs.update(annotation_resolver.resolve_fields())

        cls = super().__new__(mcs, name, bases, attrs)
        return cls
