from time import localtime
from telethon import TelegramClient

quarantine = 0  # 1 если нужно сделать таймаут для аккаунтов

api_id = 2375451
api_hash = 'a210050786a27c798ca59d63e0c58c08'

print("Для выхода нажмите enter\n")
while True:
    phone = input("Введите номер телефона -> ")
    if phone:
        client = TelegramClient(f'base/{phone}', api_id, api_hash)
        client.start(phone=phone)
    else:
        break
