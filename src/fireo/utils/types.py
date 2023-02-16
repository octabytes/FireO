from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from fireo.models import Model


@dataclass(frozen=True)
class DumpOptions:
    """Options for dumping a model to a FireStore dictionary."""

    ignore_required: bool = False
    """Ignore required fields or not mostly ignore when updating the document."""

    ignore_default: bool = False
    """Ignore default fields or not mostly ignore when updating the document."""

    ignore_default_none: bool = False
    """Ignore default None values. Mostly used during creation of document.
    Used in NestedModelField."""

    ignore_unchanged: bool = False
    """Ignore fields which are not changed when updating the document.
    Used in NestedModelField."""


@dataclass(frozen=True)
class LoadOptions:
    """Options for loading a FireStore dictionary to a model."""

    model: 'Optional[Model]' = None
    """Model instance that contains that field."""

    stored: bool = False
    """Is the field stored in FireStore or not."""

    merge: bool = False
    """Merge data with existing data or not. Mostly used in NestedModelField."""

    by_column_name: bool = False
    """Load data by column name or not. Mostly used in NestedModelField."""
