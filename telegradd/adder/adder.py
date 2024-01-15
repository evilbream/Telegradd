import asyncio
import time

from telethon import TelegramClient

import asyncio
import random
import typing
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.types import InputChannel, InputUser
from telethon import errors
import datetime

from telegradd.connect.authorisation.client import TELEGRADD_client
from telegradd.connect.authorisation.databased import Database
from telegradd.utils import get_from_csv

class ADDER:
    def __init__(self, client: TelegramClient):
        self.client = client

    async def join_group(self, group_link: str) -> bool|None:
        if group_link.startswith('https://t.me/'):
            self.group_link = group_link
        else:
            self.group_link = 'https://t.me/' + group_link
        async with self.client:
            try:
                group = await self.client.get_entity (self.group_link)
                await self.client (JoinChannelRequest (group))
                name = await self.client.get_entity('me')
                print(f'{name.first_name} successfully joined {self.group_link}')
                return True
            except Exception as err:
                if err is ValueError:
                    print("group with this username doesn't seem to exist")
                    return False
                else:
                    print(f'Something went wrong {err}')
                    return None

    async def meet_all_groups(self, show_dict=False) -> typing.Dict:
        chat_dict = {}
        num = 1
        async with self.client:
            async for dialog in self.client.iter_dialogs():
                df = dialog.id
                if show_dict:
                    if dialog.is_group:
                        chat_dict[num] = (dialog.id, dialog.name)
                        num += 1
            return chat_dict

    async def meet_users(self, group_id):
        user_list = []
        n = 1
        async with self.client:
            print(f'Skim over users, pls wait...')
            async for user in self.client.iter_participants(group_id):
                user_list.append((user.id, user.access_hash, user.first_name))
                n += 1
                if str(n).endswith('00'):
                    print(f'skimmed through {n} users')

    async def add_via_id(self, filename: str, group_link: str):
        async with self.client:
            me = await self.client.get_entity('me')
            group = await self.client.get_entity (group_link)
            chat = InputChannel (group.id, group.access_hash)
            for user_info in get_from_csv (filename):
                try:
                    users = await self.client.get_entity (int(user_info[0]))
                    user = InputUser (user_id=users.id, access_hash=users.access_hash)
                except Exception as err:
                    print(err)
                    continue
                try:
                    me = await self.client.get_entity ('me')
                    await self.client (InviteToChannelRequest (chat, [user]))
                    print (f'added {user_info[1]} by {me.first_name}')
                    await asyncio.sleep (random.randint (10, 15))
                except errors.PeerFloodError:
                    handle_db_errors (me.phone, me.username, 'Flood error')
                    break
                except errors.UserPrivacyRestrictedError:
                    print (f"can't add {user_info[1]} due to the user privacy setting")
                    continue
                except errors.UserNotMutualContactError:
                    print('User probably was in this group early, but leave it')
                    continue
                except errors.UserChannelsTooMuchError:
                    print(f'{user_info[1]} is already in too many channels/supergroups.')
                    continue
                except errors.UserKickedError:
                    print(f'{user_info[1]} was kicked from this supergroup/channel')
                except errors.UserBannedInChannelError:
                    handle_db_errors (me.phone, me.username,
                                            'was banned from sending messages in supergroups/channels')
                    break
                except errors.UserBlockedError:
                    handle_db_errors(me.phone, me.username, 'User blocked')
                    break
                except errors.FloodWaitError:
                    print(f'Flood error, pls wait one more day on this account - {me.username}')
                    break
                except Exception as err:
                    print(f'Unhandled error pls send it to me - tg @malevolentkid {err}')
                    continue

    async def add_via_username(self, filename: str, group_link: str):
        if group_link.startswith('https://t.me/'):
            self.group_link = group_link
        else:
            self.group_link = 'https://t.me/' + group_link
        async with self.client:
            me = await self.client.get_entity ('me')
            group = await self.client.get_entity (self.group_link)
            chat = InputChannel (group.id, group.access_hash)
            for user_info in get_from_csv (filename):
                if user_info[2] != 'None':
                    user = await self.client.get_entity(user_info[2])
                else:
                    print(f"User with id {user_info[0]} doesn't have username")
                    continue
                user = InputUser (user_id=user.id, access_hash=user.access_hash)
                try:
                    me = await self.client.get_entity('me')
                    await self.client (InviteToChannelRequest (chat, [user]))
                    print (f'added {user_info[2]} by {me.first_name}')
                    await asyncio.sleep (random.randint (10, 15))
                except errors.PeerFloodError:
                    handle_db_errors(me.phone, me.username, 'Flood error')
                    break
                except errors.UserPrivacyRestrictedError:
                    print (f"Can't add {user_info[2]} due to the user privacy setting")
                    continue
                except errors.UserNotMutualContactError:
                    print (f'{user_info[2]}  is not a mutual contact')
                    continue
                except errors.UserChannelsTooMuchError:
                    print(f'{user_info[1]} is already in too many channels/supergroups.')
                    continue
                except errors.UserKickedError:
                    print(f'{user_info[2]} was kicked from this supergroup/channel')
                except errors.UserBannedInChannelError:
                    handle_db_errors(me.phone, me.username, 'was banned from sending messages in supergroups/channels')
                    break
                except errors.UserBlockedError:
                    handle_db_errors(me.phone, me.username, 'User blocked')
                    break
                except errors.FloodWaitError:
                    print(f'Flood error, pls wait one more day on this account - {me.username}')
                    break
                except Exception as err:
                    print(f'Unhandled error pls send it to me - tg @malevolentkid {err}')
                    continue


def handle_db_errors(phone: str, username: str, error: str): # adding restriction to db with time
    print (f'{username} {error}')
    try:
        Database().update_restriction (f'true:{datetime.datetime.now().strftime("%Y:%m:%d:%H")}', phone=phone)
    except Exception as err:
        try:
            time.sleep(random.uniform(0.8, 4))
            Database().update_restriction (f'true:{datetime.datetime.now().strftime("%Y:%m:%d:%H")}', phone=phone)
        except Exception as err:
            print (f'Have some problem with database {err}')


async def auth_for_adding():
    Database ().automatically_delete_restrictions ()
    Database ().view_all (admin=False)
    num = input ('Choose accounts. Enter digits via spaces (all - to use all): ').lower ().strip (' ').split (' ')
    if num[0] == 'all':
        skip_account = input ('Automatically skip an account with restriction (y/n)? ').lower ()
        if skip_account == 'y':
            clients = await TELEGRADD_client ().clients (restriction=True)
            return clients
        else:
            clients = await TELEGRADD_client ().clients (restriction=False)
            return clients
    elif num[0].isdigit ():
        clients = await TELEGRADD_client (tuple (int (i) for i in num)).clients (restriction=False)
        return clients
    else:
        print ('U choose wrong options, try again')
        return False








