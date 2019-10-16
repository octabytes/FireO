from fireo.fields import TextField, IDField
from fireo.models import Model


class User(Model):
    name = TextField()


class Student(Model):
    name = TextField()
    address = TextField()


def test_parent_save_update():
    u = User(name="parent_test_parent_save_update")
    u.save()
    s = Student(parent=u.key)
    s.name = "child_name_test_parent_save_update"
    s.address = 'child_address_test_parent_save_update'
    s.save()

    s2 = Student.collection.get(s.key)
    s2.address = 'update_child_address_test_parent_save_update'
    s2.update()

    s3 = Student.collection.get(s.key)
    assert s3.id == s.id
    assert s3.key == s.key
    assert s3.name == 'child_name_test_parent_save_update'
    assert s3.address == 'update_child_address_test_parent_save_update'


def test_parent_save_update_with_id():
    u = User(name="test_parent_save_update_with_id")
    u.id = 'user_test_parent_save_update_with_id'
    u.save()
    s = Student(parent=u.key)
    s.id = 'student_test_parent_save_update_with_id'
    s.name = "child_name_test_parent_save_update_with_id"
    s.address = 'child_address_test_parent_save_update_with_id'
    s.save()

    s2 = Student.collection.get(s.key)
    s2.address = 'update_child_address_test_parent_save_update_with_id'
    s2.update()

    s3 = Student.collection.get(s.key)
    assert s3.id == s.id
    assert s3.key == s.key
    assert s3.name == 'child_name_test_parent_save_update_with_id'
    assert s3.address == 'update_child_address_test_parent_save_update_with_id'
    assert s3.id != 'student_test_parent_save_update_with_id'


class User1(Model):
    id = IDField()
    name = TextField()


class Student1(Model):
    id = IDField()
    name = TextField()
    address = TextField()


def test_parent_save_update_with_id_field():
    u = User(name="test_parent_save_update_with_id_field")
    u.id = 'user_test_parent_save_update_with_id_field'
    u.save()
    s = Student(parent=u.key)
    s.id = 'student_test_parent_save_update_with_id_field'
    s.name = "child_name_test_parent_save_update_with_id_field"
    s.address = 'child_address_test_parent_save_update_with_id_field'
    s.save()

    s2 = Student.collection.get(s.key)
    s2.address = 'update_child_address_test_parent_save_update_with_id_field'
    s2.update()

    s3 = Student.collection.get(s.key)
    assert s3.id == s.id
    assert s3.key == s.key
    assert s3.name == 'child_name_test_parent_save_update_with_id_field'
    assert s3.address == 'update_child_address_test_parent_save_update_with_id_field'
    assert s3.id == 'student_test_parent_save_update_with_id_field'


def test_parent_save_update_without_value():
    u = User(name="test_parent_save_update_without_value")
    u.save()
    s = Student(parent=u.key)
    s.name = "child_name_test_parent_save_update_without_value"
    s.address = 'child_address_test_parent_save_update_without_value'
    s.save()

    s2 = Student.collection.get(s.key)
    s2.address = 'update_child_address_test_parent_save_update_without_value'
    s2.update()

    s3 = Student.collection.get(s.key)
    assert s3.id == s.id
    assert s3.key == s.key
    assert s3.name == 'child_name_test_parent_save_update_without_value'
    assert s3.address == 'update_child_address_test_parent_save_update_without_value'


class User2(Model):
    user_id = IDField()
    name = TextField()


class Student2(Model):
    student_id = IDField()
    name = TextField()
    address = TextField()


def test_parent_save_update_different_name():
    u = User(name="test_parent_save_update_different_name")
    u.user_id = 'user_test_parent_save_update_different_name'
    u.save()
    s = Student(parent=u.key)
    s.student_id = 'student_test_parent_save_update_different_name'
    s.name = "child_name_test_parent_save_update_different_name"
    s.address = 'child_address_test_parent_save_update_different_name'
    s.save()

    s2 = Student.collection.get(s.key)
    s2.address = 'update_child_address_test_parent_save_update_different_name'
    s2.update()

    s3 = Student.collection.get(s.key)
    assert s3.student_id == s.student_id
    assert s3.key == s.key
    assert s3.name == 'child_name_test_parent_save_update_different_name'
    assert s3.address == 'update_child_address_test_parent_save_update_different_name'
    assert s3.id is None
