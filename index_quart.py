from telethon import TelegramClient, types, functions
import os
from telethon.tl.functions.messages import SendMessageRequest
import hypercorn.asyncio
from quart import Quart, request
from quart_schema import QuartSchema, validate_request

api_id = os.getenv('API_ID', 1234567)
api_hash = os.getenv('API_HASH', 'qwerty123456')
client = TelegramClient('telegram', api_id, api_hash)

app = Quart(__name__)
QuartSchema(app)

@app.before_serving
async def startup():
    await client.connect()

@app.after_serving
async def cleanup():
    await client.disconnect()

@app.route('/settings')
async def settings():
    return {'api_id': api_id, 'api_hash': api_hash}

@app.route('/start')
async def start():
    await client.send_message('me', 'Hello, myself!')
    return {'api_id': api_id, 'api_hash': api_hash}

@app.post('/check_contact')
async def check_contact():
    data = await request.get_json()
    try:
        if 'phone_number' in data:
            contact = await client.get_input_entity(data['phone_number'])
            print(contact)
            return {"user_id":contact.user_id}, 200
        elif 'username' in data:
            contact = await client.get_input_entity(data['username'])
            print(contact)
            return {"user_id":contact.user_id}, 200
        elif 'user_id' in data:
            contact = await client.get_input_entity(data['user_id'])
            print(contact)
            return {"user_id":contact.user_id}, 200
        else:
            return 'Missing parameters', 400
    except Exception as e:
        return f"Error finding contact: {e}", 500

@app.post('/send_message')
async def send_message():

    data = await request.get_json()
    # Проверяем наличие необходимых данных в запросе
    if 'user_id' not in data or 'text' not in data:
        return 'Missing parameters', 400
    try:
        contact = await client.get_input_entity(data['user_id'])
        print(contact)
    except Exception as e:
        return f"Error finding contact: {e}", 500
    try:
        result = await client(SendMessageRequest(contact, data['text']))
        print(result)
        return {"user_id":contact.user_id, "message_id": result.id}, 200
    except Exception as e:
        return f"Error finding contact: {e}", 500

async def main():
    await hypercorn.asyncio.serve(app, hypercorn.Config())

if __name__ == '__main__':
    client.loop.run_until_complete(app.run())