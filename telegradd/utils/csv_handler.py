import csv
import pathlib
import typing

BASE_PATH = pathlib.Path(pathlib.Path(__file__).parents[1], 'users')


def get_from_csv(filename: str, line_num=1):
    with open(pathlib.Path(BASE_PATH, filename), 'r', newline='', encoding='utf-8') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if csvreader.line_num > line_num:
                try:
                    yield list(row)[0].split(':')[0], list(row)[0].split(':')[1], list(row)[0].split(':')[2], list(row)[0].split(':')[3]
                except IndexError:
                    continue

def yield_users(filename: pathlib.Path, start, stop):
    user_list = []
    with open(filename, 'r', encoding='UTF-8') as f:
        csvreader = csv.reader (f)
        for row in csvreader:
            if start < csvreader.line_num <= stop:
                try:
                    user_list.append((list (row)[0].split (':')[0], list (row)[0].split (':')[1], list (row)[0].split (':')[2], list (row)[0].split (':')[3]))
                except IndexError:
                    continue
            elif csvreader.line_num > stop:
                return user_list

def get_csv_len(filename: pathlib.Path):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        csvreader = csv.reader(f)
        i = 0
        for row in csvreader:
            i += 1
        return i - 1


def add_to_csv(filename: pathlib.Path, users: typing.List):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        write = csv.writer(f, delimiter=':')
        write.writerow(['user_id', 'first_name', 'username', 'access_hash'])
        for user in users:
            write.writerow([user[0], user[1], user[2], user[3]])



def split_ac(clients_num: int, users_via_ac: int):
    start = 1
    num = users_via_ac
    for i in range(clients_num):
        user_list = yield_users (pathlib.Path(BASE_PATH, 'users.csv'), start, users_via_ac + 1)
        add_to_csv(pathlib.Path(BASE_PATH, f'users{i}.csv'), user_list)
        start += num
        users_via_ac += num
    user_list = yield_users (pathlib.Path(BASE_PATH, 'users.csv'), users_via_ac, get_csv_len(pathlib.Path(BASE_PATH, 'users.csv')))
    add_to_csv (pathlib.Path(BASE_PATH, 'users.csv'), user_list)



