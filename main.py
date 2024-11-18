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
import base64
from colorama import Fore, Style  # Import colorama for colored output

# Base64 encoded banner string
encoded_banner = """
CgorPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Kwp8IOKWiOKWiOKWiOKWiOKWiOKWiOKVlyDilojilojilojilojilojilojilZcg4paI4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4pWXICAgIOKWiOKWiOKWiOKVlyAgIOKWiOKWiOKWiOKVlyDilojilojilojilojilojilZcg4paI4paI4pWXICAgICB8CnzilojilojilZTilZDilZDilZDilojilojilZfilojilojilZTilZDilZDilojilojilZfilZrilZDilZDilojilojilZTilZDilZDilZ3ilojilojilZEgICAg4paI4paI4paI4paI4pWXIOKWiOKWiOKWiOKWiOKVkeKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVkSAgICAgfAp84paI4paI4pWRICAg4paI4paI4pWR4paI4paI4paI4paI4paI4paI4pWU4pWdICAg4paI4paI4pWRICAg4paI4paI4pWRICAgIOKWiOKWiOKVlOKWiOKWiOKWiOKWiOKVlOKWiOKWiOKVkeKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVkeKWiOKWiOKVkSAgICAgfAp84paI4paI4pWRICAg4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4pWQ4pWdICAgIOKWiOKWiOKVkSAgIOKWiOKWiOKVkSAgICDilojilojilZHilZrilojilojilZTilZ3ilojilojilZHilojilojilZTilZDilZDilojilojilZHilojilojilZEgICAgIHwKfOKVmuKWiOKWiOKWiOKWiOKWiOKWiOKVlOKVneKWiOKWiOKVkSAgICAgICAg4paI4paI4pWRICAg4paI4paI4pWRICAgIOKWiOKWiOKVkSDilZrilZDilZ0g4paI4paI4pWR4paI4paI4pWRICDilojilojilZHilojilojilojilojilojilojilojilZd8Cnwg4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWdIOKVmuKVkOKVnSAgICAgICAg4pWa4pWQ4pWdICAg4pWa4pWQ4pWdICAgIOKVmuKVkOKVnSAgICAg4pWa4pWQ4pWd4pWa4pWQ4pWdICDilZrilZDilZ3ilZrilZDilZDilZDilZDilZDilZDilZ18Cnwg4paI4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKWiOKWiOKWiOKWiOKVlyAg4paI4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKVlyAgICDilojilojilZcgICAg4paI4paI4pWXICAg4paI4paI4pWX4paI4paI4paI4paI4paI4paI4paI4paI4pWXICB8CnzilojilojilZTilZDilZDilZDilZDilZ0g4paI4paI4pWU4pWQ4pWQ4paI4paI4pWX4paI4paI4pWU4pWQ4pWQ4pWQ4paI4paI4pWX4paI4paI4pWRICAgIOKWiOKWiOKVkSAgICDilZrilojilojilZcg4paI4paI4pWU4pWd4pWa4pWQ4pWQ4paI4paI4pWU4pWQ4pWQ4pWdICB8CnzilojilojilZEgIOKWiOKWiOKWiOKVl+KWiOKWiOKWiOKWiOKWiOKWiOKVlOKVneKWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKVkSDilojilZcg4paI4paI4pWRICAgICDilZrilojilojilojilojilZTilZ0gICAg4paI4paI4pWRICAgICB8CnzilojilojilZEgICDilojilojilZHilojilojilZTilZDilZDilojilojilZfilojilojilZEgICDilojilojilZHilojilojilZHilojilojilojilZfilojilojilZEgICAgICDilZrilojilojilZTilZ0gICAgIOKWiOKWiOKVkSAgICAgfAp84pWa4paI4paI4paI4paI4paI4paI4pWU4pWd4paI4paI4pWRICDilojilojilZHilZrilojilojilojilojilojilojilZTilZ3ilZrilojilojilojilZTilojilojilojilZTilZ0gICAgICAg4paI4paI4pWRICAgICAg4paI4paI4pWRICAgICB8Cnwg4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWdIOKVmuKVkOKVnSAg4pWa4pWQ4pWdIOKVmuKVkOKVkOKVkOKVkOKVkOKVnSAg4pWa4pWQ4pWQ4pWd4pWa4pWQ4pWQ4pWdICAgICAgICDilZrilZDilZ0gICAgICDilZrilZDilZ0gICAgIHwKKz09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSsKCg==
"""  # The base64-encoded string of your banner

def _banner():
    # Decode the base64 encoded banner
    try:
        decoded_banner = base64.b64decode(encoded_banner).decode('utf-8', 'ignore')
        print(Fore.WHITE + Style.BRIGHT + decoded_banner + Style.RESET_ALL)
    except Exception as e:
        logger.error(f"Error decoding banner: {e}")
    
    # Additional details to display
    print(Fore.YELLOW + f" CREATED BY : DR ABDUL MATIN KARIMI: ⨭ {Fore.GREEN}https://t.me/doctor_amk")
    print(Fore.WHITE + f" DOWNLOAD LATEST HACKS HERE ➤ {Fore.GREEN}https://t.me/optimalgrowYT")
    print(Fore.RED  + f" LEARN HACKING HERE ➤ {Fore.GREEN}https://www.youtube.com/@optimalgrowYT/videos")
    print(Fore.RED  + f" DOWNLOAD MORE HACKS ➤ {Fore.GREEN}https://github.com/OptimalGrowYT")
    print(Fore.YELLOW + f" PASTE YOUR [USER 🆔] INTO USER_ID.TXT FILE AND PRESS START ")
    print(Fore.GREEN + f"                   [𝍖𝍖𝍖 𝙶𝚁𝙰𝚂𝚂 𝙷𝙰𝙲𝙺 𝚅𝙸𝙿 𝍖𝍖𝍖]                   ")
    log_line()

def log_line():
    print(Fore.GREEN + "-☠-" * 20 + Style.RESET_ALL)

user_agent = UserAgent(os='windows', platforms='pc', browsers='chrome')
random_user_agent = user_agent.random

async def connect_to_wss(socks5_proxy, user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy))
    logger.info(f"Connecting with Device ID: {device_id}")
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": random_user_agent,
                "Origin": "chrome-extension://lkbnfiajjmbhnfledhphioinpickokdi"
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            urilist = ["wss://proxy.wynd.network:4444/", "wss://proxy.wynd.network:4650/", 
                       "wss://proxy2.wynd.network:4444/", "wss://proxy2.wynd.network:4650/", 
                       "wss://proxy3.wynd.network:4444/", "wss://proxy3.wynd.network:4650/"]
            uri = random.choice(urilist)
            server_hostname = "proxy.wynd.network"
            proxy = Proxy.from_url(socks5_proxy)
            async with proxy_connect(uri, proxy=proxy, ssl=ssl_context, server_hostname=server_hostname,
                                     extra_headers=custom_headers) as websocket:
                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        logger.debug(f"Sending PING: {send_message}")
                        await websocket.send(send_message)
                        await asyncio.sleep(5)

                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(f"Received message: {message}")
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
                                "version": "4.26.2",
                                "extension_id": "lkbnfiajjmbhnfledhphioinpickokdi"
                            }
                        }
                        logger.debug(f"Sending AUTH response: {auth_response}")
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(f"Sending PONG response: {pong_response}")
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(f"Error with proxy {socks5_proxy}: {e}")

async def main():
    _banner()  # Display banner before proceeding

    # Read user_id from the USER_ID.txt file
    try:
        with open('USER_ID.txt', 'r') as file:
            _user_id = file.read().strip()  # Remove any leading/trailing whitespace
        if not _user_id:
            logger.error("No user ID found in USER_ID.txt!")
            return
    except FileNotFoundError:
        logger.error("USER_ID.txt file not found!")
        return

    logger.info(f"Using user_id: {_user_id}")
    
    # Read proxies from proxy_list.txt
    with open('proxy_list.txt', 'r') as file:
        local_proxies = file.read().splitlines()

    # Create tasks for each proxy to connect to WSS
    tasks = [asyncio.ensure_future(connect_to_wss(proxy, _user_id)) for proxy in local_proxies]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # Start the asyncio loop
    asyncio.run(main())
