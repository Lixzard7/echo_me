import queue
import sounddevice as sd

SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 320  # 20 ms @ 16 kHz

audio_queue = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status)

    audio_queue.put(indata.copy())


print("Streaming... Press Ctrl+C to stop.")

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16",
    blocksize=BLOCK_SIZE,
    callback=callback,
):
    try:
        while True:
            chunk = audio_queue.get()

            print(
                f"Chunk: {chunk.shape}, "
                f"Max: {chunk.max()}, "
                f"Min: {chunk.min()}"
            )

    except KeyboardInterrupt:
        print("Stopped.")