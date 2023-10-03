import asyncio
import os
import pathlib
import random

from telegradd.adder.main_adder import main_adder, join_group
from telegradd.connect.authorisation.main_auth import add_account, view_account, delete_banned, auth_for_test, \
    update_credentials, delete_duplicates_csv, delete_accounts
from telegradd.parser.main_parser import parser_page


banners = [
    """
        ████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██████╗           
        ╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗          
           ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██║  ██║██║  ██║          
           ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║  ██║██║  ██║          
           ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝          
           ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝           
                                                                     By EvilBream
                                                          Telegram @malevolentkid
    """,
    """"
  88888888888 8888888888 888      8888888888  .d8888b.  8888888b.         d8888 8888888b.  8888888b.  
      888     888        888      888        d88P  Y88b 888   Y88b       d88888 888  "Y88b 888  "Y88b 
      888     888        888      888        888    888 888    888      d88P888 888    888 888    888 
      888     8888888    888      8888888    888        888   d88P     d88P 888 888    888 888    888 
      888     888        888      888        888  88888 8888888P"     d88P  888 888    888 888    888 
      888     888        888      888        888    888 888 T88b     d88P   888 888    888 888    888 
      888     888        888      888        Y88b  d88P 888  T88b   d8888888888 888  .d88P 888  .d88P 
      888     8888888888 88888888 8888888888  "Y8888P88 888   T88b d88P     888 8888888P"  8888888P"                                                                                              
                                                                               Telegram @malevolentkid      
    """
]

update_option = "  UPDATE OPTIONS:\n" \
                " (1) Update AP_ID\n" \
                " (2) Update AP_HASH\n" \
                " (3) Update Proxy\n" \
                " (4) Update System\n" \
                " (5) Update Password\n" \
                " (6) Update Restricyion\n" \
                " (7) Update Phone\n"

def home_page():
    page_text = "\n\n" \
                f"{random.choice (banners)}\n" \
                " LOGIN OPTIONS:\n" \
                " (1) Login with Phone Number\n" \
                " (2) Load Sessions + json files\n" \
                " (3) Load Tdata\n" \
                " (4) Load Pyrogram Sessions\n" \
                " (5) Load Telethon Sessions\n\n" \
                " SCRAPER OPTIONS:\n" \
                " (6) Participants Group Scraper\n" \
                " (7) Hidden Participants Scarper\n" \
                " (8) Comments Participants Scarper\n\n" \
                " ADDER OPTIONS:\n" \
                " (9) Add by Id\n" \
                " (10) Add by Username\n\n"\
                " ADDITIONAL OPTIONS:\n" \
                " (11) Warm Up Mode\n" \
                " (12) Delete banned accounts\n" \
                " (13) List accounts\n" \
                " (14) Join Chat\n" \
                " (15) Change Proxy/Password/Etc\n" \
                " (16) Test Authorisation\n" \
                " (17) Delete Duplicates\n" \
                " (18) Delete Account(s)\n" \
                " (0)  Exit\n\n"
    print (page_text)
    usr_raw_input = input ("Choose an option (0-16) ~# ")
    try:
        option = int (usr_raw_input)
    except:
        option = 0
    if not (0 <= option <= 18):
        print ("You choose wrong option! try again ...")
        home_page()
    if 1 <= option <= 5:
        add_account(option)
    elif 6 <= option <= 8:
        parser_page(option)
    elif option == 9:
        asyncio.run(main_adder(how_to_add='id'))
    elif option == 10:
        asyncio.run(main_adder())
    elif option == 11:
        print('in progress')
    elif option == 12:
        delete_banned()
    elif option == 13:
        view_account()
    elif option == 14:
        asyncio.run(join_group())
    elif option == 15:
        print(update_option)
        raw_input = input ("Choose an option (1-7) ~# ")
        try:
            opt = int (raw_input)
            if not (1 <= opt <= 7):
                print ("You choose wrong option! try again ...")
                exit (0)
            update_credentials(opt)
        except:
            print ("Wrong option ...")
            exit (0)
        pass
    elif option == 16:
        asyncio.run(auth_for_test())
    elif option == 17:
        delete_duplicates_csv()
    elif option == 18:
        delete_accounts()
        delete_banned()
        print('All deleted accounts now stored in banned')
    elif option == 0:
        print ("Exiting ...")
        exit (0)


if __name__ == '__main__':
    try:
        home_page ()
    except KeyboardInterrupt:
        print ("\nExiting ...")
        exit (0)
