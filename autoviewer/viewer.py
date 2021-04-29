import asyncio
from os import walk, remove
import telethon
from telethon import TelegramClient, functions


def get_proxy():
    if proxyes:
        proxy = proxyes.pop(0)
        proxyes.append(proxy)
        return proxy


async def wait_post(channel, view_delay):
    client = accounts[0]

    channel = await client.get_entity(channel)
    async for message in client.iter_messages(channel, limit=1):
        last_message_id = message.id

    while True:
        try:
            async for message in client.iter_messages(channel, limit=1):
                if message.id != last_message_id:
                    last_message_id = message.id
                    print(f"Новый пост {last_message_id}")
                    for account in accounts:
                        try:
                            await asyncio.sleep(view_delay)
                            peer = await account.get_entity(channel)
                            await account(functions.messages.GetMessagesViewsRequest(
                                peer=peer,
                                id=[last_message_id],
                                increment=True))
                        except:
                            accounts.remove(account)
                await asyncio.sleep(delay)
        except:
            del accounts[0]
            client = accounts[0]


async def main():
    for _, _, sessions in walk("../base"):
        for session in sessions:
            if session.endswith("session"):
                try:
                    addr, port, user, pasw = get_proxy().split(":")

                    proxy = {'proxy_type': 'socks5', 'addr': addr, 'port': int(port), 'username': user,
                             'password': pasw, 'rdns': True}

                    client = TelegramClient(f"../base/{session}", api_id, api_hash, proxy=proxy)
                except:
                    client = TelegramClient(f"../base/{session}", api_id, api_hash)
                try:
                    await client.connect()
                    if not await client.get_me():
                        await client.disconnect()
                        remove(f"../base/{session}")
                    else:
                        print(f"{session} connected")
                        accounts.append(client)
                except telethon.errors.rpcerrorlist.AuthKeyDuplicatedError:
                    await client.disconnect()
                    remove(f"../base/{session}")

    print(f"Найдено {len(accounts)} аккаунтов в базе.")

    view_delay = int(input("Задержка между просмотрами "))

    with open("channels_to_view.txt") as file:
        channels = file.read().split('\n')

        if '' in channels:
            channels.remove('')

    print(f"Найдено {len(channels)} для отслеживания.")

    tasks = []
    for channel in channels:
        tasks.append(asyncio.create_task(wait_post(channel, view_delay)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    delay = 1  # Задержка на проверку постов в секундах

    api_id = 2375451
    api_hash = 'a210050786a27c798ca59d63e0c58c08'
    accounts = []

    with open("../proxy.txt") as file:
        proxyes = file.read().split("\n")
        if "" in proxyes:
            proxyes.remove("")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(main()))
