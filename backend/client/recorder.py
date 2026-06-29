import sounddevice as sd
import soundfile as sf
import numpy as np

SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5

print("Recording...")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16",
)

sd.wait()

print("Shape:", audio.shape)
print("Max:", np.max(audio))
print("Min:", np.min(audio))

sf.write("hello.wav", audio, SAMPLE_RATE)

print("Saved hello.wav")