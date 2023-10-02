import pathlib
import re
from typing import Union, Any
from telethon.tl import types


class Filter:
    def __init__(self, user: types.User, black_list_name: bool = False, black_list_bio: bool = False,
                 photo: bool = True, premium: bool = False, phone: bool = False, username: bool = True, without_username=False):
        self._without_username = without_username
        self._username = username
        self._phone = phone
        self._user = user
        self._premium = premium
        self._photo = photo
        self._black_list_bio = black_list_bio
        self._black_list_name = black_list_name
        self._status = False
        self._standard_filter = False
        self.black_list_path = pathlib.Path(pathlib.Path(pathlib.Path(__file__).parents[2]), 'black_list.txt')

    @property
    def without_username(self):
        if self.username is False:
            self._without_username = True
            return self._without_username
        return self._without_username

    @property
    def username(self):
        self.set_username ()
        return self._username

    def set_username(self):
        if self._user.username is None:
            self._username = False

    @property
    def phone(self):
        self.set_phone()
        return self._phone

    def set_phone(self):
        if self._user.phone is not None:
            self._phone = True

    def status(self, status):
        self.status_setter(status)
        return self._status

    def status_setter(self, status: Union[Any, bool]):
        if isinstance (status, tuple):
            try:
                if (self._user.status.was_online.year >= int (status[0])) and (
                        self._user.status.was_online.month >= int (status[1])) and (
                        self._user.status.was_online.day >= int (status[2])) and (
                        self._user.status.was_online.hour >= int (status[3])) and (
                        self._user.status.was_online.minute >= int (status[4])):
                    self._status = True
            except AttributeError:
                self._status = False
        elif isinstance (self._user.status, status):
            self._status = True

    @property
    def standard_filter(self):
        self.standard_checker()
        return self._standard_filter

    @property
    def premium(self):
        self.premium_checker()
        return self._premium

    @property
    def photo(self):
        self.photo_checker()
        return self._photo

    def bio(self, bio):
        self.bio_setter(bio)
        return self._black_list_bio

    @property
    def name(self):
        self.black_list_checker_name()
        return self._black_list_name

    def standard_checker(self):
        if self._user.bot:
            self._standard_filter = True

    def premium_checker(self):
        if self._user.premium:
            self._premium = True

    def photo_checker(self):
        if self._user.photo is None:
            self._photo = False


    def get_black_list(self):
        with open (self.black_list_path, 'r', encoding='UTF-8') as f:
            lines = [line.rstrip ('\n').lower () for line in f.readlines ()]
        return lines

    def bio_setter(self, bio):
        print(bio)
        if bio is None:
            return
        else:
            black = self.get_black_list()
            for word in black:
                if word in bio:
                    WORD_RE = re.compile (fr'.*{word}.*')
                    res = WORD_RE.match (bio.lower ())
                    if res is not None:
                        self._black_list_bio = True
                        break


    def black_list_checker_name(self):
        first_name = self._user.first_name
        last_name = self._user.last_name
        if (first_name is None) and (last_name is None):
            return

        # check in first name
        black = self.get_black_list ()
        if last_name is None:
            for word in black:
                WORD_RE = re.compile (fr'.*{word}.*')
                res = WORD_RE.match (first_name.lower())
                if res is not None:
                    self._black_list_name = True
                    break
        # check in last name
        elif first_name is None:
            for word in black:
                WORD_RE = re.compile (fr'.*{word}.*')
                res = WORD_RE.match (last_name.lower ())
                if res is not None:
                    self._black_list_name = True
                    break
        else:
        # check in both
            for word in black:
                WORD_RE = re.compile (fr'.*{word}.*')
                res = WORD_RE.match (first_name.lower ())
                if res is not None:
                    self._black_list_name = True
                    break
                res = WORD_RE.match (last_name.lower ())
                if res is not None:
                    self._black_list_name = True
                    break



                #if (word in last_name.lower()) or (word in first_name.lower()):
                    #self._black_list_name = True

print(pathlib.Path(pathlib.Path(__file__).parents[2]))