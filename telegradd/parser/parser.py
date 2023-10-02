import asyncio
import os.path
from typing import Any
import logging
from telethon import TelegramClient
import pathlib
import aiofiles
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin, ChannelParticipantsRecent, \
    UserStatusOffline, \
    UserStatusLastWeek, UserStatusLastMonth, UserStatusOnline, UserStatusRecently

from telegradd.connect.authorisation.client import TELEGRADD_client
from telegradd.connect.authorisation.databased import Database
from telegradd.parser.filters import Filter


class PARSER:
    LAST_MONTH = UserStatusLastMonth
    LAST_WEEK = UserStatusLastWeek
    OFFLINE = UserStatusOffline
    ONLINE = UserStatusOnline
    RECENTLY = UserStatusRecently

    def __init__(self, client: TelegramClient, status: Any = False, username=False, black_list_name: bool = False,
                 black_list_bio: bool = False,
                 photo: bool = False, premium: bool = False, phone: bool = False, without_username=False):
        self.without_username = without_username
        self.phone = phone
        self.premium = premium
        self.photo = photo
        self.black_list_bio = black_list_bio
        self.black_list_name = black_list_name
        self.status = status
        self.client = client
        self.username = username
        self._filename = pathlib.Path (pathlib.Path (__file__).parents[1], 'users', 'users.csv')

    async def write_users(self, user, title):
        if not self._filename.exists ():
            async with aiofiles.open (self._filename, 'a', encoding='UTF-8') as f:
                await f.write (f'user_id:first_name:username:access_hash:phone:group')
                await f.write (f'\n{user.id}:{user.first_name}:{user.username}:{user.access_hash}:{user.phone}:{title}')
        else:
            async with aiofiles.open (self._filename, 'a', encoding='UTF-8') as f:
                await f.write (f'\n{user.id}:{user.first_name}:{user.username}:{user.access_hash}:{user.phone}:{title}')
                #await f.write (f'\n{user.id}:{user.first_name}:{user.username}:{user.access_hash}')

    async def get_dialogs(self) -> int:
        async with self.client:
            dialogs = {}
            n = 1
            async for dialog in self.client.iter_dialogs ():
                if dialog.is_group:
                    dialogs[n] = (dialog.name, dialog.id)
                    n += 1
                else:
                    pass

        for k, v in dialogs.items ():
            print (k, v[0])
        dialog_num = input ('Choose group to scrape users: ')
        while not dialog_num.isdigit ():
            dialog_num = input ('Choose group to scrape users (digit): ')
        return int (dialogs[int (dialog_num)][1])

    async def get_channels(self) -> int:
        async with self.client:
            dialogs = {}
            n = 1
            async for dialog in self.client.iter_dialogs ():
                if dialog.is_channel:
                    dialogs[n] = (dialog.name, dialog.id)
                    n += 1

        for k, v in dialogs.items ():
            print (k, v[0])
        dialog_num = input ('Choose channel to scrape users: ')
        while not dialog_num.isdigit ():
            dialog_num = input ('Choose channel to scrape users (digit): ')
        return int (dialogs[int (dialog_num)][1])

    def filter(self, user, participant=True, bio=None):
        us_filter = Filter (user)
        if (participant and isinstance (user.participant, ChannelParticipantCreator)) or (participant and
            isinstance (user.participant, ChannelParticipantAdmin) ):
                return False
        elif us_filter.standard_filter:
            return False
        elif self.status and (us_filter.status (self.status) is False):
            return False
        elif self.phone and us_filter.phone is False:
            return False
        elif self.photo and us_filter.photo is False:
            return False
        elif self.premium and us_filter.premium:  # dont include premium users
            return False
        elif self.black_list_bio:
            if us_filter.bio(bio):
                return False
        elif self.black_list_name and us_filter.name:
            return False
        elif self.username and (us_filter.username is False):
            return False
        elif self.without_username and (us_filter.without_username is False):
            return False
        return True

    async def participants_scraper(self, limit=None, status_filter=ChannelParticipantsRecent (), bio=False):
        try:
            group_id = await self.get_dialogs ()
        except KeyError:
            print ('Try again, this number wasnt in list')
            group_id = await self.get_dialogs ()

        async with self.client:
            title = await self.client.get_entity(group_id)
            async for user in self.client.iter_participants (group_id, limit=limit, filter=status_filter):
                try:
                    if bio:
                        full = await self.client (GetFullUserRequest (user))
                        bio = full.full_user.about
                        if self.filter (user, bio=bio):
                            await self.write_users(user, title.title)
                    else:
                        if self.filter (user):
                            await self.write_users(user, title.title)
                except Exception as err:
                    print(err)
                    continue
        print('Successfully parsed')

    async def from_message_scraper(self, limit=None, bio=False):
        try:
            group_id = await self.get_dialogs ()
        except KeyError:
            print ('Try again, this number wasnt in list')
            group_id = await self.get_dialogs ()

        async with self.client:
            replies = []
            lap = 0
            title = await self.client.get_entity (group_id)
            async for mes in self.client.iter_messages (group_id, limit=limit):
                lap += 1
                try:
                    if lap % 100 == 0:
                        print(f'Parsed from {lap}/{limit} messages') if limit is not None else print(f'Parsed from {lap} messages')
                    user = await self.client.get_entity(mes.from_id)
                    if user.id not in replies:
                        replies.append(user.id)
                    else:
                        continue
                    try:
                        if bio:
                            full = await self.client (GetFullUserRequest (user))
                            bio = full.full_user.about
                            if self.filter (user, bio=bio, participant=False):
                                await self.write_users (user, title.title)
                        else:
                            if self.filter (user, participant=False):
                                await self.write_users (user, title.title)
                    except Exception as err:
                        print (err)
                        continue
                except Exception as err:
                    print (err)
                    continue
        print('Successfully parsed')
    async def from_comments(self, limit=None, bio=False):
        try:
            group_id = await self.get_channels ()
        except KeyError:
            print ('Try again, this number wasnt in list')
            group_id = await self.get_channels ()

        post = 0
        async with self.client:
            title = await self.client.get_entity(group_id)
            async for mes in self.client.iter_messages (group_id, limit=limit):
                post += 1
                replies = []
                print (f'Scraping from {post}/{limit} post(s)...') if limit is not None else print (f'Scraping from {post} post(s)...')

                if (mes.replies is not None) and (mes.replies.comments):
                    async for reply in self.client.iter_messages (group_id, reply_to=mes.id):
                        try:
                            user = await self.client.get_entity (reply.from_id)
                            if user.id not in replies:
                                replies.append (user.id)
                            else:
                                continue
                            try:
                                if bio:
                                    full = await self.client (GetFullUserRequest (user))
                                    bio = full.full_user.about
                                    if self.filter (user, participant=False):
                                        await self.write_users (user, title.title)
                                else:
                                    if self.filter (user, participant=False):
                                        await self.write_users (user, title.title)
                            except Exception as err:
                                    print (err)
                                    continue
                        except Exception as err:
                                print (err)
                                continue
        print('Successfully parsed')


async def auth_for_parsing() -> TelegramClient|bool:
    mode = input ('Use admin mode (y/n)?: ')
    admin = True if mode == 'y' else False
    Database ().view_all (admin=True) if admin else Database ().view_all ()
    num = int(input('Enter the account number you want to use : '))
    clients = await TELEGRADD_client ((num,)).clients (restriction=False)
    if clients:
        return clients[0]
    return False


async def main():
    client = await auth_for_parsing ()
    if client:
        async with client:
            await PARSER (client, black_list_name=True, premium=True, without_username=True).participants_scraper()


if __name__ == '__main__':
    asyncio.run(main())
