import sounddevice as sd

from config import SAMPLE_RATE, CHANNELS, BLOCK_SIZE, DTYPE
from audio.queue import playback_queue


def playback_callback(outdata, frames, time, status):

    if status:
        print(status)

    if not playback_queue.empty():

        chunk = playback_queue.get()

        outdata[:] = chunk

    else:

        outdata.fill(0)


def start_playback():

    return sd.OutputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
        blocksize=BLOCK_SIZE,
        callback=playback_callback,
    )