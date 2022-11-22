from fireo.models.errors import DuplicateIDField
import pytest
from fireo.fields import TextField, IDField
from fireo.models import Model


def test_issue_162_duplicate_id_fields():
    with pytest.raises(DuplicateIDField):
        class Test(Model):
            id = IDField()
            id2 = IDField()
            name = TextField()
