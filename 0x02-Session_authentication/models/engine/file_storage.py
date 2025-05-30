#!/usr/bin/env python3
"""
Defines FileStorage class to serialize and deserialize user data
"""

import json
from os import path
from models.user import User


class FileStorage:
    """Serializes and deserializes user instances to/from a JSON file"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of all objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to storage dictionary"""
        if obj and hasattr(obj, 'id'):
            key = "{}.{}".format(type(obj).__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """Serializes objects to the JSON file"""
        obj_dict = {
            k: v.to_dict()
            for k, v in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes JSON file to objects if file exists"""
        if not path.exists(FileStorage.__file_path):
            return
        try:
            with open(FileStorage.__file_path, 'r') as f:
                obj_dict = json.load(f)
                for k, val in obj_dict.items():
                    if val['__class__'] == 'User':
                        self.new(User(**val))
        except Exception:
            pass
