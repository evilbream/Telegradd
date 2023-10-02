import asyncio
import pathlib
import random
from dataclasses import dataclass
from typing import Optional, List

import telethon
from telethon import TelegramClient, connection
import TelethonFakeTLS
from pathlib import Path
import shutil

from telegradd.connect.authorisation.databased import Database


class Client:
    EXTENSION = '.session'

    def __init__(self, session_name: str, api_id: int, api_hash: str, device_model: str, system_version: str,
                 app_version: str, phone=None, proxy: str = '', password=None):
        self._session_name = session_name
        self._api_id = api_id
        self._api_hash = api_hash
        self._device_model = device_model
        self._system_version = system_version
        self._app_version = app_version
        self._phone = phone
        self._proxy = proxy
        self._password = password
        if self._phone == '':
            self._phone = '393475899782'

    @property
    def session_name(self):
        name = Path (pathlib.Path (__file__).parents[1], 'sessions', 'session_store',
                                   f'{self._session_name}{self.EXTENSION}')
        return str (name)

    @property
    def proxy(self) -> tuple | dict | str:
        return self._proxy

    def proxy_setter(self, str_proxy):
        proxy_list = str_proxy.split (':')
        print(proxy_list)
        # proxy without login, pass
        if len (proxy_list) == 3:
            proxy = {
                'proxy_type': proxy_list[0],  # (mandatory) protocol to use (see above)
                'addr': proxy_list[1],  # (mandatory) proxy IP address
                'port': int (proxy_list[2]),  # (mandatory) proxy port number
                'rdns': True  # (optional) whether to use remote or local resolve, default remote
            }
            self._proxy = proxy

        elif proxy_list[0] == 'MTP':
            # 16 base MTP proxy
            if proxy_list[3] == '0':
                proxy = (proxy_list[1], proxy_list[2], '00000000000000000000000000000000')
                self._proxy = proxy
            else:
                # 16 base MTP proxy
                if len (proxy_list[3]) == 32:
                    proxy = (proxy_list[1], int (proxy_list[2]), proxy_list[3])
                    self._proxy = proxy

                # proxy with ee secret
                elif proxy_list[3].startswith ('ee'):
                    proxy = (proxy_list[1], int (proxy_list[2]), proxy_list[3].lstrip ('ee'))
                    self._proxy = proxy
                elif proxy_list[3].startswith ('7'):
                    proxy = (proxy_list[1], int (proxy_list[2]), proxy_list[3].lstrip ('7'))
                    self._proxy = proxy

        # http/https socks4/5 proxy
        elif len (proxy_list) == 5:
            if proxy_list[0].lower () == 'https':
                proxy = {
                    'proxy_type': 'http',
                    'addr': proxy_list[1],
                    'port': int (proxy_list[2]),
                    'username': proxy_list[3],
                    'password': proxy_list[4],
                    'rdns': True}
            else:
                proxy = {
                    'proxy_type': proxy_list[0],
                    'addr': proxy_list[1],
                    'port': int (proxy_list[2]),
                    'username': proxy_list[3],
                    'password': proxy_list[4],
                    'rdns': True}

            self._proxy = proxy
        else:
            self._proxy = ''  # unsupported proxy format or no proxy

    async def client(self) -> TelegramClient:
        if self.proxy == '':
            return TelegramClient (self.session_name, self._api_id, self._api_hash, device_model=self._device_model,
                                   system_version=self._system_version, app_version=self._app_version)
        elif self.proxy[0] == 'mtp':
            self.proxy_setter (self._proxy)
            return TelegramClient (self.session_name, self._api_id, self._api_hash, device_model=self._device_model,
                                   system_version=self._system_version, app_version=self._app_version,
                                   connection=connection.ConnectionTcpMTProxyRandomizedIntermediate, proxy=self.proxy)
        elif self.proxy[0] == 'fakeTls':
            self.proxy_setter (self._proxy)
            return TelegramClient (self.session_name, self._api_id, self._api_hash, device_model=self._device_model,
                                   system_version=self._system_version, app_version=self._app_version, proxy=self.proxy,
                                   connection=TelethonFakeTLS.ConnectionTcpMTProxyFakeTLS)
        else:
            self.proxy_setter (self._proxy)
            print(self.proxy)
            return TelegramClient (self.session_name, self._api_id, self._api_hash, device_model=self._device_model, system_version=self._system_version, app_version=self._app_version,
                                   proxy=self.proxy)

    @property
    async def start(self) -> TelegramClient | None:
        client = await self.client ()
        if self.proxy == '':
            without_proxy = input (
                f'Do u want to start {Path (self.session_name).parts[-1]} without proxy (y/n): ').lower ()
            if without_proxy != 'y':
                print (f'Ok, Skipping {Path (self.session_name).parts[-1]}')
                return None

        print (f'Starting log in to {Path (self.session_name).parts[-1]}')
        try:
            await client.start (self._phone, password=self._password, max_attempts=2)
            if self.proxy != '':
                print (f'Succesfully log in to {Path (self.session_name).parts[-1]} with {self.proxy}')
            else:
                print (f'Succesfully log in to {Path (self.session_name).parts[-1]} without proxy')
            return client
        except telethon.errors.PhoneNumberBannedError:
            print ('This account was banned, deleting from db...')
            # delete from bd and move to banned accounts
            Database ().delete_account(name=self._session_name)
            return None
        except RuntimeError:
            ses = input('Cant log in with this credentials, delete session (y/n): ')
            if ses == 'y':
                Database ().delete_account (name=self._session_name)
        except Exception as err:
            print (f'Something went wrong, failed to connect to {self.session_name} cuz {err}')
            return None

TABLE = """CREATE TABLE IF NOT EXISTS 
                Accounts (
                Number INTEGER PRIMARY KEY NOT NULL, 0
                Name TEXT,  1
                Api_id INTEGER, 2
                Api_hash TEXT,  3
                System TEXT, 4
                Proxy TEXT, 5
                Phone TEXT,  6
                Password TEXT, 7
                Restrictions TEXT 8
                )"""


class TELEGRADD_client:
    def __init__(self, auth: tuple = ('all', )):
        self._auth = auth

    async def clients(self, restriction=False):
        Database().automatically_delete_restrictions()
        clients = []
        credentials = Database ().get_all (self._auth)
        if credentials and (restriction is False):
            clients = [await Client(data[1], int(data[2]), data[3], (data[4]).split(":")[0], (data[4]).split(":")[1],
                                   (data[4]).split(":")[2], phone=data[6], proxy=data[5], password=data[7]).start for data in credentials]
        elif credentials and restriction:
            clients = [await Client (data[1], int(data[2]), data[3], (data[4]).split(":")[0], (data[4]).split(":")[1],
                                   (data[4]).split(":")[2], phone=data[6], proxy=data[5], password=data[7]).start for data in credentials if data[8] == 'False']
        else:
            print('U havent any accounts with the given number(s)')
            return

        clients = [client for client in clients if client is not None]
        if clients:
            return clients
        else:
            print('None of ur accounts can be used')
            return False


async def main():
    clients = await TELEGRADD_client(('all',)).clients(restriction=False)
    if not clients:
        return
    for client in clients:
        async with client:
            me = await client.get_me()
            print(me)


if __name__ == '__main__':
    asyncio.run(main())
