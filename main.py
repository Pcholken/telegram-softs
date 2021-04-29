import asyncio
from random import shuffle
from os import walk, remove
from telethon import TelegramClient, functions
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest


def get_proxy():
    if proxyes:
        proxy = proxyes.pop(0)
        proxyes.append(proxy)
        return proxy


async def subscribe_public_channel(channel_link, count, delay):
    local_accounts = accounts
    shuffle(local_accounts)
    for account in range(count):
        account = local_accounts[account]
        phone = await account.get_me()
        try:
            await account(functions.account.UpdateStatusRequest(offline=False))  # Go to online
            await account(JoinChannelRequest(channel_link))
            print(f"{phone.phone} вступил в {channel_link}")
        except Exception as error:
            print(str(error))
        await asyncio.sleep(delay)


async def subscribe_private_channel(channel_link, count, delay):
    if "https://t.me/joinchat/" in channel_link:
        channel_link = channel_link.replace("https://t.me/joinchat/", "")
    elif "t.me/joinchat/" in channel_link:
        channel_link = channel_link.replace("t.me/joinchat/", "")

    local_accounts = accounts
    shuffle(local_accounts)
    for account in range(count):
        account = local_accounts[account]
        phone = await account.get_me()
        try:
            await account(functions.account.UpdateStatusRequest(offline=False))  # Go to online
            await account(ImportChatInviteRequest(channel_link))
            print(f"{phone.phone} вступил в {channel_link}")
        except Exception as error:
            print(str(error))
        await asyncio.sleep(delay)


async def leave_public_channel(channel_link, count, delay):
    for account in range(count):
        account = accounts[account]
        phone = await account.get_me()
        try:
            await account(functions.account.UpdateStatusRequest(offline=False))  # Go to online
            await account(LeaveChannelRequest(channel_link))
            print(f"{phone.phone} покинул {channel_link}")
        except Exception as error:
            print(str(error))
        await asyncio.sleep(delay)


async def leave_private_channel(channel_link, count, delay):
    if "https://t.me/joinchat/" in channel_link:
        channel_link = channel_link.replace("https://t.me/joinchat/", "")
    elif "t.me/joinchat/" in channel_link:
        channel_link = channel_link.replace("t.me/joinchat/", "")
    for account in range(count):
        account = accounts[account]
        phone = await account.get_me()
        try:
            await account(functions.account.UpdateStatusRequest(offline=False))  # Go to online
            try:
                chat = await account.get_entity(channel_link)
                chat_title = chat.title
            except:
                return
            async for dialog in account.iter_dialogs():
                if dialog.title == chat_title:
                    await dialog.delete()
                    print(f"{phone.phone} покинул {channel_link}")
        except Exception as error:
            print(str(error))
        await asyncio.sleep(delay)


async def leave_all_chanels(delay):
    with open("exceptions.txt") as file:
        exceptions = file.read().split('\n')
        if '\n' in exceptions:
            exceptions.remove('\n')

    for account in accounts:
        exceptions = []
        for exception in exceptions:
            chat = await account.get_entity(exception)
            exceptions.append(chat.title)

        async for dialog in account.iter_dialogs():
            await account(functions.account.UpdateStatusRequest(offline=False))  # Go to online
            if dialog not in exceptions:
                await dialog.delete()
            await asyncio.sleep(delay)
        await asyncio.sleep(delay)


async def view_post(chanel_name, last_post_id, count_posts, count_accounts, delay):
    for account in range(count_accounts):
        account = accounts[account]
        phone = await account.get_me()
        try:
            await account(functions.account.UpdateStatusRequest(offline=False))  # Go to online
            await account(functions.messages.GetMessagesViewsRequest(
                peer=chanel_name,
                id=[post_id for post_id in range(last_post_id, last_post_id - count_posts, -1)],
                increment=True))
            print(f"{phone.phone} посмторел посты в {chanel_name}")
        except Exception as error:
            print(str(error))
        await asyncio.sleep(delay)


async def click_on_button(chanel_name, post_id, position, count, delay):
    for account in range(count):
        account = accounts[account]
        phone = await account.get_me()
        try:
            await account(functions.account.UpdateStatusRequest(offline=False))  # Go to online
            message = await account.get_messages(chanel_name, ids=[int(post_id)])
            await message[0].click(position - 1)
            print(f"{phone.phone} нажал на кнопку в {chanel_name}")
        except Exception as error:
            print(str(error))
        await asyncio.sleep(delay)


async def main():
    for _, _, sessions in walk("base"):
        for session in sessions:
            if session.endswith("session"):
                try:
                    addr, port, user, pasw = get_proxy().split(":")

                    proxy = {'proxy_type': 'socks5', 'addr': addr, 'port': int(port), 'username': user,
                             'password': pasw, 'rdns': True}

                    client = TelegramClient(f"base/{session}", api_id, api_hash, proxy=proxy)
                except:
                    client = TelegramClient(f"base/{session}", api_id, api_hash)
                try:
                    await client.connect()
                    if not await client.get_me():
                        await client.disconnect()
                        remove(f"../base/{session}")
                    else:
                        print(f"{session} connected")
                        accounts.append(client)
                except:
                    await client.disconnect()
                    remove(f"../base/{session}")

    print(f"Найдено {len(accounts)} аккаунтов в базе.")
    while True:
        print("maked by @pcholken\n\n")
        print("[1] - подписаться на открытый канал")
        print("[2] - подписаться на приватный канал")
        print("[3] - отписаться от открытого канала")
        print("[4] - отписаться от приватного канала")
        print("[5] - отписаться от всех каналов")
        print("[6] - посмотреть посты")
        print("[7] - накрутить реакции")

        choice = input()
        if choice == "1":
            await subscribe_public_channel(input("Ссылка на канал "), int(input("Количество акков ")),
                                           int(input("Задержка в секундах ")))
        elif choice == "2":
            await subscribe_private_channel(input("Ссылка на канал "), int(input("Количество акков ")),
                                            int(input("Задержка в секундах ")))
        elif choice == "3":
            await leave_public_channel(input("Ссылка на канал "), int(input("Количество акков ")),
                                       int(input("Задержка в секундах ")))
        elif choice == "4":
            await leave_private_channel(input("Ссылка на канал "), int(input("Количество акков ")),
                                        int(input("Задержка в секундах ")))
        elif choice == "5":
            await leave_all_chanels(int(input("Задержка в секундах ")))

        elif choice == "6":
            await view_post(input("Айди канала "), int(input("Айди последнего поста ")),
                            int(input("Сколько постов просмотреть ")), int(input("Количество акков ")),
                            int(input("Задержка в секундах ")))
        elif choice == "7":
            await click_on_button(input("Айди канала "), input("Айди поста "), int(input("Номер кнопки ")),
                                  int(input("Количество акков ")),
                                  int(input("Задержка в секундах ")))
        else:
            break


if __name__ == '__main__':
    api_id = 2375451
    api_hash = 'a210050786a27c798ca59d63e0c58c08'
    accounts = []

    with open("proxy.txt") as file:
        proxyes = file.read().split("\n")
        if "" in proxyes:
            proxyes.remove("")

    asyncio.run(main())
