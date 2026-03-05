#!/usr/bin/env python3

'''
NinjaArt - Network Infrastructure Penetration Testing Tool
Copyright (c) 2020 SECFORCE (Antonio Quina and Leonidas Stavliotis)

    This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.scoping import scoped_session
from PyQt5.QtCore import QSemaphore
#from tables import *
import time
# temp
import threading

Base = declarative_base()

# Wrapper class to provide dictionary-like and attribute access to SQLAlchemy Row objects
class DictRow:
    def __init__(self, row):
        self._row = row
        self._mapping = row._mapping if hasattr(row, '_mapping') else {}

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._row[key]
        return self._mapping[key]

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        try:
            return self._mapping[name]
        except KeyError:
            raise AttributeError(f"'DictRow' object has no attribute '{name}'")

    def __iter__(self):
        return iter(self._row)

    def __len__(self):
        return len(self._row)

    def keys(self):
        return self._mapping.keys()

# Wrapper for query results to support fetchall/fetchone with dict-like rows
class ResultWrapper:
    def __init__(self, rows):
        self._rows = [DictRow(row) for row in rows]
        self._index = 0

    def fetchall(self):
        return self._rows

    def fetchone(self):
        if self._index < len(self._rows):
            row = self._rows[self._index]
            self._index += 1
            return row
        return None

    def first(self):
        return self._rows[0] if self._rows else None

class Database:
    def __init__(self, dbfilename):
        
        try:
            self.connect(dbfilename)
            #setup_all()
            #create_all()
        
        except Exception as e:
            print('[-] Could not create database. Please try again.')
            print(e)

    def openDB(self, dbfilename):
        
        try:
            self.connect(dbfilename)
            #setup_all()
        
        except Exception as e:
            print('[-] Could not open database file. Is the file corrupted?')
            print(e)

    def connect(self, dbfilename):
        self.name = dbfilename
        self.dbsemaphore = QSemaphore(1)                            # to control concurrent write access to db
        self.engine = create_engine('sqlite:///'+dbfilename, connect_args={"check_same_thread": False})
        self.session = scoped_session(sessionmaker())
        self.session.configure(bind=self.engine, autoflush=False)
        self.metadata = Base.metadata
        self.metadata.create_all(self.engine)
        self.metadata.echo = True
        self.metadata.bind = self

    # SQLAlchemy 2.0 compatible execute method
    def execute(self, query, *args):
        # Convert ? placeholders to :paramN style for SQLAlchemy 2.0
        param_count = query.count('?')
        params = {}
        for i in range(param_count):
            query = query.replace('?', f':param{i}', 1)
            if i < len(args):
                params[f'param{i}'] = args[i]

        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            rows = result.fetchall()
            return ResultWrapper(rows)


    # this function commits any modified data to the db, ensuring no concurrent write access to the DB (within the same thread)
    # if you code a thread that writes to the DB, make sure you acquire/release at the beginning/end of the thread (see nmap importer)
    def commit(self):
        self.dbsemaphore.acquire()

        try:
            session = self.session
            session.commit()
        
        except Exception as e:
            print("[-] Could not commit to DB.")
            print(e)

        self.dbsemaphore.release()
