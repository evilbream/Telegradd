from telethon import TelegramClient
import asyncio
import logging
logging.basicConfig(level=logging.INFO)
app_id = 14044787
app_hash = '47dc1bc15685111a8c993d2c11c3222a'
name = '5511935007763'
proxy = {
    'proxy_type': 'http', # (mandatory) protocol to use (see above)
    'addr': '193.28.177.41',      # (mandatory) proxy IP address
    'port': 50812,           # (mandatory) proxy port number
    'username': 'FuIDgWEn52x',      # (optional) username if the proxy requires auth
    'password': 'FuIDgWEn52x',      # (optional) password if the proxy requires auth
    'rdns': True            # (optional) whether to use remote or local resolve, default remote
}
async def main():
    async with TelegramClient('5511983365311', 11194047, "8e827f38b128f76f917d265feadd4ae6", device_model='B560 MB',
                              system_version='Windows 8.1', app_version='4.8.7 x64', proxy=proxy) as client:
        me = await client.get_me()
        print(me)



asyncio.run(main())