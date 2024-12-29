import socketio  # обеспечивает двустороннюю связь в реальном времени между веб-клиентом
from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins='*') #разрешение на крос-доменные запросы
app = web.Application() # создание объекта веб сервера 
sio.attach(app) #прикрепляем сервер к сокету

 # создание обработчиков
  
 #обработчик подключения клиента к общей комнате
@sio.event
async def connect( sid, environ ):
    print(f'Клиент {sid} подключен')
    
    await sio.enter_room(sid, 'common_room') # подключение


 # обработчик отключения клиента к общей комнате
@sio.event
async def disconnect(sid):
    print(f'Клиент {sid} отключен')
    
    await sio.leave_room(sid, 'common_room') # отключение 

#обработчик нового сообщения от клиента 
@sio.event
async def message(sid, data):
    print(f'Получено сообщение от {sid}: {data}')
    
    await sio.emit('message', data, room= 'common_room', skip_sid=sid)#(отправляем сообщение всем кроме отправителя)

#запуск сервера
if __name__ == '__main__':
    web.run_app(app, port=12345)
    
   # !!! Важно !!! без клиентской части не работает  