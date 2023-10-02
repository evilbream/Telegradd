import collections
import re
from abc import ABC
from telethon import TelegramClient
from typing import Union, Any
from telethon.tl import types


class Parser (ABC):
    def __init__(self, client: TelegramClient, status: Union[str, bool, Any] = False, PHOTO: bool = False, Black_list: bool = False,
                 Emoji: bool = False, hidden: bool = False, comments: bool = False, premium: bool = False, phone: bool = False,
                 limit: Union[int, bool] = False, post_limit: Union[int, bool] = False):
        self.phone = phone
        self.client = client
        self.post_limit = post_limit
        self.limit = limit
        self.premium = premium
        self.comments = comments
        self.hidden = hidden
        self.Emoji = Emoji
        self.Black_list = Black_list
        self._status = status
        self.PHOTO = PHOTO
        self.User_obj = collections.namedtuple('Users', ['username', 'user_id', 'first_name', 'phone', 'group'])

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: Union[str]):
        if status not in ['LAST_MONTH', 'LAST_WEEK', 'OFFLINE', 'ONLINE', 'DATE']:
            raise Exception('Unsupported status type')
        elif status == 'LAST_MONTH':
            self._status = types.UserStatusLastMonth
        elif status == 'LAST_WEEK':
            self._status = types.UserStatusLastWeek
        elif status == 'OFFLINE':
            self._status = types.UserStatusOffline
        elif status == 'ONLINE':
            self._status = types.UserStatusOnline
        elif status == 'DATE':
            date = input ('Enter the date and time in 24 hours format. F.e: 2023:08:19:12:20 ')
            pattern = re.compile (r'\d\d\d\d:\d\d:\d\d:\d\d:\d\d')
            res = pattern.match (date)
            while res is None:
                print('Unsupported date format try again')
                date = input('Enter the date and time in 24 hours format. F.e: 2023:08:19:12:20 ')
                res = pattern.match (date)

            self._status = (i.lstrip('0') for i in date.split(':'))


    async def get_dialogs(self) -> int:
        async with self.client:
            dialogs = {}
            n = 1
            async for dialog in self.client.iter_dialogs():
                if dialog.is_group:
                    dialogs[n] = (dialog.name, dialog.id)
                    n += 1
                else:
                    pass

        for k, v in dialogs.items ():
            print (k, v[0])
        dialog_num = input ('Choose group from which parsing will be done: ')
        while not dialog_num.isdigit ():
            dialog_num = input ('Choose group from which parsing will be done (digit): ')
        return int(dialogs[int (dialog_num)][1]) # returned dialog id

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
        dialog_num = input ('Choose channel from which parsing will be done: ')
        while not dialog_num.isdigit ():
            dialog_num = input ('Choose channel from which parsing will be done (digit): ')
        return int (dialogs[int (dialog_num)][1]) # returned dialog id





