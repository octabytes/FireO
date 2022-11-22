from fireo.fields import TextField, NumberField
from fireo.models import Model


def test_fix_issue_45():
    class Student(Model):
        name = TextField()
        age = NumberField()

    s = Student()
    s.name = 'abc'
    s.age = 7
    s.save()

    student = Student.collection.get(s.key)
    
    assert student.key == s.key

    student.age = 10
    student.save()

    assert student.key == s.key
    
    student.save()

    assert student.key == s.key

    student.save()

    assert student.key == s.key
