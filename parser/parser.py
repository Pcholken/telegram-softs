import sys
import asyncio
from telethon import TelegramClient

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.users import GetFullUserRequest

api_id = 2375451
api_hash = 'a210050786a27c798ca59d63e0c58c08'


async def parse():
    account = TelegramClient("parser.session", api_id, api_hash)
    await account.connect()

    url = input("Введите ссылку на канал или чат: ")
    channel = await account.get_entity(url)

    offset_user = 0
    limit_user = 1

    all_participants = []
    filter_user = ChannelParticipantsSearch('')
    while True:
        participants = await account(GetParticipantsRequest(channel, filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset_user += len(participants.users)
        print(f"Спаресено {len(all_participants)}")

    usernames = open("usernames.txt", "a", encoding="utf8")
    first_names = open("first_names.txt", "a", encoding="utf8")
    last_names = open("last_names.txt", "a", encoding="utf8")
    abouts = open("abouts.txt", "a", encoding="utf8")

    for i in range(len(all_participants)):
        try:
            full = await account(GetFullUserRequest(all_participants[i]))
            if full.user.username:
                usernames.write(f"{full.user.username}\n")
            if full.user.first_name:
                first_names.write(f"{full.user.first_name}\n")
            last_names.write(f"{full.user.last_name if full.user.last_name else ''}\n")
            if full.about:
                abouts.write(f"{full.about}\n")
            try:
                await account.download_media(full.profile_photo, "parsed_photos")
            except Exception as error:
                print(f"Ошибка при загрузке фото: {error}")
            print(f"Записаны данные с {i + 1} аккаунта")
        except Exception as error:
            print(error)

if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(parse()))
