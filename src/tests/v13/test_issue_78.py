from fireo.fields import TextField, ReferenceField
from fireo.models import Model


def test_issue_78():
    class UserIssue78(Model):
        name = TextField()
   
    class AddressIssue78(Model):
        user = ReferenceField(UserIssue78)
        address_name = TextField()

    # create user and address
    user = UserIssue78.collection.create(name="tester")
    address = AddressIssue78.collection.create(user=user, address_name="address name")
    
    # query Address by user (ReferenceField)
    get_address = AddressIssue78.collection.filter(user=user._reference).get()
    assert get_address.id == address.id
    assert get_address.address_name == address.address_name
