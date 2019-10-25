from datetime import datetime

import fireo
from fireo.fields import IDField, TextField, BooleanField, NumberField, ListField, DateTime, GeoPoint, MapField, \
    NestedModel, ReferenceField
from fireo.models import Model


class NModel(Model):
    name = TextField()


class RModel(Model):
    name = TextField()


class CityEmptyField(Model):
    text = TextField()
    number = NumberField()
    date = DateTime()
    bool = BooleanField()
    geo_point = GeoPoint()
    list = ListField()
    map = MapField()
    nested = NestedModel(NModel)
    ref = ReferenceField(RModel)


def test_empty_text_field():
    nmodel = NModel(name="Nested Model")
    rmodel = RModel.collection.create(name="Reference Model")
    CityEmptyField.collection.create(
        number=24, date=datetime.now(), bool=True, geo_point=fireo.GeoPoint(32.32, 42.32),
        list=['abc', 'def'], map={'key':'val'}, nested=nmodel, ref=rmodel
    )


def test_empty_number_field():
    nmodel = NModel(name="Nested Model")
    rmodel = RModel.collection.create(name="Reference Model")
    CityEmptyField.collection.create(
        text="abc", date=datetime.now(), bool=True, geo_point=fireo.GeoPoint(32.32, 42.32),
        list=['abc', 'def'], map={'key':'val'}, nested=nmodel, ref=rmodel
    )


def test_empty_date_field():
    nmodel = NModel(name="Nested Model")
    rmodel = RModel.collection.create(name="Reference Model")
    CityEmptyField.collection.create(
        text="abc", number=24, bool=True, geo_point=fireo.GeoPoint(32.32, 42.32),
        list=['abc', 'def'], map={'key':'val'}, nested=nmodel, ref=rmodel
    )


def test_empty_bool_field():
    nmodel = NModel(name="Nested Model")
    rmodel = RModel.collection.create(name="Reference Model")
    CityEmptyField.collection.create(
        text="abc", number=24, date=datetime.now(), geo_point=fireo.GeoPoint(32.32, 42.32),
        list=['abc', 'def'], map={'key':'val'}, nested=nmodel, ref=rmodel
    )


def test_empty_geopoint_field():
    nmodel = NModel(name="Nested Model")
    rmodel = RModel.collection.create(name="Reference Model")
    CityEmptyField.collection.create(
        text="abc", number=24, date=datetime.now(), bool=True,
        list=['abc', 'def'], map={'key':'val'}, nested=nmodel, ref=rmodel
    )


def test_empty_list_field():
    nmodel = NModel(name="Nested Model")
    rmodel = RModel.collection.create(name="Reference Model")
    CityEmptyField.collection.create(
        text="abc", number=24, date=datetime.now(), bool=True, geo_point=fireo.GeoPoint(32.32, 42.32),
        map={'key':'val'}, nested=nmodel, ref=rmodel
    )


def test_empty_map_field():
    nmodel = NModel(name="Nested Model")
    rmodel = RModel.collection.create(name="Reference Model")
    CityEmptyField.collection.create(
        text="abc", number=24, date=datetime.now(), bool=True, geo_point=fireo.GeoPoint(32.32, 42.32),
        list=['abc', 'def'], nested=nmodel, ref=rmodel
    )


def test_empty_nested_field():
    nmodel = NModel(name="Nested Model")
    rmodel = RModel.collection.create(name="Reference Model")
    CityEmptyField.collection.create(
        text="abc", number=24, date=datetime.now(), bool=True, geo_point=fireo.GeoPoint(32.32, 42.32),
        list=['abc', 'def'], map={'key':'val'}, ref=rmodel
    )


def test_empty_reference_field():
    nmodel = NModel(name="Nested Model")
    rmodel = RModel.collection.create(name="Reference Model")
    CityEmptyField.collection.create(
        text="abc", number=24, date=datetime.now(), bool=True, geo_point=fireo.GeoPoint(32.32, 42.32),
        list=['abc', 'def'], map={'key':'val'}, nested=nmodel
    )