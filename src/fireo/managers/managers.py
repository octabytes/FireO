from fireo.queries import queries


class ManagerErr(Exception):
    pass


class ManagerDescriptor:

    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        if instance is not None:
            raise ManagerErr(f"Manager can not accessible via {owner.__name__} instance")
        return self.manager


class Manager:

    def __init__(self):
        self.model = None
        self.name = None

    def initialize(self, model):
        self.model = model

    def contribute_to_model(self, model_cls, name="collection"):
        self.name = name
        setattr(model_cls, name, ManagerDescriptor(self))

    @property
    def queryset(self):
        return queries.QuerySet(self.model)

    def create(self, **kwargs):
        return self.queryset.create(**kwargs)