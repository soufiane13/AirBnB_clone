#!/usr/bin/python3
"""A script of the base model"""

import uuid
from datetime import datetime
from models import storage

class BaseModel:

    """The Parent Class from which all other classes will inherit"""

    def __init__(self, *args, **kwargs):
        """Initializes All instance attributes

        Args:
            - *args: list of arguments
            - **kwargs: dict of key-values arguments
        """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
    

    def __str__(self):
        """Returns official string representation of the BaseModel instance."""
        cName = self.__class__.__name__
        return "[{}] ({}) {}".format(cName, self.id, self.__dict__)
    
    def save(self):
        """updates the public instance attribute updated_at"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        
        """returns a dictionary containing all keys/values of __dict__"""

        r_dict = self.__dict__.copy()
        r_dict["created_at"] = self.created_at.isoformat()
        r_dict["updated_at"] = self.updated_at.isoformat()
        r_dict["__class__"] = self.__class__.__name__
        return r_dict
