import asyncio
import asyncssh
import sys

async def run_client():
    async with asyncssh.connect('localhost', username='stargazer', password='Apple2011', known_hosts=None) as conn:
        result = await conn.run('ls', check=True)
        print(result.stdout, end='')

try:
    asyncio.get_event_loop().run_until_complete(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
