#!/usr/bin/python3
"""Amenity model Module"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class that inherits from BaseModel"""

    name = ""

    def __init__(self, *args, **kwargs):
        """Constructor Method"""
        super().__init__(*args, **kwargs)
