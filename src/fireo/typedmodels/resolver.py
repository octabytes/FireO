"""Provide method and classes to convert type annotation into FirO Fields."""
import sys
from datetime import datetime
from enum import Enum
from functools import partial
from typing import Iterator, Tuple, Union

from google.cloud import firestore

from fireo.fields import (
    BooleanField,
    DateTime,
    Field,
    GeoPoint,
    ListField,
    MapField,
    NestedModelField,
    NumberField,
    TextField,
)
from fireo.fields.enum_field import EnumField
from fireo.models import Model

if sys.version_info >= (3, 10):
    from types import NoneType, UnionType
else:
    NoneType = type(None)
    UnionType = type('FakeUnionType', (type,), {})

if sys.version_info >= (3, 8):
    from typing import get_args, get_origin
else:
    from typing_extensions import get_args, get_origin


class FieldResolver:
    def __init__(self, resolver: 'AnnotationResolver', field_type: type, extra_kwargs: dict):
        self.resolver = resolver
        self.extra_kwargs = extra_kwargs
        self.field_type = field_type

    def can_use(self) -> bool:
        raise NotImplementedError

    def resolve(self) -> Field:
        raise NotImplementedError


class SimpleFieldResolver(FieldResolver):
    def __init__(
        self,
        resolver: 'AnnotationResolver',
        field_type,
        extra_kwargs,
        supported_field_type,
        field_class,
        field_kwargs,
    ):
        super().__init__(resolver, field_type, extra_kwargs)
        self.field_class = field_class
        self.supported_field_type = supported_field_type
        self.field_kwargs = field_kwargs

    def can_use(self) -> bool:
        return self.field_type == self.supported_field_type

    def resolve(self) -> Field:
        return self.field_class(**{
            **self.extra_kwargs,
            **(self.field_kwargs or {}),
        })


class OptionalFieldResolver(FieldResolver):
    def can_use(self) -> bool:
        return (
            get_origin(self.field_type) is Union or
            get_origin(self.field_type) is UnionType
        ) and NoneType in get_args(self.field_type)

    def resolve(self) -> Field:
        args: list = list(get_args(self.field_type))
        args.remove(NoneType)

        extra_kwargs = {**self.extra_kwargs, 'required': False}
        if len(args) == 1:
            return self.resolver.get_field_by_annotation(
                args[0],
                extra_kwargs,
            )
        else:
            return self.resolver.get_field_by_annotation(
                Union[tuple(args)],
                extra_kwargs,
            )


class ListFieldResolver(FieldResolver):
    def can_use(self) -> bool:
        return get_origin(self.field_type) is list or self.field_type is list

    def resolve(self) -> Field:
        args = get_args(self.field_type)
        nested_field = None
        if args:
            nested_field = self.resolver.get_field_by_annotation(args[0], {})

        return ListField(nested_field, **self.extra_kwargs)


class NestedModelResolver(FieldResolver):
    def can_use(self) -> bool:
        try:
            return issubclass(self.field_type, Model)
        except TypeError:
            return False

    def resolve(self) -> Field:
        return NestedModelField(self.field_type, **self.extra_kwargs)


class IntOrFloatFieldResolver(FieldResolver):
    def can_use(self) -> bool:
        return (
            get_origin(self.field_type) is Union or
            get_origin(self.field_type) is UnionType
        ) and set(get_args(self.field_type)) == {int, float}

    def resolve(self) -> Field:
        return NumberField(**self.extra_kwargs)


class EnumFieldResolver(FieldResolver):
    def can_use(self) -> bool:
        return issubclass(self.field_type, Enum)

    def resolve(self) -> Field:
        return EnumField(self.field_type, **self.extra_kwargs)


NO_VALUE = object()


class AnnotationResolver:
    resolvers = [
        partial(SimpleFieldResolver, supported_field_type=int, field_class=NumberField, field_kwargs=dict(
            int_only=True)),
        partial(SimpleFieldResolver, supported_field_type=float, field_class=NumberField, field_kwargs=dict(
            float_only=True)),
        partial(SimpleFieldResolver, supported_field_type=str, field_class=TextField, field_kwargs=dict()),
        partial(SimpleFieldResolver, supported_field_type=bool, field_class=BooleanField, field_kwargs=dict()),
        partial(SimpleFieldResolver, supported_field_type=datetime, field_class=DateTime, field_kwargs=dict()),
        partial(SimpleFieldResolver, supported_field_type=dict, field_class=MapField, field_kwargs=dict()),
        partial(SimpleFieldResolver,
                supported_field_type=firestore.GeoPoint,
                field_class=GeoPoint,
                field_kwargs=dict()),
        OptionalFieldResolver,
        ListFieldResolver,
        NestedModelResolver,
        IntOrFloatFieldResolver,
        EnumFieldResolver,
    ]

    def __init__(self, namespace: dict) -> None:
        self.namespace = namespace
        self.annotations = namespace.get('__annotations__', {})

    def resolve_fields(self) -> Iterator[Tuple[str, Field]]:
        for field_name, field_type in self.annotations.items():
            value = self.namespace.get(field_name, NO_VALUE)
            if isinstance(value, Field):
                continue

            field = self.get_field_by_annotation(field_type, default=value)
            yield field_name, field

    def get_field_by_annotation(self, field_type, extra_kwargs=None, default=NO_VALUE) -> Field:
        extra_kwargs = extra_kwargs.copy() if extra_kwargs else {}
        extra_kwargs.setdefault('required', True)
        if default is not NO_VALUE:
            extra_kwargs.setdefault('default', default)

        for resolver_cls in self.resolvers:
            resolver = resolver_cls(self, field_type, extra_kwargs)
            if resolver.can_use():
                return resolver.resolve()

        raise ValueError(f'Cannot resolve field type {field_type}')
