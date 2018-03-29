#!/usr/bin/python3
"""
    This module defines the BaseModel class
"""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """
        Base class for other classes to be used for the duration.
    """
    id = Column(String(60), primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
            Initialize public instance attributes.
        """

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            if 'created_at' in kwargs:
                kwargs["created_at"] = datetime.strptime(kwargs["created_at"],
                                                         "%Y-%m-%dT%H:%M:%S.%f")
            if 'updated_at' in kwargs:
                kwargs["updated_at"] = datetime.strptime(kwargs["updated_at"],
                                                         "%Y-%m-%dT%H:%M:%S.%f")

            for key, value in kwargs.items():
                if "__class__" not in key:
                    setattr(self, key, value)

    def __str__(self):
        """
            Return string representation of BaseModel class
        """
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def __repr__(self):
        """
            Return string representation of BaseModel class
        """
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        """
            Update the updated_at attribute with new.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
            Return dictionary representation of BaseModel class.
        """
        cp_dct = dict(self.__dict__)
        cp_dct['__class__'] = self.__class__.__name__
        cp_dct['updated_at'] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        cp_dct['created_at'] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        if '_sa_instance_state' in cp_dct:
            del cp_dct['_sa_instance_state']
        return (cp_dct)

    def delete(self):
        """
        Public instance method to delete current instance from storage
        """
        models.storage.delete(self)
