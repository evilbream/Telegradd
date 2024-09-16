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
- Restriction feature
- Free tool
- More features are coming

## Parser options:
- Scrape users from comments in the channel
- Scrape users from the group
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
 
# Getting api_id and api_hash
* Go to http://my.telegram.org and log in.
* Click on API development tools and fill the required fields.
* copy "api_id" n "api_hash" after clicking create app
* **! Skip this step if u use authorization by __session__ files**

# Installation
- Install python at least version 3.10 [how to install](https://www.digitalocean.com/community/tutorials/install-python-windows-10)
- Download the archive directly and unzip it or u can install git and download archive using git clone [install git](https://github.com/git-guides/install-git) (https://github.com/git-guides/install-git)

## Usage via terminal 
- ```pip3 install requirements.txt```
- ```git clone https://github.com/evilbream/Telegradd.git```
- ```cd Telegradd``` Change directory to downloaded folder.
- ```black_list.txt``` - It'll open black_list.txt. If u want to filter users by first name, last name and bio run it and add words. Users with these word(s) in name and bio will be excluded
- ```python main.py```  -  Run script


## Usage via PyCharm
- Download and install PyCharm community edition [jetbrains.com](https://www.jetbrains.com/pycharm/download/?section=windows)
- Open downloaded folder Telegradd with PyCharm
- Add data to black_list.txt if you want to filter users by name and bio
- Run main.py

### Using session files for authorisation
- Add sessions to one of the folders (pyrogram, telethon, tdata, json) in the sessions folder or log in using your phone number and app id, app hash (option 1 in main.py)
- Run ```main.py``` - choose options 2-5
- If u latter want to add more accounts just add more sessions and again run ```main.py``` 
- Add tdata in the folder with the phone number and place it in TData

### Restriction feature
- When adding users to a group and one of the following errors occurs - PeerFloodError, UserBannedInChannelError, a note will be added to the account with current date n time
- After 3 days note will be automatically deleted. 
- U can manually delete this note in main.py by clicking change restrictions
- When adding users to chats u can automatically skip an account if it has some restrictions


#### Some examples of supported  MTProxies
ip: 170.187.188.55 port: 443 secret: eec210ca2aa6d3d81670ed32899925445b626c6f672e636c6f7564666c6172652e636f6d
ip: 46.149.73.29 port: 443 secret: ee1603010200010001fc030386e24c3add646e2e79656b74616e65742e636f6d646c2e676f6f676c652e636f6d666172616b61762e636f6d160301020001000100000000000000000000000000000000 

I am not responsible for the work of the public proxies above, at the time of the release, the proxies were working

## Proxy usage:
- Proxy format: proxy_type:addr:port:username:password 
  - f.e. 'HTTP:22.92.130.159:8000:JKGGD3:R6KD4t' 
- MTP:host_name:port:proxy_secret (for MTProto Proxies)
  - 'MTP:mtproxy.network:8880:secret' 
  - if the proxy has no secret enter 0 instead of a secret
 
## json file example 
{"session_file":"123456789","phone":"123456789","register_time":1652446478,"app_id":1234,"app_hash":"b18441a1gg607e10a989891a5462e627","sdk":"4.3 Jelly Bean MR2 (18)","app_version":"4.8.1","device":"Windows","lang_pack":"an","system_lang_pack":"an","proxy":"[2, \"127.0.0.1\", 9158, true, null, null]","first_name":"Lindy","last_name":"f teee","username":"","ipv6":false,"twoFA":""}

## 2-fa
When loading sessions, you will be asked for a password, this is the password for 2-fa, if there is none, press enter
 
### Warning
Do not use with newly registered accounts

