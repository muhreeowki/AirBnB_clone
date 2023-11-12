#!/usr/bin/python3
"""
Defines unittests for models/review_model.py.

Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_new_instance_stored_in_objects(self):
        """Tests instantiation of the Review Class"""
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_str(self):
        """Tests instantiation of the Review Class"""
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        """Tests instantiation of the Review Class"""
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        """Tests instantiation of the Review Class"""
        self.assertEqual(datetime, type(Review().updated_at))

    def test_unique_model_ids(self):
        """Tests instantiation of the Review Class"""
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_created_at_values_for_two_models(self):
        """Tests instantiation of the Review Class"""
        review1 = Review()
        sleep(0.15)
        review2 = Review()
        self.assertLess(review1.created_at, review2.created_at)

    def test_updated_at_values_for_two_models(self):
        """Tests instantiation of the Review Class"""
        review1 = Review()
        sleep(0.15)
        review2 = Review()
        self.assertLess(review1.updated_at, review2.updated_at)

    def test_str_representation(self):
        """Tests instantiation of the Review Class"""
        dt = datetime.today()
        dt_repr = repr(dt)
        review = Review()
        review.id = "7894"
        review.created_at = review.updated_at = dt
        reviewstr = review.__str__()
        self.assertIn("[Review] (7894)", reviewstr)
        self.assertIn("'id': '7894'", reviewstr)
        self.assertIn("'created_at': " + dt_repr, reviewstr)
        self.assertIn("'updated_at': " + dt_repr, reviewstr)

    def test_args_unused(self):
        """Tests instantiation of the Review Class"""
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_instantiation_using_kwargs(self):
        """Tests instantiation of the Review Class"""
        date = datetime.today()
        date_iso = date.isoformat()
        review = Review(created_at=date_iso, id="789", updated_at=date_iso)
        self.assertEqual(review.id, "789")
        self.assertEqual(review.created_at, date)
        self.assertEqual(review.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests instantiation of the Review Class"""
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        """Tests instantiation of the Review Class"""
        date = datetime.today()
        date_iso = date.isoformat()
        review = Review("40", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(review.created_at, date)
        self.assertEqual(review.updated_at, date)


class TestReview_save(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

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
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        self.assertLess(first_updated_at, review.updated_at)

    def test_two_saves(self):
        """Tests save method"""
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        second_updated_at = review.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        review.save()
        self.assertLess(second_updated_at, review.updated_at)

    def test_save_updates_file(self):
        """Tests save method"""
        review = Review()
        review.save()
        reviewid = "Review." + review.id
        with open("file.json", "r") as f:
            self.assertIn(reviewid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict_type(self):
        """Tests to dict method"""
        review = Review()
        self.assertTrue(dict, type(review.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Tests to dict method"""
        review = Review()
        self.assertIn("id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Tests to dict method"""
        review = Review()
        review.language = "python"
        review.new_number = 90
        self.assertIn("language", review.to_dict())
        self.assertIn("new_number", review.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Tests to dict method"""
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests to dict method"""
        dt = datetime.today()
        review = Review()
        review.id = "1234"
        review.created_at = review.updated_at = dt
        tdict = {
            "id": "1234",
            "__class__": "Review",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertDictEqual(review.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Tests to dict method"""
        review = Review()
        self.assertNotEqual(review.to_dict(), review.__dict__)

    def test_to_dict_with_arg(self):
        """Tests to dict method"""
        review = Review()
        with self.assertRaises(TypeError):
            review.to_dict(None)


if __name__ == "__main__":
    unittest.main()
