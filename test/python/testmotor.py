import asyncio
import motor.motor_asyncio
import functools

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client['MyCRT']


@asyncio.coroutine
def find(username, password):
    print(88888888)
    u = yield from db.user.find_one({'username': username, 'password': password})
    return u

loop = asyncio.get_event_loop()
user = asyncio.run_coroutine_threadsafe(find('foo', 'bar'), loop)
print(user.result())
loop.run_forever()
