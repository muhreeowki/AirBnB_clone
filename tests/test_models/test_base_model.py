#!/usr/bin/python3
"""
Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_new_instance_stored_in_objects(self):
        """Tests instantiation of the BaseModel Class"""
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_str(self):
        """Tests that id is a str"""
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        """Tests created_at type of the BaseModel Class"""
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        """Tests updated_at type of the BaseModel Class"""
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_unique_model_ids(self):
        """Tests uuid of the BaseModel Class"""
        base1 = BaseModel()
        base2 = BaseModel()
        self.assertNotEqual(base1.id, base2.id)

    def test_created_at_values_for_two_models(self):
        """Tests created_at attributes of the BaseModel Class"""
        base1 = BaseModel()
        sleep(0.15)
        base2 = BaseModel()
        self.assertLess(base1.created_at, base2.created_at)

    def test_updated_at_values_for_two_models(self):
        """Tests updated_at attributes of the BaseModel Class"""
        base1 = BaseModel()
        sleep(0.15)
        base2 = BaseModel()
        self.assertLess(base1.updated_at, base2.updated_at)

    def test_str_representation(self):
        """Tests string representation of the BaseModel Class"""
        dt = datetime.today()
        dt_repr = repr(dt)
        base = BaseModel()
        base.id = "7894"
        base.created_at = base.updated_at = dt
        basestr = base.__str__()
        self.assertIn("[BaseModel] (7894)", basestr)
        self.assertIn("'id': '7894'", basestr)
        self.assertIn("'created_at': " + dt_repr, basestr)
        self.assertIn("'updated_at': " + dt_repr, basestr)

    def test_args_unused(self):
        """Tests instantiation of the BaseModel Class without using args"""
        base = BaseModel(None)
        self.assertNotIn(None, base.__dict__.values())

    def test_instantiation_using_kwargs(self):
        """Tests instantiation of the BaseModel Class using kwargs"""
        date = datetime.today()
        date_iso = date.isoformat()
        base = BaseModel(created_at=date_iso, id="789", updated_at=date_iso)
        self.assertEqual(base.id, "789")
        self.assertEqual(base.created_at, date)
        self.assertEqual(base.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests instantiation of the BaseModel Class with None kwargs"""
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        """Tests instantiation of the BaseModel Class
        with both args and kwargs"""
        date = datetime.today()
        date_iso = date.isoformat()
        base = BaseModel("40", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(base.created_at, date)
        self.assertEqual(base.updated_at, date)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

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
        """Tests save method with one save"""
        base = BaseModel()
        sleep(0.05)
        first_updated_at = base.updated_at
        base.save()
        self.assertLess(first_updated_at, base.updated_at)

    def test_two_saves(self):
        """Tests save method with two saves"""
        base = BaseModel()
        sleep(0.05)
        first_updated_at = base.updated_at
        base.save()
        second_updated_at = base.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base.save()
        self.assertLess(second_updated_at, base.updated_at)

    def test_save_updates_file(self):
        """Tests save method updates file"""
        base = BaseModel()
        base.save()
        baseid = "BaseModel." + base.id
        with open("file.json", "r") as f:
            self.assertIn(baseid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        """Tests to dict method return type"""
        base = BaseModel()
        self.assertTrue(dict, type(base.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Tests to dict method contains correct keys"""
        base = BaseModel()
        self.assertIn("id", base.to_dict())
        self.assertIn("created_at", base.to_dict())
        self.assertIn("updated_at", base.to_dict())
        self.assertIn("__class__", base.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Tests to dict method with added attributes"""
        base = BaseModel()
        base.language = "python"
        base.new_number = 90
        self.assertIn("language", base.to_dict())
        self.assertIn("new_number", base.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Tests to dict method datetime attributes are strings"""
        base = BaseModel()
        base_dict = base.to_dict()
        self.assertEqual(str, type(base_dict["created_at"]))
        self.assertEqual(str, type(base_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests to dict method output"""
        dt = datetime.today()
        base = BaseModel()
        base.id = "1234"
        base.created_at = base.updated_at = dt
        tdict = {
            "id": "1234",
            "__class__": "BaseModel",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertDictEqual(base.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Tests to dict method dunder dict"""
        base = BaseModel()
        self.assertNotEqual(base.to_dict(), base.__dict__)

    def test_to_dict_with_arg(self):
        """Tests to dict method with args"""
        base = BaseModel()
        with self.assertRaises(TypeError):
            base.to_dict(None)


if __name__ == "__main__":
    unittest.main()
