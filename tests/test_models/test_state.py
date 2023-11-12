#!/usr/bin/python3
"""
Defines unittests for models/state_model.py.

Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_new_instance_stored_in_objects(self):
        """Tests instantiation of the State Class"""
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_str(self):
        """Tests instantiation of the State Class"""
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        """Tests instantiation of the State Class"""
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        """Tests instantiation of the State Class"""
        self.assertEqual(datetime, type(State().updated_at))

    def test_unique_model_ids(self):
        """Tests instantiation of the State Class"""
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_created_at_values_for_two_models(self):
        """Tests instantiation of the State Class"""
        state1 = State()
        sleep(0.15)
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)

    def test_updated_at_values_for_two_models(self):
        """Tests instantiation of the State Class"""
        state1 = State()
        sleep(0.15)
        state2 = State()
        self.assertLess(state1.updated_at, state2.updated_at)

    def test_str_representation(self):
        """Tests instantiation of the State Class"""
        dt = datetime.today()
        dt_repr = repr(dt)
        state = State()
        state.id = "7894"
        state.created_at = state.updated_at = dt
        statestr = state.__str__()
        self.assertIn("[State] (7894)", statestr)
        self.assertIn("'id': '7894'", statestr)
        self.assertIn("'created_at': " + dt_repr, statestr)
        self.assertIn("'updated_at': " + dt_repr, statestr)

    def test_args_unused(self):
        """Tests instantiation of the State Class"""
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    def test_instantiation_using_kwargs(self):
        """Tests instantiation of the State Class"""
        date = datetime.today()
        date_iso = date.isoformat()
        state = State(created_at=date_iso, id="789", updated_at=date_iso)
        self.assertEqual(state.id, "789")
        self.assertEqual(state.created_at, date)
        self.assertEqual(state.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests instantiation of the State Class"""
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        """Tests instantiation of the State Class"""
        date = datetime.today()
        date_iso = date.isoformat()
        state = State("40", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(state.created_at, date)
        self.assertEqual(state.updated_at, date)


class TestState_save(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        self.assertLess(first_updated_at, state.updated_at)

    def test_two_saves(self):
        """Tests save method"""
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        second_updated_at = state.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        state.save()
        self.assertLess(second_updated_at, state.updated_at)

    def test_save_updates_file(self):
        """Tests save method"""
        state = State()
        state.save()
        stateid = "State." + state.id
        with open("file.json", "r") as f:
            self.assertIn(stateid, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_type(self):
        """Tests to dict method"""
        state = State()
        self.assertTrue(dict, type(state.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Tests to dict method"""
        state = State()
        self.assertIn("id", state.to_dict())
        self.assertIn("created_at", state.to_dict())
        self.assertIn("updated_at", state.to_dict())
        self.assertIn("__class__", state.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Tests to dict method"""
        state = State()
        state.language = "python"
        state.new_number = 90
        self.assertIn("language", state.to_dict())
        self.assertIn("new_number", state.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Tests to dict method"""
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests to dict method"""
        dt = datetime.today()
        state = State()
        state.id = "1234"
        state.created_at = state.updated_at = dt
        tdict = {
            "id": "1234",
            "__class__": "State",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertDictEqual(state.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Tests to dict method"""
        state = State()
        self.assertNotEqual(state.to_dict(), state.__dict__)

    def test_to_dict_with_arg(self):
        """Tests to dict method"""
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict(None)


if __name__ == "__main__":
    unittest.main()
