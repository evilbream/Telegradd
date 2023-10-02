from dataclasses import dataclass

@dataclass
class User:
    _username: str
    _user_id: int
    _first_name: str
    _phone: int
    _group: str

    @property
    def username(self):
        return self._username

    @property
    def user_id(self):
        return self._user_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def phone(self):
        return self._phone

    @property
    def group(self):
        return self._group






