#!/usr/bin/python3
"""
Defines unittests for models/base_model.py.

Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_two_models_unique_ids(self):
        um1 = User()
        um2 = User()
        self.assertNotEqual(um1.id, um2.id)

    def test_two_models_different_created_at(self):
        um1 = User()
        sleep(0.05)
        um2 = User()
        self.assertLess(um1.created_at, um2.created_at)

    def test_two_models_different_updated_at(self):
        um1 = User()
        sleep(0.05)
        um2 = User()
        self.assertLess(um1.updated_at, um2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        um = User()
        um.id = "123456"
        um.created_at = um.updated_at = dt
        umstr = um.__str__()
        self.assertIn("[User] (123456)", umstr)
        self.assertIn("'id': '123456'", umstr)
        self.assertIn("'created_at': " + dt_repr, umstr)
        self.assertIn("'updated_at': " + dt_repr, umstr)

    def test_args_unused(self):
        um = User(None)
        self.assertNotIn(None, um.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        um = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(um.id, "345")
        self.assertEqual(um.created_at, dt)
        self.assertEqual(um.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        um = User("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(um.id, "345")
        self.assertEqual(um.created_at, dt)
        self.assertEqual(um.updated_at, dt)


class TestUser_save(unittest.TestCase):
    """Unittests for testing save method of the User class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        um = User()
        sleep(0.05)
        first_updated_at = um.updated_at
        um.save()
        self.assertLess(first_updated_at, um.updated_at)

    def test_two_saves(self):
        um = User()
        sleep(0.05)
        first_updated_at = um.updated_at
        um.save()
        second_updated_at = um.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        um.save()
        self.assertLess(second_updated_at, um.updated_at)

    def test_save_with_arg(self):
        um = User()
        with self.assertRaises(TypeError):
            um.save(None)

    def test_save_updates_file(self):
        um = User()
        um.save()
        umid = "User." + um.id
        with open("file.json", "r") as f:
            self.assertIn(umid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dict_type(self):
        um = User()
        self.assertTrue(dict, type(um.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        um = User()
        self.assertIn("id", um.to_dict())
        self.assertIn("created_at", um.to_dict())
        self.assertIn("updated_at", um.to_dict())
        self.assertIn("__class__", um.to_dict())

    def test_to_dict_contains_added_attributes(self):
        um = User()
        um.name = "Holberton"
        um.my_number = 98
        self.assertIn("name", um.to_dict())
        self.assertIn("my_number", um.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        um = User()
        um_dict = um.to_dict()
        self.assertEqual(str, type(um_dict["created_at"]))
        self.assertEqual(str, type(um_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        um = User()
        um.id = "123456"
        um.created_at = um.updated_at = dt
        tdict = {
            "id": "123456",
            "__class__": "User",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertDictEqual(um.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        um = User()
        self.assertNotEqual(um.to_dict(), um.__dict__)

    def test_to_dict_with_arg(self):
        um = User()
        with self.assertRaises(TypeError):
            um.to_dict(None)


if __name__ == "__main__":
    unittest.main()
