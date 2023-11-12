#!/usr/bin/python3
"""FileStorage Module"""

import json
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models.state import State


class FileStorage:
    """
    FileStorage Class that handles serialization
    and deserialization of objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns a dictionary of all the objects saved"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets a new object in the __objects dictionary"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize the objects dictionary into a json file."""
        with open(self.__file_path, "w") as f:
            obj_dicts = {}
            for key, value in FileStorage.__objects.items():
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
                        class_name, id = key.split(".")
                        FileStorage.__objects[key] = eval(f"{class_name}(**value)")
        except FileNotFoundError:
            pass
