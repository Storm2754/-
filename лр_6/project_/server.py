import socketio
from aiohttp import web
import asyncio
import datetime
import os
import sys
import traceback

# Инициализация Socket.IO сервера
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print(f'Klient {sid} connect {datetime.datetime.now().strftime("%H:%M:%S.%f")}')
    await sio.enter_room(sid, 'common_room')

@sio.event
async def disconnect(sid):
    print(f'Kient {sid} disconnect {datetime.datetime.now().strftime("%H:%M:%S.%f")}')
    try:
        await sio.leave_room(sid, 'common_room')
    except Exception as e:
        print(f"Ошибка отключения клиента: {e}")
        traceback.print_exc()

@sio.event
async def message(sid, data):
   try:
    # Отправляем сообщение всем, включая отправителя
        print(f'Message_received {sid}: {data} at {datetime.datetime.now().strftime("%H:%M:%S.%f")}')
        await sio.emit('message', {'sender': data['author'], 'text': data['text']}, room='common_room')
   except Exception as e:
       print(f"Ошибка отправки сообщения: {e}")
       traceback.print_exc()

async def run_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)  # Слушаем на всех интерфейсах
    await site.start()
    print("Start_serv 5000")
    await asyncio.Future()  # Держим сервер запущенным

async def main():
    try:
        await run_server()
    except KeyboardInterrupt:
        print("Сервер остановлен по Ctrl+C")
    finally:
        sys.exit(0)

if __name__ == '__main__':
    asyncio.run(main())