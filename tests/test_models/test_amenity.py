#!/usr/bin/python3
"""
Defines unittests for models/amenity_model.py.

Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_unique_model_ids(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_created_at_values_for_two_models(self):
        amenity1 = Amenity()
        sleep(0.15)
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    def test_updated_at_values_for_two_models(self):
        amenity1 = Amenity()
        sleep(0.15)
        amenity2 = Amenity()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        amenity = Amenity()
        amenity.id = "7894"
        amenity.created_at = amenity.updated_at = dt
        amenitystr = amenity.__str__()
        self.assertIn("[Amenity] (7894)", amenitystr)
        self.assertIn("'id': '7894'", amenitystr)
        self.assertIn("'created_at': " + dt_repr, amenitystr)
        self.assertIn("'updated_at': " + dt_repr, amenitystr)

    def test_args_unused(self):
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    def test_instantiation_using_kwargs(self):
        date = datetime.today()
        date_iso = date.isoformat()
        amenity = Amenity(created_at=date_iso, id="789", updated_at=date_iso)
        self.assertEqual(amenity.id, "789")
        self.assertEqual(amenity.created_at, date)
        self.assertEqual(amenity.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        date = datetime.today()
        date_iso = date.isoformat()
        amenity = Amenity("40", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(amenity.created_at, date)
        self.assertEqual(amenity.updated_at, date)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        amenity = Amenity()
        sleep(0.05)
        first_updated_at = amenity.updated_at
        amenity.save()
        self.assertLess(first_updated_at, amenity.updated_at)

    def test_two_saves(self):
        amenity = Amenity()
        sleep(0.05)
        first_updated_at = amenity.updated_at
        amenity.save()
        second_updated_at = amenity.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenity.save()
        self.assertLess(second_updated_at, amenity.updated_at)

    def test_save_updates_file(self):
        amenity = Amenity()
        amenity.save()
        amenityid = "Amenity." + amenity.id
        with open("file.json", "r") as f:
            self.assertIn(amenityid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        amenity = Amenity()
        self.assertTrue(dict, type(amenity.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    def test_to_dict_contains_added_attributes(self):
        amenity = Amenity()
        amenity.language = "python"
        amenity.new_number = 90
        self.assertIn("language", amenity.to_dict())
        self.assertIn("new_number", amenity.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        amenity = Amenity()
        amenity.id = "1234"
        amenity.created_at = amenity.updated_at = dt
        tdict = {
            "id": "1234",
            "__class__": "Amenity",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertDictEqual(amenity.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        amenity = Amenity()
        self.assertNotEqual(amenity.to_dict(), amenity.__dict__)

    def test_to_dict_with_arg(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.to_dict(None)


if __name__ == "__main__":
    unittest.main()
