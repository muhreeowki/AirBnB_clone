#!/usr/bin/python3
"""FileStorage Module"""
import json
from models.base_model import BaseModel


class FileStorage:
    """FileStorage Class that handles serialization and deserialization of objects."""

    __file_path = "storage.json"
    __objects = {}

    def all(self):
        """Returns a dictionary of all the objects saved"""
        return self.__objects.copy()

    def new(self, obj):
        """Sets a new object in the __objects dictionary"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize the objects dictionary into a json file."""
        with open(self.__file_path, "w") as f:
            obj_dicts = {}
            for key, value in self.__objects.items():
                obj_dicts[key] = value.to_dict()
            f.write(json.dumps(obj_dicts))

    def reload(self):
        """Deserialize the json file into the objects dictionary."""
        try:
            with open(self.__file_path, "r") as f:
                json_string = f.read()
                if json_string:
                    obj_dicts = json.loads(json_string)
                    for key, value in obj_dicts.items():
                        self.__objects[key] = BaseModel(**value)
        except FileNotFoundError:
            pass
