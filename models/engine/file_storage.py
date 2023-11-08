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
        return self.__objects

    def new(self, obj):
        """Sets a new object in the __objects dictionary"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize the objects dictionary into a json file."""
        with open(self.__file_path, "w") as f:
            # New dictionary to hold dictionary representaton of the objects
            # Convert each object into its dictionary representaton
            # Store it in the new dictionary
            # Convert the new dictionary into a json string and write that string to the file
            obj_dicts = {}
            for key, value in self.__objects.items():
                obj_dicts[key] = value.to_dict()
            f.write(json.dumps(obj_dicts))

    def reload(self):
        """Deserialize the json file into the objects dictionary."""
        try:
            with open(self.__file_path, "r") as f:
                # Load the dictionary of object dicts from the file
                # Convert each object dict into an object
                # Store each object in the __objects dictionary
                json_string = f.read()
                if json_string:
                    obj_dicts = json.loads(json_string)
                    for key, value in obj_dicts.items():
                        self.__objects[key] = BaseModel(**value)
                        """
                        Main dictionary {
                            BaseModel.1212: {att:val}
                            BaseModel.8232: {att:val}
                            BaseModel.1211: {att:val}
                            BaseModel.3222: {att:val}
                            BaseModel.0292: {att:val}
                        }
                        """
        except FileNotFoundError:
            pass
