from telethon import TelegramClient, types, functions
from dataclasses import dataclass
import hypercorn.asyncio
from quart import Quart, request
from quart_schema import QuartSchema, validate_request

api_id = 17735788
api_hash = '285b5aee89a674d518dcc14f295c58f7'
client = TelegramClient('telegram', api_id, api_hash)

app = Quart(__name__)
QuartSchema(app)

@app.before_serving
async def startup():
    await client.connect()


@app.after_serving
async def cleanup():
    await client.disconnect()

@app.route('/')
async def hello_world():
    await client.send_message('me', 'Hello World')
    return 'Message Sent!'

@app.post('/send_message')
async def send_message():

    data = await request.get_json()

    # Проверяем наличие необходимых данных в запросе
    if 'phone_number' not in data or 'text' not in data:
        return 'Missing parameters', 400

    # Пытаемся отправить сообщение
    try:
        # Получаем объект сущности для контакта
        contact_entity = await client.get_entity(data['phone_number'])
    except ValueError:
        # Если контакт отсутствует, добавляем его
        try:
            contact = types.InputPhoneContact(
                client_id=0,
                phone=data.get['phone_number'],
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

async def main():
    await hypercorn.asyncio.serve(app, hypercorn.Config())

if __name__ == '__main__':
    client.loop.run_until_complete(app.run())