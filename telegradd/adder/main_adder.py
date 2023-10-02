import logging
import asyncio
import os
import typing

from telethon import events

from telegradd.connect.authorisation.client import TELEGRADD_client
from telegradd.connect.authorisation.databased import Database
from telegradd.adder.adder import ADDER, auth_for_adding
from telegradd.utils import split_ac


async def join_groups(clients: typing.List, group_link: str):
    join_group = [ADDER (cl).join_group (group_link) for cl in clients]
    res = await asyncio.gather (*join_group)
    while False in res:
        if None in res:
            break
        group_link = input ('Enter group link without @, like "group_link" or "https://t.me/group_link": ')
        join_group = [ADDER (cl).join_group (group_link) for cl in clients]
        res = await asyncio.gather (*join_group)
    return group_link

def already_skimmed():
    skimmed = input ('Users already skimmed (y/n): ').lower ()
    while skimmed not in ['y', 'n']:
        skimmed = input ('Users already skimmed (y/n): ').lower ()
    skim = True if skimmed == 'y' else False
    return skim


async def main_adder(how_to_add='username'):
    if how_to_add == 'id':
        print ("WARNING: U can't add via ID a user or interact with a chat through id, that your current session hasn’t met yet."
               "That's why more errors may occur and additional actions would be required!!")
    clients = await auth_for_adding()
    # join group to add users
    if clients:
        group_link = input('Enter group link: ')
        await join_groups(clients, group_link)  # join group
    else:
        return

    # choose how to add users to group and add users to group
    client_num = len(clients)
    user_num = hows_to_add()
    # split csv
    try:
        split_ac(client_num, int(user_num))
    except TypeError:
        print('it seems there are not enough users in users.csv file. Try add more users in it or reduce the number '
              'of accounts or users via ac')
        return

    # adding to group
    add_user_objects = [ADDER(cl) for cl in clients]
    if how_to_add == 'id':
        how_to_act = get_by_id()
        if how_to_act == 'y':
            if not already_skimmed():
                show_groups = [obj.meet_all_groups () for obj in add_user_objects[1:]]
                show_groups.append (add_user_objects[0].meet_all_groups (show_dict=True))
                res = await asyncio.gather (*show_groups)
                group_id = choose_dialog(res[-1])
                await asyncio.gather(*[cl.meet_users(group_id) for cl in add_user_objects])

            num = 0
            client_list = []

            for client in clients:
                client_list.append (ADDER (client).add_via_id(f'users{num}.csv', group_link))
                num += 1

            # run loop per 5 accounts
            if len (client_list) > 5:
                for client in get_batch_acc (batch_size=5, clients=client_list):
                    await asyncio.gather (*client, return_exceptions=True)
            else:
                await asyncio.gather (*client_list, return_exceptions=True)

        else:
            group_lin = await join_groups(clients, how_to_act)  # join group from which users were parsed, link returned
            await asyncio.gather (*[cl.meet_users (group_lin) for cl in add_user_objects])
            num = 0
            client_list = []
            for client in clients:
                client_list.append (ADDER (client).add_via_id (f'users{num}.csv', group_link))
                num += 1

            if len (client_list) > 5:
                for client in get_batch_acc (batch_size=5, clients=client_list):
                    await asyncio.gather (*client, return_exceptions=True)
            else:
                await asyncio.gather (*client_list, return_exceptions=True)

    elif how_to_add == 'username':
        num = 0
        client_list = []
        for client in clients:
            client_list.append(ADDER(client).add_via_username(f'users{num}.csv', group_link))
            num += 1
        #  with loop will add thread
        if len(client_list) > 5:
            for client in get_batch_acc(batch_size=5, clients=client_list):
                await asyncio.gather (*client, return_exceptions=True)
                #tasks = [asyncio.to_thread(*client)]
                #res = await asyncio.gather(*client)
                #res = await asyncio.gather (*client, return_exceptions=True)
        else:
            await asyncio.gather (*client_list, return_exceptions=True)

def get_batch_acc(batch_size: int, clients):
    batch = 0
    for _ in range (len (clients) // batch_size + 1):
        if not clients[batch:batch + batch_size]:
            break
        yield clients[batch:batch + batch_size]
        batch += batch_size


def choose_dialog(dialog_dict: typing.Dict) -> int:
    for k, v in dialog_dict.items ():
        print (k, v[1])
    ch_num = input('Choose num of the group from which users were parsed: ')
    while not ch_num.isdigit():
        ch_num = input ('Choose number of the group from which users were parsed (digit): ')
    return dialog_dict[int(ch_num)][0]


def get_by_id() -> str:
    is_joined = input("Are all the accounts from which the adding will take place joined the group from where "
                      "the users were parsed (y/n)?\n - ").lower()
    while not ((is_joined == 'y') or (is_joined == 'n')):
        is_joined = input ("Are all the accounts from which the adding will take place joined the group from where "
                           "the users were parsed (y/n)?\n - ").lower()

    if is_joined == 'n':
        group_link = input ('Enter group link from which users were parsed without @, like "group_link" or '
                            '"https://t.me/group_link": ')
        return group_link
    else:
        return is_joined


def hows_to_add():
    users_num = input("How many users do u want to add via one account? Recommended: 60 or less\n - ")
    while not users_num.isdigit():
        users_num = input ("How many users do u want to add via one account? Recommended: 60 or less. Pls type the digit\n - ")

    return users_num


async def join_group():# -> TelegramClient|bool:
    mode = input ('Use admin mode (y/n)?: ')
    admin = True if mode == 'y' else False
    Database ().view_all (admin=True) if admin else Database ().view_all ()
    num = input('Choose accounts. Enter digits via spaces (all - to use all): ').lower().strip(' ').split(' ')
    group_link = input('Enter group link to join: ')
    if num[0] == 'all':
        clients = await TELEGRADD_client ().clients (restriction=False)
        await join_groups(clients, group_link)
    elif num[0].isdigit():
        clients = await TELEGRADD_client (tuple(int(i) for i in num)).clients (restriction=False)
        await join_groups (clients, group_link)
    else:
        print('U choose wrong options, try again')
        return

if __name__ == '__main__':
    asyncio.run(main_adder())





