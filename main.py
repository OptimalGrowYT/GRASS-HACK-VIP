import asyncio
import random
import ssl
import json
import time
import uuid
import requests
import shutil
from loguru import logger
from websockets_proxy import Proxy, proxy_connect
from fake_useragent import UserAgent
import websockets
from colorama import Fore, Style
import base64

# Banner code
def _banner():
    # Base64 encoded banner
    encoded_banner = r"""
    Pj49PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PDwKfHwg4paI4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKWiOKWiOKWiOKWiOKVlyDilojilojilojilojilojilojilojilojilZfilojilojilZfilojilojilojilZcgICDilojilojilojilZcg4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKVlyAgICAgICB8fAp8fOKWiOKWiOKVlOKVkOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KVmuKVkOKVkOKWiOKWiOKVlOKVkOKVkOKVneKWiOKWiOKVkeKWiOKWiOKWiOKWiOKVlyDilojilojilojilojilZHilojilojilZTilZDilZDilojilojilZfilojilojilZEgICAgICAgfHwKfHzilojilojilZEgICDilojilojilZHilojilojilojilojilojilojilZTilZ0gICDilojilojilZEgICDilojilojilZHilojilojilZTilojilojilojilojilZTilojilojilZHilojilojilojilojilojilojilojilZHilojilojilZEgICAgICAgfHwKfHzilojilojilZEgICDilojilojilZHilojilojilZTilZDilZDilZDilZ0gICAg4paI4paI4pWRICAg4paI4paI4pWR4paI4paI4pWR4pWa4paI4paI4pWU4pWd4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4paI4paI4pWR4paI4paI4pWRICAgICAgIHx8Cnx84pWa4paI4paI4paI4paI4paI4paI4pWU4pWd4paI4paI4pWRICAgICAgICDilojilojilZEgICDilojilojilZHilojilojilZEg4pWa4pWQ4pWdIOKWiOKWiOKVkeKWiOKWiOKVkSAg4paI4paI4pWR4paI4paI4paI4paI4paI4paI4paI4pWXICB8fAp8fCDilZrilZDilZDilZDilZDilZDilZ0g4pWa4pWQ4pWdICAgICAgICDilZrilZDilZ0gICDilZrilZDilZ3ilZrilZDilZ0gICAgIOKVmuKVkOKVneKVmuKVkOKVnSAg4pWa4pWQ4pWd4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWQ4pWdICB8fAp8fCAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB8fAp8fCDilojilojilojilojilojilojilZcg4paI4paI4paI4paI4paI4paI4pWXICDilojilojilojilojilojilojilZcg4paI4paI4pWXICAgIOKWiOKWiOKVlyAgICDilojilojilZcgICDilojilojilZfilojilojilojilojilojilojilojilojilZd8fAp8fOKWiOKWiOKVlOKVkOKVkOKVkOKVkOKVnSDilojilojilZTilZDilZDilojilojilZfilojilojilZTilZDilZDilZDilojilojilZfilojilojilZEgICAg4paI4paI4pWRICAgIOKVmuKWiOKWiOKVlyDilojilojilZTilZ3ilZrilZDilZDilojilojilZTilZDilZDilZ18fAp8fOKWiOKWiOKVkSAg4paI4paI4paI4pWX4paI4paI4paI4paI4paI4paI4pWU4pWd4paI4paI4pWRICAg4paI4paI4pWR4paI4paI4pWRIOKWiOKVlyDilojilojilZEgICAgIOKVmuKWiOKWiOKWiOKWiOKVlOKVnSAgICDilojilojilZEgICB8fAp8fOKWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKVkeKWiOKWiOKWiOKVl+KWiOKWiOKVkSAgICAgIOKVmuKWiOKWiOKVlOKVnSAgICAg4paI4paI4pWRICAgfHwKfHzilZrilojilojilojilojilojilojilZTilZ3ilojilojilZEgIOKWiOKWiOKVkeKVmuKWiOKWiOKWiOKWiOKWiOKWiOKVlOKVneKVmuKWiOKWiOKWiOKVlOKWiOKWiOKWiOKVlOKVnSAgICAgICDilojilojilZEgICAgICDilojilojilZEgICB8fAp8fCDilZrilZDilZDilZDilZDilZDilZ0g4pWa4pWQ4pWdICDilZrilZDilZ0g4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWdICDilZrilZDilZDilZ3ilZrilZDilZDilZ0gICAgICAgIOKVmuKVkOKVnSAgICAgIOKVmuKVkOKVnSAgIHx8Cj4+PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PTw8Cg==
    """ 
    
    # Decode the base64 encoded banner
    decoded_banner = base64.b64decode(encoded_banner).decode('utf-8')

    # Print the decoded banner
    print(Fore.GREEN + Style.BRIGHT + decoded_banner + Style.RESET_ALL)
    
    # Base64 encoded URLs and texts
    encoded_links = {
        "CONTACT_US": "aHR0cHM6Ly90Lm1lL2RvY3Rvcl9hbWw=",
        "DOWNLOAD_HACKS": "aHR0cHM6Ly90Lm1lL29wdGltYWxncm93WVQ=",
        "LEARN_HACKING": "aHR0cHM6Ly93d3cueW91dWJldC5jb20vQG9wdGltYWxncm93WVQvdmlkZW9z",
        "PARTNER_CHANNEL": "aHR0cHM6Ly90Lm1lL0FpcmRyb3BoYWNrMTIzOQ==",
        "PASTE_USER_ID": "UEFTVEUgeW91ciAoVVNFUiggX1VJREkpIElOVE8gVVNFUl9JRC5UWEQgRklMRSBhbmQgUFJFU1MgU1RBUg==",
        "GRASS_AIRDROP_HACK": "U+X4IGVuYoX5z0aRkZXoV8KGGlT-IEA==",
    }

    # Decode and print each URL link
    print(Fore.RED + f" CONTACT US: ⨭ {Fore.GREEN}{base64.b64decode(encoded_links['CONTACT_US']).decode('utf-8')}")
    print(Fore.WHITE + f" DOWNLOAD LATEST HACKS HERE ➤ {Fore.GREEN}{base64.b64decode(encoded_links['DOWNLOAD_HACKS']).decode('utf-8')}")
    print(Fore.RED  + f" LEARN HACKING HERE ➤ {Fore.GREEN}{base64.b64decode(encoded_links['LEARN_HACKING']).decode('utf-8')}")
    print(Fore.YELLOW + f" PARTNER CHANNEL  {Fore.GREEN}{base64.b64decode(encoded_links['PARTNER_CHANNEL']).decode('utf-8')}")
    print(Fore.YELLOW + f" PASTE YOUR (USER ID) INTO USER_ID.TXT FILE AND PRESS START ")
    print(Fore.GREEN + f" ▀▄▀▄▀▄ 🌿 𝗚𝗿𝗮𝘀𝘀 𝗔𝗶𝗿𝗱𝗿𝗼𝗽 𝗛𝗮𝗰𝗸 🌿 ▄▀▄▀▄▀ ")
    log_line()

def log_line():
    print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)

# Main script starts here
user_agent = UserAgent()
random_user_agent = user_agent.random

async def connect_to_wss(socks5_proxy, user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy))
    logger.info(device_id)
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": random_user_agent,
                "Origin": "chrome-extension://ilehaonighjijnmpnagapkhpcdbhclfg"
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            uri = "wss://proxy.wynd.network:4650"
            server_hostname = "proxy.wynd.network"
            proxy = Proxy.from_url(socks5_proxy)

            # Using websockets.connect
            async with websockets.connect(uri, ssl=ssl_context, extra_headers=custom_headers) as websocket:
                logger.info("Connected to websocket")

                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        logger.debug(send_message)
                        await websocket.send(send_message)
                        await asyncio.sleep(5)

                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(message)
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "4.0.3",
                                "extension_id": "ilehaonighjijnmpnagapkhpcdbhclfg"
                            }
                        }
                        logger.debug(auth_response)
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(pong_response)
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(e)
            logger.error(socks5_proxy)

async def main():
    # Display the banner on start
    _banner()

    # Read user_id from USER_ID.txt file
    try:
        with open('USER_ID.txt', 'r') as file:
            _user_id = file.read().strip()  # Read and remove any extra whitespace
        if not _user_id:
            logger.error("User ID is empty in USER_ID.txt!")
            return
    except FileNotFoundError:
        logger.error("USER_ID.txt file not found!")
        return
    
    logger.info(f"Using user_id: {_user_id}")
    
    # Read proxy list from proxy.txt
    with open('proxy.txt', 'r') as file:
        local_proxies = file.read().splitlines()
    
    tasks = [asyncio.ensure_future(connect_to_wss(i, _user_id)) for i in local_proxies]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
