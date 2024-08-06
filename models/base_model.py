i#!/usr/bin/python3
"""
This module contains the BaseModel class, which serves as the foundation
for other models in the application. It provides common attributes and
methods for managing models, including saving, deleting, and converting
to a dictionary representation.
"""

from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from os import getenv

# Define the time format used for datetime serialization
time = "%Y-%m-%dT%H:%M:%S.%f"

# Check the storage type and define the Base class accordingly
if models.storage_t == "db":
    # Use SQLAlchemy's declarative_base if using database storage
    Base = declarative_base()
else:
    # Use a basic object if not using database storage
    Base = object


class BaseModel:
    """
    The BaseModel class from which future classes will be derived.

    Attributes:
        id (str): Unique identifier for the instance.
        created_at (datetime): The datetime when the instance was created.
        updated_at (datetime): The datetime when the instance was last updated.
    """

    if models.storage_t == "db":
        # Define columns for database storage
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initialize a new instance of BaseModel.

        Args:
            *args: Unused.
            **kwargs: Key-value pairs for setting attributes of the instance.
        """
        # Assign a unique ID to the instance
        self.id = str(uuid.uuid4())
        # Set the creation datetime
        self.created_at = datetime.now()
        # Initialize updated_at to match created_at initially
        self.updated_at = self.created_at
        # Iterate over kwargs to set instance attributes
        for key, value in kwargs.items():
            # Skip the '__class__' attribute
            if key == '__class__':
                continue
            # Set the attribute on the instance
            setattr(self, key, value)
            # Convert created_at from string to datetime if necessary
            if isinstance(self.created_at, str):
                self.created_at = datetime.strptime(self.created_at, time)
            # Convert updated_at from string to datetime if necessary
            if isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime(self.updated_at, time)

    def __str__(self):
        """
        Return a string representation of the BaseModel instance.

        Returns:
            str: A string in the format "[ClassName] (id) {attributes}"
        """
        # Format the instance's class name, ID, and dictionary of attributes
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """
        Update the updated_at attribute and save the instance.

        This method updates the 'updated_at' attribute with the current
        datetime and saves the instance to storage.
        """
        # Update the updated_at attribute to the current datetime
        self.updated_at = datetime.utcnow()
        # Add the instance to storage
        models.storage.new(self)
        # Save changes to storage
        models.storage.save()

    def to_dict(self, secure_pwd=True):
        """
        Convert the instance to a dictionary representation.

        Args:
            secure_pwd (bool): Whether to exclude the password from the
                               dictionary.

        Returns:
            dict: A dictionary containing all keys/values of the instance.
        """
        # Create a copy of the instance's dictionary
        new_dict = self.__dict__.copy()
        # Convert created_at to a string in the specified format
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        # Convert updated_at to a string in the specified format
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        # Add the class name to the dictionary
        new_dict["__class__"] = self.__class__.__name__
        # Remove SQLAlchemy instance state if present
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        # Remove the password if secure_pwd is True
        if secure_pwd:
            if 'password' in new_dict:
                del new_dict['password']
        # Return the dictionary representation
        return new_dict

    def delete(self):
        """
        Delete the current instance from storage.

        This method removes the instance from the storage, effectively
        deleting it from persistence.
        """
        # Call the storage's delete method to remove the instance
        models.storage.delete(self)
