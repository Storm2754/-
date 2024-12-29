import socketio  # Обеспечивает двустороннюю связь в реальном времени между веб-клиентом и сервером
from aiohttp import web
import asyncio


# Инициализация Socket.IO сервера
sio = socketio.AsyncServer(cors_allowed_origins='*')  # Разрешение на кросс-доменные запросы

# Создание веб-приложения aiohttp
app = web.Application()

# Прикрепление Socket.IO сервера к веб-приложению
sio.attach(app)

# Обработчик подключения клиента
@sio.event
async def connect(sid: str, environ: dict) -> None:
    print(f'Клиент {sid} подключен')
    await sio.enter_room(sid, 'common_room')  # Подключение к общей комнате

# Обработчик отключения клиента
@sio.event
async def disconnect(sid: str) -> None:
    print(f'Клиент {sid} отключен')
    await sio.leave_room(sid, 'common_room') # Отключение от общей комнаты

# Обработчик нового сообщения от клиента
@sio.event
async def message(sid: str, data: str) -> None:
    print(f'Получено сообщение от {sid}: {data}')
    await sio.emit('message', data, room='common_room', skip_sid=sid)  # Отправка сообщения всем, кроме отправителя

# Запуск сервера
async def main() -> None:
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 12345)
    await site.start()

    print("Сервер запущен на порту 12345")

    # Keep the program running until interrupted (e.g. by Ctrl+C)
    try:
      await asyncio.Future()
    except asyncio.CancelledError:
      await runner.cleanup()

if __name__ == '__main__':
    asyncio.run(main())

# !!! Важно !!! без клиентской части не работает