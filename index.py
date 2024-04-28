from flask import Flask, request
from telethon.sync import TelegramClient, events
from telethon import functions, types


# Замените на ваши данные авторизации
API_ID = 17735788
API_HASH = '285b5aee89a674d518dcc14f295c58f7'
PHONE_NUMBER = '+77071025816'

# Создаем объект приложения Flask
app = Flask(__name__)

# Создаем объект клиента Telethon
client = TelegramClient('anon', API_ID, API_HASH)

# Определяем функцию для отправки сообщения
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

if __name__ == '__main__':
    # Запускаем приложение Flask на локальном хосте
    app.run(host='0.0.0.0', port=5000)
