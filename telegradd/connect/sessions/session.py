import random
import sqlite3
from dataclasses import dataclass
from typing import List
import os
import pathlib
from telegradd.connect.sessions.base_session import Session
import json
# all authorised sessions stored in sessions store
# all usable sessions are stored in sessions.sessions when connected to sessions deleted from other places
# creates sessions file telethon
import shutil
import logging
from telegradd.connect.sessions.tdata_support import convert_tdata

@dataclass
class TGdata:
    _dc_id: int
    _auth_key: bytes
    _port = 443
    _server_address = None
    _takeout_id = 0
    _version = 7

    @property
    def takeout_id(self):
        return self._takeout_id

    @property
    def version(self):
        return self._version

    @property
    def dc_id(self):
        return self._dc_id

    @property
    def port(self):
        return self._port

    @property
    def auth_key(self):
        return self._auth_key

    @property
    def server_address(self):
        self._server_address = self.ip_address(self._dc_id)
        return self._server_address

    def ip_address(self, dc_id):
        SERVERS = {
                1: "149.154.175.53",
                2: "149.154.167.51",
                3: "149.154.175.100",
                4: "149.154.167.91",
                5: "91.108.56.130",
                121: "95.213.217.195"}
        _server_address = (SERVERS[dc_id])

        return _server_address

@dataclass()
class Pyrogram_session(Session):
    def __init__(self, pyrogram_name, session=None):
        self._pyrogram_name: str = pyrogram_name
        _session = session
        super().__init__()

    @property
    def pyrogram_session(self):
        self._pyrogram_session_name = ('\\').join((self.FULL_PATH, 'sessions', 'pyrogram_sessions', f'{self._pyrogram_name}{self.EXTENSION}'))#'C:\\Users\\Atrocity\\Desktop\\Telegradd\\sessions\\pyrogram_sessions\\my_account.sessions'
        return self._pyrogram_session_name

    def _create_table(self, tables: List):  # pass list of tables as arg to create  tables
        # get phone number for sessions name and set sessions name
        print(self.pyrogram_session)
        conn = sqlite3.connect(self.pyrogram_session)
        c = conn.cursor()
        try:
            self._phone = c.execute('SELECT phone_number FROM peers').fetchone()[0]

        finally:
            conn.close()
        self.set_telethon_session(self._phone)
        # create tables in telethon file
        conn = sqlite3.connect(self.telethon_session)
        cur = conn.cursor()
        for i in tables:
            cur.execute(i)
        conn.commit()
        conn.close()

    def from_pyrogram_sessions(self):
        self._create_table(TELETHON_TABLES)
        pyrogram_row = self._execute(self.pyrogram_session, 'SELECT * FROM sessions')
        self._session = TGdata(pyrogram_row[0], pyrogram_row[3])

    def to_telethon_session(self):  # return done sessions file obj
        self.from_pyrogram_sessions() # delete when added tdata
        if self._session is not None:
            conn = sqlite3.connect (self.telethon_session)
            cur = conn.cursor ()
            cur.execute("INSERT OR REPLACE INTO version VALUES (?)", (self._session.version,))
            cur.execute("INSERT OR REPLACE INTO sessions VALUES (?, ?, ?, ?, ?)", (self._session.dc_id,
                          self._session.server_address, self._session.port, self._session.auth_key,
                          self._session.takeout_id))
            conn.commit()
            conn.close()

    def delete_pyrogram_session(self):
        if os.path.exists(self.pyrogram_session):
            os.remove(self.pyrogram_session)




TELETHON_TABLES = ["""CREATE TABLE IF NOT EXISTS version 
                (version INTEGER PRIMARY KEY)""",

          """CREATE TABLE IF NOT EXISTS sessions (
                dc_id INTEGER PRIMARY KEY, 
                server_address TEXT, 
                port INTEGER, 
                auth_key BLOB,
                takeout_id INTEGER)""",

          """CREATE TABLE IF NOT EXISTS entities (
                id integer primary key,
                hash integer not null,
                username text,
                phone integer,
                name text,
                date integer
                )""",

          """CREATE TABLE IF NOT EXISTS sent_files (
                md5_digest blob,
                file_size integer,
                type integer,
                id integer,
                hash integer,
                primary key (md5_digest, file_size, type)) """,

          """CREATE TABLE IF NOT EXISTS update_state (
                id integer primary key,
                pts integer,
                qts integer,
                date integer,
                seq integer)"""]


class Telethon_session(Session): # moved sessions to session store
    def __init__(self, telethon_name):
        self._telethon_name: str = telethon_name
        super().__init__()

    def to_telethon_session(self):
        telethon_session = ('\\').join((self.FULL_PATH, 'sessions', 'telethon_sessions', f'{self._telethon_name}{self.EXTENSION}'))
        self.set_telethon_session(self._telethon_name)
        shutil.move(telethon_session, self.telethon_session)


class Json_sessions(Session):
    def __init__(self, session_name):
        self.session_name = session_name
        self.JS_EXTENSION = '.json'
        super().__init__()

    def to_telethon_session(self):
        session = ('\\').join ((self.FULL_PATH, 'sessions', 'sessions_json', f'{self.session_name}{self.EXTENSION}'))
        self.set_telethon_session (self.session_name)
        shutil.move (session, self.telethon_session)

    def js_dict(self) -> dict:
        js_file = ('\\').join ((self.FULL_PATH, 'sessions', 'sessions_json', f'{self.session_name}{self.JS_EXTENSION}'))
        with open (js_file) as f:
            line = json.loads(f.readlines ()[0].rstrip ('\n'))
        return line

    @property
    def done_session(self):
        js_dict = self.js_dict()
        return pathlib.Path(self.telethon_session).name.rstrip('.session'), js_dict['app_id'], js_dict['app_hash'], \
               f"{js_dict['device']}:{js_dict['sdk']}:{js_dict['app_version']}", js_dict['phone'], js_dict['twoFA']



class Tdata_session(Session):
    def __init__(self, session_name: str):
        super().__init__()
        self._session_name = session_name.lstrip('+')
        self._TDATA_path = pathlib.Path (__file__).parents[3].joinpath('sessions', 'TData', session_name, 'tdata')

        self.set_telethon_session(self._session_name)

    def _create_table(self, tables: List):  # pass list of tables as arg to create  tables
        conn = sqlite3.connect(self.telethon_session)
        cur = conn.cursor()
        for i in tables:
            cur.execute(i)
        conn.commit()
        conn.close()

    def from_tdata(self):
        self._create_table(TELETHON_TABLES)
        data = convert_tdata(self._TDATA_path)
        self._session = TGdata(data[0], data[1])
        return self._session

    def to_telethon_session(self):  # return done sessions file obj
        self.from_tdata()
        # delete when added tdata
        if self._session is not None:
            conn = sqlite3.connect (self.telethon_session)
            cur = conn.cursor ()
            cur.execute("INSERT OR REPLACE INTO version VALUES (?)", (self._session.version,))
            cur.execute("INSERT OR REPLACE INTO sessions VALUES (?, ?, ?, ?, ?)", (self._session.dc_id,
                          self._session.server_address, self._session.port, self._session.auth_key,
                          self._session.takeout_id))
            conn.commit()
            conn.close()

    @property
    def done_session(self):
        pas = [pas for pas in os.listdir(self._TDATA_path.parent) if str(pas).endswith('.txt')]
        if len(pas) == 1:
            with open (self._TDATA_path.parent.joinpath (str (pas[0])), 'r') as f:
                pas = f.read ()
            return self.telethon_session, pas
        return pathlib.Path(self.telethon_session).name.rstrip('.session')


class UNITED_SESSION:
    TELETHON = 'TELETHON'
    PYROGRAM = 'PYROGRAM'
    JS = 'JS'
    TDATA = 'TDATA'

    def __init__(self, session):
        self._session = session

    def session(self, name):
        if self._session == self.TELETHON:
            sess = Telethon_session(name)
            sess.to_telethon_session()
            return sess.done_session
        elif self._session == self.JS:
            sess = Json_sessions (name)
            sess.to_telethon_session ()
            return sess.done_session
        elif self._session == self.PYROGRAM:
            sess = Pyrogram_session (name)
            sess.to_telethon_session ()
            return sess.done_session
        elif self._session == self.TDATA:
            sess = Tdata_session (name)
            sess.to_telethon_session ()
            return sess.done_session





