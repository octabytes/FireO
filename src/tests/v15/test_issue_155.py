from fireo.models import Model
from fireo.fields import TextField, MapField
import fireo


def test_issue_155():

    class Test(Model):
        name = TextField()
        score_data = MapField(default={
            'field1': 0,
            'field2': 0
        })


    test1 = Test(name='test1')
    test1.save()
    test1.score_data['field1'] = 100
    test1.score_data['field2'] = 300
    test1.upsert()

    test2 = Test(name='test2')
    test2.save()
    test2.score_data['field1'] = 200
    test2.score_data['field2'] = 200
    test2.upsert()

    test3 = Test(name='test3')
    test3.save()
    test3.score_data['field1'] = 300
    test3.score_data['field2'] = 100
    test3.upsert()

    try:
        Test.collection.order('score_data.field2').fetch()
        assert True == True
    except Exception as e:
        assert True == False

