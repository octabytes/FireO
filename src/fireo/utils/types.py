from dataclasses import dataclass


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
