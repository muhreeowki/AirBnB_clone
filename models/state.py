#!/usr/bin/python3
"""State model Module"""
from models.base_model import BaseModel


class State(BaseModel):
    """State class that inherits from BaseModel"""
    name = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
