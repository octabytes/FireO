from fireo.fields import Field
from fireo.models import Model


class WeekDays(Field):
    pass


class User(Model):
    day = WeekDays()


def test_simple_custom_field():
    u = User(day=1)
    u.save()

    u2 = User.collection.get(u.key)
    assert u2.day == 1


class WeekDays2(Field):
    def db_value(self, val):
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        return days[val]


class User2(Model):
    day = WeekDays2()


def test_custom_db_value_extend():
    u = User2.collection.create(day=0)
    u2 = User2.collection.get(u.key)

    assert u2.day == 'Mon'


class WeekDays3(Field):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def db_value(self, val):
        return self.days[val]

    def field_value(self, val):
        return self.days.index(val)


class User3(Model):
    day = WeekDays3()


def test_custom_field_value_extend():
    u = User3.collection.create(day=0)
    u2 = User3.collection.get(u.key)

    assert u2.day == 0


class EmailGenerator(Field):
    allowed_attributes = ['suffix', 'domain']

    def attr_suffix(self, attr_val, field_val):
        return attr_val + "." + field_val

    def attr_domain(self, attr_val, field_val):
        return field_val + "@" + attr_val


class Student(Model):
    email = EmailGenerator(suffix='suffix', domain='example.com')


def test_custom_field_attributes():
    s = Student()
    s.email = 'my_email'
    s.save()

    s2 = Student.collection.get(s.key)
    assert s2.email == 'suffix.my_email@example.com'