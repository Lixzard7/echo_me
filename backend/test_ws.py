import asyncio
import websockets

async def test():
    uri = "ws://127.0.0.1:8000/audio"

    async with websockets.connect(uri) as websocket:
        message = b"Hello EchoMe"

        await websocket.send(message)

        response = await websocket.recv()

        print("Server replied:", response)

asyncio.run(test())