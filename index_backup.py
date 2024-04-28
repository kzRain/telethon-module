import random

from flask import Flask, jsonify, request
import asyncio
from telethon import TelegramClient
from telethon.tl.types import InputPhoneContact, ImportedContact
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon import functions, types
from telethon.tl.functions.contacts import AddContactRequest

# Remember to use your own values from my.telegram.org!
api_id = 17735788
api_hash = '285b5aee89a674d518dcc14f295c58f7'
client = TelegramClient('anon', api_id, api_hash)
loop = asyncio.get_event_loop()

app = Flask(__name__)

incomes = [
    { 'description': 'salary', 'amount': 5000 }
]


@app.route('/incomes')
async def get_incomes():
    await client.connect()
    await client.send_message('+77785080094', 'text')
    await client.disconnect()
    return jsonify(incomes)


@app.route('/send_message', methods=['POST'])
async def send_message():
    # Получаем данные из запроса
    data = request.get_json()

    # Проверяем наличие необходимых данных в запросе
    if 'phone_number' not in data or 'text' not in data:
        return 'Missing parameters', 400

    # Авторизуемся в Telegram
    await client.start()

    # Пытаемся отправить сообщение
    try:
        # Получаем объект сущности для контакта
        contact_entity = await client.get_entity(data['phone_number'])
    except ValueError:
        # Если контакт отсутствует, добавляем его
        try:
            contact = types.InputPhoneContact(
                client_id=0,
                phone=data.get('phone_number'),
                first_name='auto',
                last_name='user1'
            )
            result = await client(functions.contacts.ImportContactsRequest(
                contacts=[contact]
            ))
            print(result)
            # Повторно получаем объект сущности для контакта
            contact_entity = await client.get_entity(data['phone_number'])
        except Exception as e:
            return f"Error adding contact: {e}", 500

    # Отправляем сообщение
    try:
        await client.send_message(contact_entity, data['text'])
        return 'Message sent successfully', 200
    except Exception as e:
        return f"Error sending message: {e}", 500
    finally:
        await client.stop()



if __name__ == "__main__":
    loop.run_until_complete(app.run())