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

# HTML-код для чата, включая CSS
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Локальный чат</title>
    <script src="https://cdn.socket.io/4.6.0/socket.io.min.js"></script>
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0;
            background-color: #bbbbbb;
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }
        header {
            color: rgb(0, 0, 0);
            width: 100%;
            text-align: center;
        }
        header h1 {
            text-shadow: 6px 6px 8px rgb(36, 152, 58);
        }
        #messages {
            width: 40%;
            height: 300px;
            max-height: 300px;
            overflow-y: auto;
            background-color: #808080;
            color: rgb(0, 0, 0);
            border-radius: 15px;
            margin-bottom: 20px;
            padding: 10px;
            display: flex;
            flex-direction: column;
            border: 1px solid rgb(152, 44, 44);
            background-color: rgb(106, 170, 170);
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }
        button {
            padding: 10px 20px;
            background-color: #000000;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #5a0153;
        }
        #nameInput,
        #messageInput {
            width: 30%;
            padding: 10px;
            margin-bottom: 5px;
            border: 1px solid #ccc;
            border-radius: 10px;
            margin: 10px 0;
        }
        #messages li {
             margin-bottom: 10px;
            padding: 8px;
            border-radius: 8px;
            max-width: 70%;
            word-wrap: break-word;
            clear: both;
            display: flex;
        }
        #messages li.sent {
            align-self: flex-end;
            background-color: #e0f7fa;
            margin-left: auto;
        }
        #messages li.received {
            align-self: flex-start;
            background-color: #f0f0f0;
            margin-right: auto;
        }
    </style>
</head>
<body>
    <header>
        <h1>Локальный чат</h1>
    </header>

    <ul id="messages"></ul>
    <form id="message-form">
        <input type="text" id="nameInput" placeholder="Имя">
        <input type="text" id="messageInput" placeholder="Сообщение">
        <button type="submit">Отправить :></button>
    </form>
    <script>
        const socket = io('http://' + window.location.hostname + ':12345', {autoConnect: true});
        const messagesList = document.getElementById('messages');
        const nameInput = document.getElementById('nameInput');
        const messageInput = document.getElementById('messageInput');
        let userName = '';
        const messageForm = document.getElementById('message-form');

        socket.on('connect', () => {
            console.log('Подключился к серверу');
            userName = nameInput.value.trim();
        });

        socket.on('disconnect', (reason) => {
             console.log('Отключился от сервера ', reason);
                if (reason === "io server disconnect"){
                  alert("Произошло отключение, попробуйте перезапустить страницу")
                 }
            });

        socket.on('message', (data) => {
            const messageItem = document.createElement('li');
            messageItem.innerHTML = `<strong>${data.sender}:</strong> ${data.text}`;
             if (data.sender === userName) {
                messageItem.classList.add('sent');
            } else {
                messageItem.classList.add('received');
            }
            messagesList.appendChild(messageItem);
            messagesList.scrollTop = messagesList.scrollHeight;
        });

      messageForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const currentName = nameInput.value.trim();
        const message = messageInput.value.trim();

        if (!currentName || !message) {
           alert("Вы не ввели имя или сообщение !");
            return;
        }
        userName = currentName;
        socket.emit('message', { text: message, author: userName });
        messageInput.value = '';
      });
    </script>
</body>
</html>
"""


# Добавляем маршрут для HTML-страницы
async def index(request):
    return web.Response(text=HTML_CONTENT, content_type='text/html')

# Регистрируем маршрут для /
app.add_routes([web.get('/', index)])

@sio.event
async def connect(sid, environ):
    print(f'Клиент {sid} подключен at {datetime.datetime.now().strftime("%H:%M:%S.%f")}')
    await sio.enter_room(sid, 'common_room')

@sio.event
async def disconnect(sid):
    print(f'Клиент {sid} отключен at {datetime.datetime.now().strftime("%H:%M:%S.%f")}')
    try:
        await sio.leave_room(sid, 'common_room')
    except Exception as e:
        print(f"Ошибка отключения клиента: {e}")
        traceback.print_exc()

@sio.event
async def message(sid, data):
   try:
        print(f'Получено сообщение от {sid}: {data} at {datetime.datetime.now().strftime("%H:%M:%S.%f")}')
        await sio.emit('message', {'sender': data['author'], 'text': data['text']}, room='common_room')
   except Exception as e:
       print(f"Ошибка отправки сообщения: {e}")
       traceback.print_exc()

async def run_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 12345)  # Слушаем на всех интерфейсах
    await site.start()
    print("Сервер запущен на порту 12345")
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