import asyncio
import os
import pathlib
import shutil

import aiofiles
from telethon import TelegramClient

from telegradd.connect.authorisation.client import TELEGRADD_client
from telegradd.connect.authorisation.databased import Auth, Database


def add_account(option: int):
    load = 'CUSTOM'
    if option == 2:
        load = 'JS'
    elif option == 3:
        load = 'TDATA'
    elif option == 4:
        load = 'PYROGRAM'
    elif option == 5:
        load = 'TELETHON'

    try:
        Auth(load).add_account()
    except Exception as err:
        print(err)


def view_account():
    mode = input('Use admin mode (y/n)?: ')
    admin = True if mode == 'y' else False
    Database().view_all(admin=True) if admin else Database().view_all()


def delete_banned():
    path = pathlib.Path(pathlib.Path(__file__).parents[1], 'sessions', 'session_store')
    accounts = [account[1] for account in Database().get_all(('all', ))]
    sessions = [str(file).rstrip('.session') for file in os.listdir(path) if str(file).endswith('.session')]
    for file in sessions:
        if file not in accounts:
            shutil.move(pathlib.Path(path, f'{file}.session'), pathlib.Path(pathlib.Path(__file__).parents[1], 'sessions', 'banned', f'{file}.session'))


async def auth_for_test():# -> TelegramClient|bool:
    mode = input ('Use admin mode (y/n)?: ')
    admin = True if mode == 'y' else False
    Database ().view_all (admin=True) if admin else Database ().view_all ()
    num = input('Choose accounts. Enter digits via spaces (all - to use all): ').lower().strip(' ').split(' ')
    if num[0] == 'all':
        await TELEGRADD_client ().clients (restriction=False)
    elif num[0].isdigit():
        await TELEGRADD_client (tuple(int(i) for i in num)).clients (restriction=False)
    else:
        print('U choose wrong options, try again')
        return


def update_credentials(opt: int):
    Database ().view_all (admin=True)
    account = input('Choose an account: ')
    try:
        account = int(account)
    except:
        opt = 8
    if opt == 1:
        api_id = input('Enter new app_id: ')
        Database().update_id(api_id, account)
    elif opt == 2:
        app_hash = input('Enter new app_hash: ')
        Database().update_hash(app_hash, account)
    elif opt == 3:
        proxy = input('Enter new Proxy: ')
        Database().update_proxy(proxy, account)
    elif opt == 4:
        system = input('Enter new system. Format: device model:system:app version: ')
        Database().update_system(system, account)
    elif opt == 5:
        password = input('Enter new password: ')
        Database().update_password(password, account)
    elif opt == 6:
        restr = input('Enter new restriction')
        Database().update_restriction(restr, account)
    elif opt == 7:
        phone = input('Enter new phone: ')
        Database().update_phone(phone, account)
    elif opt == 8:
        print('Wrong option...')
        return

def delete_duplicates_csv():
    path_user = pathlib.Path(pathlib.Path(__file__).parents[2], 'users', 'users.csv')
    with open(path_user, encoding='UTF-8') as f:
        users = {line for line in f.readlines () if not line.startswith('user_id:first_name')}

    with open(path_user, 'w', encoding='UTF-8') as f:
        f.write('user_id:first_name:username:access_hash:phone:group\n')
        for user in users:
            f.write(user)

def delete_accounts():
    Database().view_all(admin=False)
    delete = input('Enter number of an account (all - delete all): ')
    if delete == 'all':
        acc = Database().get_all(('all',))
        for i in acc:
            Database().delete_account(num=i[0])
    else:
        if delete.isdigit():
            acc = Database().get_all((int(delete),))
            Database().delete_account(num=acc[0][0])
        else:
            print('Wrong input...')
            return



if __name__ == '__main__':
    delete_accounts()