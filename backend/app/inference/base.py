from abc import ABC, abstractmethod


class VoiceConverter(ABC):

    @abstractmethod
    async def initialize(self):
        """Load model into memory."""
        pass

    @abstractmethod
    async def convert(self, audio_bytes: bytes) -> bytes:
        """Convert incoming PCM audio."""
        pass