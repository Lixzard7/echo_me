from queue import Queue

# Microphone -> WebSocket
capture_queue = Queue(maxsize=100)

# WebSocket -> Speaker
playback_queue = Queue(maxsize=100)