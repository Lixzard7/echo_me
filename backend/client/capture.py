import sounddevice as sd

from config import SAMPLE_RATE, CHANNELS, BLOCK_SIZE, DTYPE
from audio.queue import capture_queue


def audio_callback(indata, frames, time, status):

    if status:
        print(status)

    # Store a copy of every 20 ms chunk
    capture_queue.put(indata.copy())


def start_capture():

    return sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
        blocksize=BLOCK_SIZE,
        callback=audio_callback,
    )