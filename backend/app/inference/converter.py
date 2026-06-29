from app.inference.base import VoiceConverter


class ApplioVoiceConverter(VoiceConverter):

    async def initialize(self):
        print("Initializing converter...")

    async def convert(self, audio_bytes: bytes) -> bytes:
        """
        Placeholder implementation.

        For now we simply return the original audio.
        """
        return audio_bytes