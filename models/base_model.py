#!/usr/bin/python3
"""
Base Model Module 
"""
import uuid
from datetime import datetime


class BaseModel:
    """BaseModel Class"""

    def __init__(self, *args, **kwargs):
        """Constructor Method"""
        if kwargs:
            for key, value in kwargs.items():
                if key in ('created_at', 'updated_at'):
                    date = datetime.fromisoformat(value)
                    setattr(self, key, date)
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()


    def __str__(self):
        """Returns string representation of the object"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute updated_at with the current datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__ of the instance"""
        dict_represntation = self.__dict__
        dict_represntation["__class__"] = self.__class__.__name__
        dict_represntation["created_at"] = self.created_at.isoformat()
        dict_represntation["updated_at"] = self.updated_at.isoformat()
        return dict_represntation
