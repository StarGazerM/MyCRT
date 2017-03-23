import asyncio
import asyncssh

async def async_run_client():
    host_local = 'localhost'
    username_local = 'stargazer'
    password_local = 'Apple2011'
    host_remote = 'localhost'
    username_remote = 'foo'
    password_remote = 'bar'
    # with open('id_rsa.pub') as file:
    #     key = asyncssh.import_public_key(file.read())

    # conn_local = asyncssh.connect(
    #     host=host_local, port=22, username=username_local,
    #     password=password_local, known_hosts=None)
    # conn_remote = asyncssh.connect(
    #     host=host_remote, port=2200, username=username_remote,
    #     password=password_remote, known_hosts=None)
    # stdin_local, stdout_local, stderror_local = await conn_local.open_session()
    # stdin_remote, stdout_remote, stderror_remote = await conn_remote.open_session()
    # await stdin_remote.write(username_remote)
    # loop.create_task(exchange_data(stdout_local, stdin_remote))
    # loop.create_task(exchange_data(stdout_remote, stdin_local))
    async with asyncssh.connect(
            host=host_local, port=22, username=username_local,
            password=password_local, known_hosts=None) as conn_local:
        stdin_local, stdout_local, stderror_local = await conn_local.open_session()

    async with asyncssh.connect(
            host=host_remote, port=2200, username=username_remote,
            password=password_remote, known_hosts=None) as conn_remote:
        stdin_remote, stdout_remote, stderror_remote = await conn_remote.open_session()

    await stdin_remote.write(username_remote)
    loop.create_task(exchange_data(stdout_local, stdin_remote))
    loop.create_task(exchange_data(stdout_remote, stdin_local))

async def exchange_data(reader, writer):
    while True:
        data = await reader.read()
        await writer.write(data)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_run_client())
    loop.run_forever()
