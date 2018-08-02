"""
Represents a `User`
"""

import sqlite3

class User:
    def __init__(self, username):
        self._username = username
        self.initDatabase()

    def initDatabase(self):
        """ initialize a database with this username """
        # connec to the database with that name:
        sqlite3.connect("{}.db".format(str(self._username)))