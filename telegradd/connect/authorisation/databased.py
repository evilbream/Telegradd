import pathlib
import datetime
from pathlib import Path
import sqlite3
import os

from dateutil.relativedelta import relativedelta

from telegradd.connect.authorisation.app_id_hash import Apps
from telegradd.connect.authorisation.system import WindowsDevice
from telegradd.connect.sessions.session import UNITED_SESSION


class Database:
    TABLE = """CREATE TABLE IF NOT EXISTS 
                Accounts (
                Number INTEGER PRIMARY KEY NOT NULL,
                Name TEXT, 
                Api_id INTEGER, 
                Api_hash TEXT, 
                System TEXT,
                Proxy TEXT,
                Phone TEXT, 
                Password TEXT,
                Restrictions TEXT
                )"""

    SYSTEM = 'System'
    PROXY = 'Proxy'
    PHONE = 'Phone'
    PASSWORD = 'Password'
    RESTRICTIONS = 'Restrictions'
    API_ID = 'Api_id'
    API_HASH = 'Api_hash'

    DELETE = 'delete'
    UPDATE = 'update'
    GET = 'get'

    FILENAME = Path (Path (pathlib.Path (__file__)).parent, 'accounts.db')

    def __init__(self):
        self._conn = None

    def add_accounts(self, name, api_id=None, api_hash=None, system=None, proxy='', phone='', password='', restrictions='False'):
        if system is None:
            system = WindowsDevice().device_list
        if api_id is None:
            api_id, api_hash = Apps().app_info
        if phone == '' and name.isdigit():
            phone = name
        self._execute (self.TABLE)
        res = self._execute('''SELECT * from Accounts WHERE Name == ?''', name)
        if res:
            print(f'Session with a name {name} already exist')
            return
        c = sqlite3.connect(self.FILENAME)
        cur = c.cursor()
        try:
            cur.execute ('''INSERT INTO Accounts (
                         Name, Api_id, Api_hash, 
                         System, Proxy, Phone, 
                         Password, Restrictions)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (name, api_id, api_hash,
                       system, proxy, phone, password, restrictions))
            print(f'Session {name}  successfully added')
        finally:
            c.commit()
            c.close()

    def get_by_num(self, num: int):
        self._execute (self.TABLE)
        get = self._execute("""SELECT * FROM Accounts
                                WHERE Number == ?""", num)
        if get:
            return get
        print(f'No account with a number {num}')

    def get_by_name(self, name: int):
        self._execute (self.TABLE)
        get = self._execute("""SELECT * FROM Accounts
                               WHERE Name == ?""", name)
        if get:
            return get
        print (f'No account with a name {name}')

    def update_phone(self, phone, num=None, name=None):
        if name is not None:
            self._updater_by_name(self.PHONE, phone, name)
        elif num is not None:
            self._updater_by_num(self.PHONE, phone, num)

    def update_password(self, password, num=None, name=None):
        if name is not None:
            self._updater_by_name(self.PASSWORD, password, name)
        elif num is not None:
            self._updater_by_num(self.PHONE, password, num)

    def update_proxy(self, proxy, num=None, name=None):
        if name is not None:
            self._updater_by_name(self.PROXY, proxy, name)
        elif num is not None:
            self._updater_by_num(self.PROXY, proxy, num)

    def update_hash(self, hash, num=None, name=None):
        if name is not None:
            self._updater_by_name(self.API_HASH, hash, name)
        elif num is not None:
            self._updater_by_num(self.API_HASH, hash, num)

    def update_id(self, ids, num=None, name=None):
        if name is not None:
            self._updater_by_name(self.API_ID, ids, name)
        elif num is not None:
            self._updater_by_num(self.API_ID, ids, num)


    def update_restriction(self, restriction, num=None, name=None, phone=None):
        if name is not None:
            self._updater_by_name(self.RESTRICTIONS, restriction, name)
        elif num is not None:
            self._updater_by_num(self.RESTRICTIONS, restriction, num)
        elif phone is not None:
            self._update_by_phone(self.RESTRICTIONS, restriction, phone)

    def automatically_delete_restrictions(self):
        for data in self.get_all(('all',)):
            if data[8] == 'False':
                continue
            else:
                try:
                    res = data[8].split (':')
                    pass_3_days = datetime.datetime (int (res[1]), int (res[2].lstrip ('0')), int (res[3].lstrip ('0')),
                                                     int (res[4].lstrip ('0')) if int(res[4]) != 00 else int(res[4])) \
                                  + relativedelta (days=3) < datetime.datetime.now ()
                    if pass_3_days:
                        self.update_restriction ('False', num=data[0])
                        print(f'Restriction updated for {data[1]}')
                except IndexError:
                    self.update_restriction ('False', num=data[0])

    def update_system(self, system, num=None, name=None):
        if name is not None:
            self._updater_by_name(self.SYSTEM, system, name)
        elif num is not None:
            self._updater_by_num(self.SYSTEM, system, num)

    def _updater_by_num(self, what_to_update, updated_data, num=0):
        res = self._execute ("""SELECT * FROM Accounts
                                WHERE Number == ?""", num)
        conn = sqlite3.connect (self.FILENAME, check_same_thread=False)
        cur = conn.cursor ()
        if res:
            cur.execute (f'''UPDATE Accounts
                                    SET {what_to_update} = ? 
                                    WHERE Number == ?''', (updated_data, num))
            print (f'{what_to_update} successfully updated')
        else:
            print ('There is no account with such a number')
        conn.commit ()
        conn.close ()

    def _update_by_phone(self, what_to_update, updated_data, phone=0):
        res = self._execute ("""SELECT * FROM Accounts
                                WHERE Phone == ?""", phone)
        conn = sqlite3.connect (self.FILENAME, check_same_thread=False)
        cur = conn.cursor ()
        if res:
            cur.execute (f'''UPDATE Accounts
                                    SET {what_to_update} = ? 
                                    WHERE Phone == ?''', (updated_data, phone))
            print (f'{what_to_update} successfully updated')
        else:
            print ('There is no account with such a phone')
        conn.commit ()
        conn.close ()

    def _updater_by_name(self, what_to_update, updated_data, name='None'):
        res = self._execute ("""SELECT * FROM Accounts
                        WHERE Name == ?""", name)
        conn = sqlite3.connect(self.FILENAME, check_same_thread=False)
        cur = conn.cursor()
        if res:
            cur.execute (f'''UPDATE Accounts
                            SET {what_to_update} = ? 
                            WHERE Name == ?''', (updated_data, name))
            print(f'{what_to_update} successfully updated')
        else:
            print ('There is no account with such a name')
        conn.commit ()
        conn.close ()

    def delete_account(self, name=None, num=None):

        if num is not None:
            res = self.get_by_num(num)
            if res:
                conn = sqlite3.connect(self.FILENAME, check_same_thread=False)
                cur = conn.cursor()
                try:
                    cur.execute (f'''DELETE FROM Accounts 
                                WHERE Number == ?''', (num,))
                    print('Successfully deleted')
                finally:
                    conn.commit()
                    conn.close()
            else:
                print(f'Cant delete. There is no account with the number: {num}')
        if name is not None:
            res = self.get_by_name (name)
            if res:
                conn = sqlite3.connect (self.FILENAME, check_same_thread=False)
                cur = conn.cursor ()
                try:
                    cur.execute (f'''DELETE FROM Accounts 
                                     WHERE Name == ?''', (name,))
                    print ('Successfully deleted')
                finally:
                    conn.commit ()
                    conn.close ()
            else:
                print (f'Cant delete. There is no account with the name: {name}')

    def view_all(self, admin=False):
        self._execute (self.TABLE)
        tables = self._execute("""SELECT * from Accounts""")
        #print(tables)
        if admin:
            print (f'{"NUM":<3} | {"Name":<15} | {"App Id":<9} | {"App Hash":<35} | {"System":<35} | {"Proxy":<40} | {"Phone":<12} | {"Password":<9} | {"Restrictions":<13}')
            for row in tables:
                print (f'{row[0]:<3} | {row[1]:>15} | {row[2]:>9} | {row[3]:>35} | {row[4]:>35} | {row[5]:>40} | {row[6]:>12} | {row[7]:>9} | {row[8]:>13}')
        else:
            print (f'{"NUM":<3} | {"Name":<15} | {"Proxy":<45} | {"Password":<9} | {"Restriction":<20}')
            for row in tables:
                print (f'{row[0]:<3} | {row[1]:>15} | {row[5]:>45} | {row[7]:>9} | {row[-1]:>20}')

    def get_all(self, num:tuple):
        self._execute (self.TABLE)
        if num[0] == 'all':
            tables = self._execute("""SELECT * from Accounts""")
        else:
            tables = [self._execute ("""SELECT * from Accounts WHERE Number == ?""", i) for i in num]
            tables = [i[0] for i in tables if i]
        if tables:
            return tables
        return False

    def _cursor(self):  # cursor returned
        if self._conn is None:
            self._conn = sqlite3.connect (self.FILENAME, check_same_thread=False)
        return self._conn.cursor ()

    def _execute(self, executable_str, *values):  # select all w/without value, fetch something
        cur = self._cursor ()
        try:
            return cur.execute (executable_str, values).fetchall()
        finally:
            cur.close ()

    def close(self):
        # closes connection and set conn to none
        if self._conn is not None:
            self._conn.commit ()
            self._conn.close ()
            self._conn = None



class Auth:
    TELETHON = 'TELETHON'
    tl_path = Path (pathlib.Path (__file__).parents[3], 'sessions', 'telethon_sessions')
    PYROGRAM = 'PYROGRAM'
    pr_path = Path (pathlib.Path (__file__).parents[3], 'sessions', 'pyrogram_sessions')
    JS = 'JS'
    js_path = Path (pathlib.Path (__file__).parents[3], 'sessions', 'sessions_json')
    TDATA = 'TDATA'
    tdata_path = Path (pathlib.Path (__file__).parents[3], 'sessions', 'TData')
    CUSTOM = 'CUSTOM'
    destination_path = Path (pathlib.Path (__file__).parents[1], 'sessions', 'session_store')

    def __init__(self, log_in: str, ):
        self.log_in = log_in
        self._proxy = None
        self._manual = False
        self._use_proxy = True

    @property
    def path(self):
        if self.log_in == self.TDATA:
            return self.tdata_path
        elif self.log_in == self.TELETHON:
            return self.tl_path
        elif self.log_in == self.PYROGRAM:
            return self.pr_path
        elif self.log_in == self.JS:
            return self.js_path


    """def get_proxy(self):
        if self.log_in == self.TDATA:
            self.request_proxy (self.tdata_path)
        elif self.log_in == self.TELETHON:
            self.request_proxy (self.tl_path)
        elif self.log_in == self.PYROGRAM:
            self.request_proxy (self.pr_path)
        elif self.log_in == self.JS:
            self.request_proxy (self.js_path)"""

    def request_proxy(self):
        use_proxy = input ('Do u want to use prox(y/ies) (y/n): ').lower ()
        while use_proxy not in ['y', 'n']:
            use_proxy = input ('Do u want to use prox(y/ies) (y/n): ').lower ()
        if use_proxy == 'n':
            self._use_proxy = False
            return

        how_to_set_proxy = input ('Do u want to set a proxy for each account manually (y/n): ').lower ()
        while how_to_set_proxy not in ['y', 'n']:
            how_to_set_proxy = input ('Do u want to set a proxy for each account manually (y/n): ').lower ()
        if how_to_set_proxy == 'y':
            self._manual = True
            return

        """files = os.listdir (file_path)
        proxy_request = input (f'U have {len (files)} accounts to authorise.\n'
                               f'How many accounts do u want to use per one proxy?\n'
                               f'"enter" - without proxy: ')
        while not proxy_request.isdigit ():
            if proxy_request == '':
                return
            proxy_request = input (
                f'U have {len (files)} to authorise.\nHow many accounts do u want to use per one proxy?\n'
                f'"enter" - without proxy: ')

        if int (proxy_request) > len (files):
            print (f'U have less then {proxy_request} accounts, cant do this')
            return
        else:
            per = len (files) / int (proxy_request)
            self._per = per
            if len (files) % int (proxy_request) == 0:
                self._proxy = input (f'Enter {int (per)} prox(y/ies) or press enter and ad them to proxy.txt: ')
            else:
                self._proxy = input (f'Enter {int (per) + 1} prox(y/ies) or press enter and ad them to proxy.txt: ')
"""
    def manual_adder(self):
        add_another = 'y'
        while add_another == 'y':
            try:
                api_id = int (input ('Enter api_id: '))
            except ValueError:
                print ('api_id must be integer')
                api_id = int (input ('Enter api_id: '))
            api_hash = input ('Enter api_hash: ')
            phone = input ('Enter phone number with country code: ').lstrip ('+')
            proxy = ''
            if self._use_proxy:
                proxy = input ("Enter proxy for this account, press enter if u want to use this account without proxy.\n"
                           "Proxy format: proxy_type:addr:port:username:password or MTP:host_name:port:proxy_secret (for "
                           "MTProto Proxies), f.e. 'HTTP:22.92.130.159:8000:JKGGD3:R6KD4t' or "
                           "'MTP:mtproxy.network:8880:secret' (if the proxy has no secret enter 0 instead of secret): ")
            password = input ('Enter password fo 2fa, press enter if u havent any')
            Database().add_accounts(name=phone, api_id=api_id, api_hash=api_hash, proxy=proxy, phone=phone, password=password)
            add_another = input ('Do u wanna add another account (y/n)').lower ()

    def session_manual_proxy(self):
        password = input (f'Enter password: ')
        for file in os.listdir (self.path):
            if (not str(file).endswith('.session')) and (self.log_in != self.TDATA):
                continue
            file = str (file).rstrip ('.session')
            done = UNITED_SESSION(self.log_in).session(file)
            proxy = input(f'Enter proxy for {file}: ')
            if self.log_in == self.JS:
                Database ().add_accounts (name=done[0], api_id=done[1], api_hash=done[2],
                                          system=done[3], phone=done[4], password=done[5], proxy=proxy)
            else:
                if file.isdigit ():
                    Database ().add_accounts (file, phone=file, password=password, proxy=proxy)
                else:
                    Database ().add_accounts (file, password=password, proxy=proxy)

    def divided_proxy(self):
        password = input (f'Enter password: ')
        proxy = input (f'Enter proxy for new sessions: ')
        for file in os.listdir (self.path):
            if (not str(file).endswith('.session')) and (self.log_in != self.TDATA):
                continue
            file = str (file).rstrip ('.session')
            done = UNITED_SESSION(self.log_in).session(file)
            if self.log_in == self.JS:
                Database ().add_accounts (name=done[0], api_id=done[1], api_hash=done[2],
                                          system=done[3], phone=done[4], password=done[5], proxy=proxy)
            else:
                if file.isdigit ():
                    Database ().add_accounts (file, phone=file, password=password, proxy=proxy)
                else:
                    Database ().add_accounts (file, password=password,  proxy=proxy)

    def session_without_proxy(self):
        password = input (f'Enter password: ')
        for file in os.listdir(self.path):
            if str(file).startswith('info.txt'):
                continue
            if (not str(file).endswith('.session')) and (self.log_in != self.TDATA):
                continue
            file = str(file).rstrip('.session')
            done = UNITED_SESSION(self.log_in).session(file)
            if self.log_in == self.JS:
                Database().add_accounts(name=done[0], api_id=done[1], api_hash=done[2],
                                        system=done[3], phone=done[4], password=done[5])
            else:
                if file.isdigit():
                    Database ().add_accounts (file, phone=file, password=password)
                else:
                    Database().add_accounts(file, password=password)

    def add_account(self):
        self.request_proxy()
        if self.log_in == self.CUSTOM:
            self.manual_adder()
        elif self._use_proxy is False:
            self.session_without_proxy()
        elif self._manual: #add proxy manually per session
            self.session_manual_proxy()
        elif self._manual is False:
            self.divided_proxy()



