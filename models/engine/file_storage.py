#!/usr/bin/python3
"""FileStorage Module"""
import json


class FileStorage:
    """FileStorage Class that handles serialization and deserialization of objects."""

    __file_path = "storage.json"
    __objects = {}

    def all(self):
        """Returns a dictionary of all the objects saved"""
        return self.__objects

    def new(self, obj):
        """Sets a new object in the __objects dictionary"""
        self.__objects[obj.id] = obj

    def save(self):
        """Serialize the objects dictionary into a json file."""
        with open(self.__file_path, "w") as f:
            f.write(json.dumps(self.__objects))

    def reload(self):
        """Deserialize the json file into the objects dictionary."""
        try:
            with open(self.__file_path, "r") as f:
                self.__objects = json.loads(f.read())
        except FileNotFoundError:
            pass
