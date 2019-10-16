from fireo.fields import TextField, IDField
from fireo.models import Model
from fireo.utils import utils


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
    s.id = 'student_test_some_change'
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
    u = User2(name="test_parent_save_update_different_name")
    u.user_id = 'user_test_parent_save_update_different_name'
    u.save()
    s = Student2(parent=u.key)
    s.student_id = 'student_test_parent_save_update_different_name'
    s.name = "child_name_test_parent_save_update_different_name"
    s.address = 'child_address_test_parent_save_update_different_name'
    s.save()

    s2 = Student2.collection.get(s.key)
    s2.address = 'update_child_address_test_parent_save_update_different_name'
    s2.update()

    s3 = Student2.collection.get(s.key)
    assert s3.student_id == s.student_id
    assert s3.key == s.key
    assert s3.name == 'child_name_test_parent_save_update_different_name'
    assert s3.address == 'update_child_address_test_parent_save_update_different_name'
    assert s3.id is None


class AbParent(Model):
    name = TextField()


class AbChild(Model):
    address = TextField()


def test_parent_create_get():
    p = AbParent.collection.create(name='test_parent')
    c = AbChild.collection.create(parent=p.key, address="child_address")

    assert utils.get_parent_doc(c.key) == p.key


def test_parent_create_with_obj():
    p = AbParent()
    p.name = 'test_parent'
    p.save()

    c = AbChild(parent=p.key)
    c.address = 'child_address'
    c.save()

    assert utils.get_parent_doc(c.key) == p.key


class AbParent1(Model):
    id = IDField()
    name = TextField()


class AbChild1(Model):
    id = IDField()
    address = TextField()


def test_parent_create_id():
    p = AbParent1.collection.create(id='test_parent_create_id', name='test_parent')
    c = AbChild1.collection.create(parent=p.key, id='child_create_id', address="child_address")

    assert utils.get_parent_doc(c.key) == p.key
    assert c.id == 'child_create_id'
    assert p.id == 'test_parent_create_id'


def test_parent_create_with_id():
    p = AbParent1()
    p.id = 'test_parent_create_id'
    p.name = 'test_parent'
    p.save()

    c = AbChild1(parent=p.key)
    c.id = 'child_create_id'
    c.address = 'child_address'
    c.save()

    assert utils.get_parent_doc(c.key) == p.key
    assert c.id == 'child_create_id'
    assert p.id == 'test_parent_create_id'


class AbParent2(Model):
    p_id = IDField()
    name = TextField()


class AbChild2(Model):
    c_id = IDField()
    address = TextField()


def test_parent_create_diff_name():
    p = AbParent2.collection.create(p_id='test_parent_create_id', name='test_parent')
    c = AbChild2.collection.create(parent=p.key, c_id='child_create_id', address="child_address")

    assert utils.get_parent_doc(c.key) == p.key
    assert c.c_id == 'child_create_id'
    assert p.p_id == 'test_parent_create_id'
    assert c.id is None
    assert p.id is None


def test_parent_create_with_obj_diff_name():
    p = AbParent2()
    p.p_id = 'test_parent_create_id'
    p.name = 'test_parent'
    p.save()

    c = AbChild2(parent=p.key)
    c.c_id = 'child_create_id'
    c.address = 'child_address'
    c.save()

    assert utils.get_parent_doc(c.key) == p.key
    assert c.c_id == 'child_create_id'
    assert p.p_id == 'test_parent_create_id'
    assert c.id is None
    assert p.id is None
