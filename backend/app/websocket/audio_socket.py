from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import wave

from app.websocket.connection_manager import manager
from app.inference.service import voice_service

router = APIRouter()

SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2  # int16 = 2 bytes


@router.websocket("/audio")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    frames = []

    try:
        while True:

            # Receive raw PCM audio from client
            data = await websocket.receive_bytes()

            # Save original audio for debugging
            frames.append(data)

            # Voice conversion (currently passthrough)
            converted_audio = await voice_service.convert(data)

            # Send converted audio back to client
            await manager.send(websocket, converted_audio)

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        print("Client disconnected.")

        # Save received audio for debugging
        with wave.open("received.wav", "wb") as wav_file:
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(SAMPLE_WIDTH)
            wav_file.setframerate(SAMPLE_RATE)

            for frame in frames:
                wav_file.writeframes(frame)

        print("Audio saved as received.wav")