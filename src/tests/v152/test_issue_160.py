import fireo
from fireo.fields import TextField, IDField
from fireo.models import Model


# first try with default field name
def test_issue_160_default_id():

    class Test(Model):
        name = TextField()

    test1 = Test(name='test1')
    test1.save()

    test2 = Test(name='test2')
    test2.save()

    try:
        results = Test.collection.filter('__name__', 'in',
                                         [test1.id, test2.id]).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 2

        results = Test.collection.filter('id', 'in',
                                         [test1.id, test2.id]).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 2

        # test compound query
        results = Test.collection.filter('id', 'in',
                                         [test1.id, test2.id]).filter(
                                             "name", "==", test1.name).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 1

    except Exception:
        assert True == False


def test_issue_160_custom_id():

    class Test(Model):
        test_id = IDField()
        name = TextField()

    test1 = Test(name='test1')
    test1.save()

    test2 = Test(name='test2')
    test2.save()

    try:
        results = Test.collection.filter(
            '__name__', 'in', [test1.test_id, test2.test_id]).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 2

        results = Test.collection.filter(
            'test_id', 'in', [test1.test_id, test2.test_id]).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 2

        # test compound query
        results = Test.collection.filter(
            'test_id', 'in',
            [test1.test_id, test2.test_id]).filter("name", "==",
                                                   test1.name).fetch()
        num_results = sum(1 for _ in results)
        assert num_results == 1

    except Exception:
        assert True == False
