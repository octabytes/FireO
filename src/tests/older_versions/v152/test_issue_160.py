import pytest
from fireo.fields.errors import AttributeTypeError
from fireo.fields import TextField, IDField
from fireo.models import Model

# first try with default field name
def test_issue_160_default_id():

    class TestIssue160Model(Model):
        name = TextField()

    test1 = TestIssue160Model(name='test1')
    test1.save()

    test2 = TestIssue160Model(name='test2')
    test2.save()

    try:
        results = TestIssue160Model.collection.filter('__name__', 'in',
                                         [test1.id, test2.id]).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 2

        results = TestIssue160Model.collection.filter('id', 'in',
                                         [test1.id, test2.id]).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 2

        # test compound query
        results = TestIssue160Model.collection.filter('id', 'in',
                                         [test1.id, test2.id]).filter(
                                             "name", "==", test1.name).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 1

    except Exception:
        assert True == False


def test_issue_160_custom_id():

    class TestIssue160Model2(Model):
        test_id = IDField()
        name = TextField()

    test1 = TestIssue160Model2(name='test1')
    test1.save()

    test2 = TestIssue160Model2(name='test2')
    test2.save()

    try:
        results = TestIssue160Model2.collection.filter(
            '__name__', 'in', [test1.test_id, test2.test_id]).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 2

        results = TestIssue160Model2.collection.filter(
            'test_id', 'in', [test1.test_id, test2.test_id]).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 2

        # test compound query
        results = TestIssue160Model2.collection.filter(
            'test_id', 'in',
            [test1.test_id, test2.test_id]).filter("name", "==",
                                                   test1.name).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 1

    except Exception:
        assert True == False


def test_issue_160_should_throw_error_if_not_list_value():
    class TestIssue160Model(Model):
        name = TextField()

    with pytest.raises(AttributeTypeError):
        TestIssue160Model.collection.filter("id", "in", "not-list").fetch()

def test_issue_160_should_able_to_get_with_key():
    class TestIssue160Model(Model):
        name = TextField()

    test1 = TestIssue160Model(name='test1')
    test1.save()

    try:
        results = TestIssue160Model.collection.filter("id", "in", [test1.key]).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 1
    except Exception:
        assert True == False