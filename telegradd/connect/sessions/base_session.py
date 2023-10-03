import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
import sqlite3
import pathlib
dir_path = pathlib.Path.cwd()
dirs = str(dir_path).split('\\')


@dataclass
class Session(ABC):
    EXTENSION = '.session'
    FULL_PATH = str(pathlib.Path(__file__).parents[3])
    _telethon_base_path = '\\'.join ([FULL_PATH, 'telegradd', 'connect', 'sessions', 'session_store'])
    _telethon_session = None
    _conn = None

    @property
    def telethon_session(self):
        return self._telethon_session

    def set_telethon_session(self, value):  # set with phone number
        self._telethon_session = '\\'.join((self._telethon_base_path, f'{value}{self.EXTENSION}'))

    def _cursor(self, filename):  # cursor returned
        if self._conn is None:
            self._conn = sqlite3.connect (filename, check_same_thread=False)
        return self._conn.cursor ()

    def _execute(self, filename, executable_str, *values):  # select all w/without value, fetch something
        cur = self._cursor (filename)
        try:
            return cur.execute (executable_str, values).fetchone()
        finally:
            cur.close ()

    def close(self):
        # closes connection and set conn to none
        if self._conn is not None:
            self._conn.commit ()
            self._conn.close ()
            self._conn = None

    @abstractmethod
    def to_telethon_session(self):
        pass  # method to create telethon session in another path

    @property
    def done_session(self):
        return pathlib.Path(self.telethon_session).name.rstrip('.session')

    def clear_path(self):
        pass


