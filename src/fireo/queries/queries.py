
class QuerySet:

    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        pass


class BaseQuery:

    def __int__(self, model):
        self.model = model

    def get_ref(self):
        pass
