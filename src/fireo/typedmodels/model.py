from fireo.models import Model
from fireo.typedmodels.model_meta import TypedModelMeta


class TypedModel(Model, metaclass=TypedModelMeta):
    """Model with fields generation by type annotation

    Example:
        >>> from typing import List
        >>> from fireo.typedmodels import TypedModel
        >>> class Comment(TypedModel):
        ...     text: str
        ...     likes: int = 0
        >>> class User(TypedModel):
        ...     name: str
        ...     age: int
        ...     comments: List[Comment] = [] # Mutable default value is safe to use
        >>> # Use the model as usual:
        >>> user = User(name='John', age=30)
        >>> user.save()

    Note: postoned type annotation is not supported (e.g. `comments: 'List[Comment]'`)
    """

    class Meta:
        abstract = True
