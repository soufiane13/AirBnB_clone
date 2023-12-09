#!/usr/bin/python3
"""This module creates a User class."""
from models.base_model import BaseModel

class State(BaseModel):
    """Represent a state.

    Attributes:
        name (str): The name of the state.
    """

    name = ""
