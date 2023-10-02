import asyncio
import re

from telegradd.connect.authorisation.client import TELEGRADD_client
from telegradd.connect.authorisation.databased import Database
from telethon import TelegramClient

from telegradd.parser.parser import PARSER, auth_for_parsing

"""     " (6) Participants Group Scraper\n" \
                " (7) Hidden Participants Scarper\n" \
                " (8) Scrape Reacted in Chat Users\n" \
                " (9) Comments Participants Scarper\n\n" \""""


def parser_page(us_option: int = 6):
    possible_limit = 'Possible' if us_option == 6 else 'Not Possible'
    possible_reaction = 'Possible' if us_option == 9 else 'Not Possible'
    possible_comment = 'Possible' if (us_option == 8) or (us_option == 7) else 'Not Possible'
    page_text = "\n\n" \
                " PARSER OPTIONS:\n" \
                " *1* Filter by Status:\n" \
                "       [1.1.] User Status - LAST_MONTH\n" \
                "       [1.2.] User Status - LAST_WEEK\n" \
                "       [1.3.] User Status - OFFLINE\n" \
                "       [1.4.] User Status - ONLINE\n" \
                "       [1.5.] User Status - RECENTLY\n" \
                "       [1.6.] User Status - Was Online Later Than a Specific Date\n" \
                " (2) Fetch Only Recent Participants (Recommended)\n" \
                " (3) Filter Premium Users\n" \
                " (4) Filter Users With Phone\n" \
                " (5) Only with Photo\n" \
                " *6* Use Black List\n" \
                "       [6.1.] In Name\n" \
                "       [6.2.] In Bio\n" \
                "       [6.3.] In Name And Bio\n" \
                " (7) Only With Username\n" \
                " (8) Without Username\n" \
                f" (9) Set User Limit ({possible_limit})\n" \
                f" (10) Specify Emojy ({possible_reaction})\n" \
                f" (11) Specify Post/Message Limit ({possible_comment})\n" \
                " [12] Parse Without Any Filter\n" \
                " (0)  Exit\n\n"
    print (page_text)
    usr_input = input ('Choose an option(s) (0-16). Enter digits via spaces: ').lower ().strip (' ').split (' ')

    input_set = {*usr_input}
    user_set = {'1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '2', '3', '4', '5', '6.1', '6.2', '6.3',
                '7', '8', '9', '10', '11', '12', '0'}

    if not user_set.intersection (input_set):
        print ('You chose wrong options')
        return


    if '1.1' in usr_input:
        status = PARSER.LAST_MONTH
    elif '1.2' in usr_input:
        status = PARSER.LAST_WEEK
    elif '1.3' in usr_input:
        status = PARSER.OFFLINE
    elif '1.4' in usr_input:
        status = PARSER.ONLINE
    elif '1.5' in usr_input:
        status = PARSER.RECENTLY
    elif '1.6' in usr_input:
        date = input (
            'Enter the date and time in 24 h format. F.e: 2023:08:19:12:20 ')
        pattern = re.compile (r'\d\d\d\d:\d\d:\d\d:\d\d:\d\d')
        res = pattern.match (date)
        while res is None:
            print ('Unsupported date format try again')
            date = input (
                'Enter the date and time in 24 hours format no earlier than when the user should have been online. F.e: 2023:08:19:12:20 ')

        status = (i.lstrip ('0') for i in date.split (':'))
    else:
        status = False

    if '3' in usr_input:
        premium = True
    else:
        premium = False

    if '4' in usr_input:
        phone = True
    else:
        phone = False

    if '5' in usr_input:
        photo = True
    else:
        photo = False

    if '6.1' in usr_input:
        black_list_name = True
        black_list_bio = False
        bio = False
    elif '6.2' in usr_input:
        black_list_name = False
        black_list_bio = True
        bio = True
    elif '6.3' in usr_input:
        black_list_name = True
        black_list_bio = True
        bio = True
    else:
        black_list_name = False
        black_list_bio = False
        bio = False

    if '7' in usr_input:
        username = True
    else:
        username = False

    if '8' in usr_input:
        without_username = True
    else:
        without_username = False

    if '2' in usr_input:
        recent = True
    else:
        recent = False

    if ('9' in usr_input) or ('11' in usr_input):
        limit = input ('Enter limit: ')
        while not limit.isdigit ():
            limit = input ('Enter limit: ')
        limit = int(limit)
    else:
        limit = None

    if '12' in usr_input:
        pass

    if usr_input == 0:
        print ("Exiting ...")
        exit (0)

    asyncio.run (main (option=us_option, status=status, username=username, black_list_name=black_list_name,
                       black_list_bio=black_list_bio, photo=photo, premium=premium, phone=phone,
                       without_username=without_username, recent=recent, bio=bio))


async def main(option: int, status=False, username=False, black_list_name: bool = False, black_list_bio: bool = False,
               photo: bool = False, premium: bool = False, phone: bool = False, without_username=False, recent=False,
               limit=None, bio=False):
    client = await auth_for_parsing ()
    if client:
        async with client:
            if option == 6:
                if recent:
                    await PARSER (client, status=status, username=username, black_list_name=black_list_name,
                       black_list_bio=black_list_bio, photo=photo, premium=premium, phone=phone,
                       without_username=without_username).participants_scraper (limit=limit, bio=bio)
                else:
                    await PARSER (client, status=status, username=username, black_list_name=black_list_name,
                                  black_list_bio=black_list_bio, photo=photo, premium=premium, phone=phone,
                                  without_username=without_username).participants_scraper (limit=limit, bio=bio, status_filter=False)
            elif option == 8:
                await PARSER (client, status=status, username=username, black_list_name=black_list_name,
                              black_list_bio=black_list_bio, photo=photo, premium=premium, phone=phone,
                              without_username=without_username).from_comments (limit=limit, bio=bio)

            elif option == 7:
                await PARSER (client, status=status, username=username, black_list_name=black_list_name,
                              black_list_bio=black_list_bio, photo=photo, premium=premium, phone=phone,
                              without_username=without_username).from_message_scraper (limit=limit, bio=bio)

if __name__ == '__main__':
    parser_page(6)
