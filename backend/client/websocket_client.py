import asyncio
import websockets

from config import SERVER_URL
from audio.queue import capture_queue, playback_queue


async def send_audio(websocket):
    print("🎤 Sender started")

    while True:
        chunk = capture_queue.get()
        await websocket.send(chunk.tobytes())


async def receive_audio(websocket):
    print("🔊 Receiver started")

    while True:
        data = await websocket.recv()

        # Convert bytes back to numpy array
        import numpy as np

        audio = np.frombuffer(data, dtype=np.int16)
        audio = audio.reshape(-1, 1)

        playback_queue.put(audio)


async def start_websocket():

    print(f"Connecting to {SERVER_URL}")

    async with websockets.connect(SERVER_URL) as websocket:

        print("✅ Connected to backend")

        sender = asyncio.create_task(
            send_audio(websocket)
        )

        receiver = asyncio.create_task(
            receive_audio(websocket)
        )

        await asyncio.gather(
            sender,
            receiver
        )