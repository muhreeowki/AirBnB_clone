#!/usr/bin/python3
"""
Defines unittests for models/place_model.py.

Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_new_instance_stored_in_objects(self):
        """Tests instantiation of the Place Class"""
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_str(self):
        """Tests instantiation of the Place Class"""
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        """Tests instantiation of the Place Class"""
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        """Tests instantiation of the Place Class"""
        self.assertEqual(datetime, type(Place().updated_at))

    def test_unique_model_ids(self):
        """Tests instantiation of the Place Class"""
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_created_at_values_for_two_models(self):
        """Tests instantiation of the Place Class"""
        place1 = Place()
        sleep(0.15)
        place2 = Place()
        self.assertLess(place1.created_at, place2.created_at)

    def test_updated_at_values_for_two_models(self):
        """Tests instantiation of the Place Class"""
        place1 = Place()
        sleep(0.15)
        place2 = Place()
        self.assertLess(place1.updated_at, place2.updated_at)

    def test_str_representation(self):
        """Tests instantiation of the Place Class"""
        dt = datetime.today()
        dt_repr = repr(dt)
        place = Place()
        place.id = "7894"
        place.created_at = place.updated_at = dt
        placestr = place.__str__()
        self.assertIn("[Place] (7894)", placestr)
        self.assertIn("'id': '7894'", placestr)
        self.assertIn("'created_at': " + dt_repr, placestr)
        self.assertIn("'updated_at': " + dt_repr, placestr)

    def test_args_unused(self):
        """Tests instantiation of the Place Class"""
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_instantiation_using_kwargs(self):
        """Tests instantiation of the Place Class"""
        date = datetime.today()
        date_iso = date.isoformat()
        place = Place(created_at=date_iso, id="789", updated_at=date_iso)
        self.assertEqual(place.id, "789")
        self.assertEqual(place.created_at, date)
        self.assertEqual(place.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests instantiation of the Place Class"""
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        """Tests instantiation of the Place Class"""
        date = datetime.today()
        date_iso = date.isoformat()
        place = Place("40", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(place.created_at, date)
        self.assertEqual(place.updated_at, date)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

    @classmethod
    def setUp(cls):
        """Function that sets up for the tests"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(cls):
        """Function that cleans up after the tests"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """Tests save method"""
        place = Place()
        sleep(0.05)
        first_updated_at = place.updated_at
        place.save()
        self.assertLess(first_updated_at, place.updated_at)

    def test_two_saves(self):
        """Tests save method"""
        place = Place()
        sleep(0.05)
        first_updated_at = place.updated_at
        place.save()
        second_updated_at = place.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        place.save()
        self.assertLess(second_updated_at, place.updated_at)

    def test_save_updates_file(self):
        """Tests save method"""
        place = Place()
        place.save()
        placeid = "Place." + place.id
        with open("file.json", "r") as f:
            self.assertIn(placeid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        """Tests to dict method"""
        place = Place()
        self.assertTrue(dict, type(place.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Tests to dict method"""
        place = Place()
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Tests to dict method"""
        place = Place()
        place.language = "python"
        place.new_number = 90
        self.assertIn("language", place.to_dict())
        self.assertIn("new_number", place.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Tests to dict method"""
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests to dict method"""
        dt = datetime.today()
        place = Place()
        place.id = "1234"
        place.created_at = place.updated_at = dt
        tdict = {
            "id": "1234",
            "__class__": "Place",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertDictEqual(place.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Tests to dict method"""
        place = Place()
        self.assertNotEqual(place.to_dict(), place.__dict__)

    def test_to_dict_with_arg(self):
        """Tests to dict method"""
        place = Place()
        with self.assertRaises(TypeError):
            place.to_dict(None)


if __name__ == "__main__":
    unittest.main()
