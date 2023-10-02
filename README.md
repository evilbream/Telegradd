# Telegradd

Adder for Telegram with Proxy Support

# Features: 
- Multiple accounts support
- Login with phone + app id and hash, pyrogram, telethon sessions, Tdata, session + json files
- Asynchronous scraper and adder
- Add users by username or id
- Add accounts with 2fa
- Proxy support for each account specifically. Tested with http/https/socks5/socks4
- Random time sleep from 10 to 15 seconds
- Mtproxy support for new version - with ee secret or base 64 secret and for old version - with 16 bytes secret
- Multiple filters to scrape users 
- Scrape users from comments in channel
- Remove duplicates from the user file
- Automatically filter bot users, admins and group owners
- Device model, system and app version for each account
- Automatically skip an account, that reached limit for the day
- Free tool
- More features are coming

## Parser options:
- Scrape users from comments in the channel
- Scrape users from messages in the group
- Filters:
- You can choose more than one options (one option from square brackets)
  - 1 Filter by Status:
    - [1.1.] User Status - LAST_MONTH
    - [1.2.] User Status - LAST_WEEK
    - [1.3.] User Status - OFFLINE
    - [1.4.] User Status - ONLINE
    - [1.5.] User Status - RECENTLY
    - [1.6.] User Status - Was Online Later Than a Specific Date
  - 2 Fetch Only Recent Participants (Recommended)
  - 3 Filter Premium Users
  - 4 Filter Users With Phone 
  - 5 Only with Photo
  - 6 Use Black List
    - [6.1.] In Name
    - [6.2.] In Bio
    - [6.3.] In Name And Bio
  - 7 Only With Username
  - 8 Without Username
  - 9 Set User Limit 
  - 10 Specify Post/Message Limit

## Usage 
- Download repository
- Install requirements
- Run main.py in telegradd folder
- Add sessions to one of the folders (pyrogram, telethon, tdata, json) in the sessions folder or log in using your phone number and app id, app hash
- Now you can do whatever you want

## Proxy usage:
- Proxy format: proxy_type:addr:port:username:password 
  - f.e. 'HTTP:22.92.130.159:8000:JKGGD3:R6KD4t' 
- MTP:host_name:port:proxy_secret (for MTProto Proxies)
  - 'MTP:mtproxy.network:8880:secret' 
  - if the proxy has no secret enter 0 instead of a secret

## Contacts
You can text to me for any questions
* Telegram - [malevolentkid](https://t.me//malevolentkid)

