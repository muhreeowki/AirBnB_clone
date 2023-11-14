#!/usr/bin/python3
"""
Defines unittests for models/user_model.py.

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
    
    def test_attributes(self):
        """Test attributes of the User Class"""

        User.email = 'user.email'
        User.first_name = 'John'
        User.last_name = 'Smith'
        User.password = '1234'
        self.assertEqual(str, type(User.email))
        self.assertEqual(str, type(User.first_name))
        self.assertEqual(str, type(User.last_name))
        self.assertEqual(str, type(User.password))

    def test_new_instance_stored_in_objects(self):
        """Tests instantiation of the User Class"""
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_str(self):
        """Tests instantiation of the User Class"""
        self.assertEqual(str, type(User().id))

    def test_created_at_is_public_datetime(self):
        """Tests instantiation of the User Class"""
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_public_datetime(self):
        """Tests instantiation of the User Class"""
        self.assertEqual(datetime, type(User().updated_at))

    def test_unique_model_ids(self):
        """Tests instantiation of the User Class"""
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_created_at_values_for_two_models(self):
        """Tests instantiation of the User Class"""
        user1 = User()
        sleep(0.15)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_updated_at_values_for_two_models(self):
        """Tests instantiation of the User Class"""
        user1 = User()
        sleep(0.15)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_str_representation(self):
        """Tests instantiation of the User Class"""
        dt = datetime.today()
        dt_repr = repr(dt)
        user = User()
        user.id = "7894"
        user.created_at = user.updated_at = dt
        userstr = user.__str__()
        self.assertIn("[User] (7894)", userstr)
        self.assertIn("'id': '7894'", userstr)
        self.assertIn("'created_at': " + dt_repr, userstr)
        self.assertIn("'updated_at': " + dt_repr, userstr)

    def test_args_unused(self):
        """Tests instantiation of the User Class"""
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_instantiation_using_kwargs(self):
        """Tests instantiation of the User Class"""
        date = datetime.today()
        date_iso = date.isoformat()
        user = User(created_at=date_iso, id="789", updated_at=date_iso)
        self.assertEqual(user.id, "789")
        self.assertEqual(user.created_at, date)
        self.assertEqual(user.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests instantiation of the User Class"""
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        """Tests instantiation of the User Class"""
        date = datetime.today()
        date_iso = date.isoformat()
        user = User("40", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(user.created_at, date)
        self.assertEqual(user.updated_at, date)


class TestUser_save(unittest.TestCase):
    """Unittests for testing save method of the User class."""

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
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    def test_two_saves(self):
        """Tests save method"""
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        second_updated_at = user.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        user.save()
        self.assertLess(second_updated_at, user.updated_at)

    def test_save_updates_file(self):
        """Tests save method"""
        user = User()
        user.save()
        userid = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(userid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dict_type(self):
        """Tests to dict method"""
        user = User()
        self.assertTrue(dict, type(user.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Tests to dict method"""
        user = User()
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Tests to dict method"""
        user = User()
        user.language = "python"
        user.new_number = 90
        self.assertIn("language", user.to_dict())
        self.assertIn("new_number", user.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Tests to dict method"""
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests to dict method"""
        dt = datetime.today()
        user = User()
        user.id = "1234"
        user.created_at = user.updated_at = dt
        tdict = {
            "id": "1234",
            "__class__": "User",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertDictEqual(user.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Tests to dict method"""
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def test_to_dict_with_arg(self):
        """Tests to dict method"""
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)


if __name__ == "__main__":
    unittest.main()
