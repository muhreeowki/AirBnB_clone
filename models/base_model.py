#!/usr/bin/python3
"""Module that creates the BaseModel class"""
import uuid
import models
from datetime import datetime


class BaseModel:
    """BaseModel Class that is used by all other Classes"""

    def __init__(self, *args, **kwargs):
        """Constructor Method"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    date = datetime.fromisoformat(value)
                    setattr(self, key, date)
                elif key != "__class__":
                    setattr(self, key, value)
        else:
            models.storage.new(self)

    def __str__(self):
        """Returns string representation of the object"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all
        keys/values of __dict__ of the instance
        """
        dict_represntation = self.__dict__.copy()
        dict_represntation["__class__"] = self.__class__.__name__
        dict_represntation["created_at"] = self.created_at.isoformat()
        dict_represntation["updated_at"] = self.updated_at.isoformat()
        return dict_represntation
