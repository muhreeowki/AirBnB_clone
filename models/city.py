#!/usr/bin/python3
"""City model Module"""
from models.base_model import BaseModel


class City(BaseModel):
    """City class that inherits from BaseModel"""

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """Constructor Method"""
        super().__init__(*args, **kwargs)
