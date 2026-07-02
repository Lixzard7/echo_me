from abc import ABC, abstractmethod


class VoiceConverter(ABC):

    @abstractmethod
    async def initialize(self, manager=None):
        """Load model into memory. Optionally receive a `ModelManager` instance."""
        pass

    @abstractmethod
    async def convert(self, audio_bytes: bytes) -> bytes:
        """Convert incoming PCM audio."""
        pass