import websockets
import asyncio
# def send_command(msg):
async def talk(msg):
    url = "ws://192.168.100.178:81"

    async with websockets.connect(url) as ws:
        while True:
            await ws.send(msg)


    asyncio.get_event_loop().run_until_complete(talk(msg))

