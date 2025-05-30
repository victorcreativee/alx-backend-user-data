#!/usr/bin/env python3
"""Initialize models package and storage engine"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
