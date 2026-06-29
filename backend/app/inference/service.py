from app.inference.model_manager import ModelManager
from app.inference.converter import ApplioVoiceConverter


class VoiceService:

    def __init__(self):
        self.manager = ModelManager()
        self.converter = ApplioVoiceConverter()

    async def initialize(self):
        await self.manager.load()
        await self.converter.initialize()

    async def convert(self, audio: bytes) -> bytes:
        return await self.converter.convert(audio)


voice_service = VoiceService()