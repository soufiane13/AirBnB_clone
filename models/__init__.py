#!/usr/bin/python3

""" method To Initializes the package"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
