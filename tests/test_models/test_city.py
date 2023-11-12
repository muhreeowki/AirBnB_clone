#!/usr/bin/python3
"""
Defines unittests for models/city_model.py.

Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_new_instance_stored_in_objects(self):
        """Tests instantiation of the City Class"""
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_str(self):
        """Tests instantiation of the City Class"""
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        """Tests instantiation of the City Class"""
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        """Tests instantiation of the City Class"""
        self.assertEqual(datetime, type(City().updated_at))

    def test_unique_model_ids(self):
        """Tests instantiation of the City Class"""
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_created_at_values_for_two_models(self):
        """Tests instantiation of the City Class"""
        city1 = City()
        sleep(0.15)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def test_updated_at_values_for_two_models(self):
        """Tests instantiation of the City Class"""
        city1 = City()
        sleep(0.15)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_str_representation(self):
        """Tests instantiation of the City Class"""
        dt = datetime.today()
        dt_repr = repr(dt)
        city = City()
        city.id = "7894"
        city.created_at = city.updated_at = dt
        citystr = city.__str__()
        self.assertIn("[City] (7894)", citystr)
        self.assertIn("'id': '7894'", citystr)
        self.assertIn("'created_at': " + dt_repr, citystr)
        self.assertIn("'updated_at': " + dt_repr, citystr)

    def test_args_unused(self):
        """Tests instantiation of the City Class"""
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_instantiation_using_kwargs(self):
        """Tests instantiation of the City Class"""
        date = datetime.today()
        date_iso = date.isoformat()
        city = City(created_at=date_iso, id="789", updated_at=date_iso)
        self.assertEqual(city.id, "789")
        self.assertEqual(city.created_at, date)
        self.assertEqual(city.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests instantiation of the City Class"""
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        """Tests instantiation of the City Class"""
        date = datetime.today()
        date_iso = date.isoformat()
        city = City("40", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(city.created_at, date)
        self.assertEqual(city.updated_at, date)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

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
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        self.assertLess(first_updated_at, city.updated_at)

    def test_two_saves(self):
        """Tests save method"""
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        second_updated_at = city.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city.save()
        self.assertLess(second_updated_at, city.updated_at)

    def test_save_updates_file(self):
        """Tests save method"""
        city = City()
        city.save()
        cityid = "City." + city.id
        with open("file.json", "r") as f:
            self.assertIn(cityid, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        """Tests to dict method"""
        city = City()
        self.assertTrue(dict, type(city.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Tests to dict method"""
        city = City()
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Tests to dict method"""
        city = City()
        city.language = "python"
        city.new_number = 90
        self.assertIn("language", city.to_dict())
        self.assertIn("new_number", city.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Tests to dict method"""
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests to dict method"""
        dt = datetime.today()
        city = City()
        city.id = "1234"
        city.created_at = city.updated_at = dt
        tdict = {
            "id": "1234",
            "__class__": "City",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Tests to dict method"""
        city = City()
        self.assertNotEqual(city.to_dict(), city.__dict__)

    def test_to_dict_with_arg(self):
        """Tests to dict method"""
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)


if __name__ == "__main__":
    unittest.main()
