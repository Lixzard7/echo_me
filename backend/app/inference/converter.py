from app.inference.base import VoiceConverter
from app.inference.wokada_engine import WokadaEngine


class ApplioVoiceConverter(VoiceConverter):

    def __init__(self):
        self.engine: WokadaEngine | None = None

    async def initialize(self, manager=None):
        print("Initializing converter...")
        self.engine = WokadaEngine()

        model_path = None
        index_path = None
        if manager is not None:
            model_path = getattr(manager, "model", None)
            index_path = getattr(manager, "index", None)

        # Initialize engine with available model/index paths (may be None)
        self.engine.initialize(model_path, index_path)

    async def convert(self, audio_bytes: bytes) -> bytes:
        """
        If the engine is initialized, forward conversion to it; otherwise passthrough.
        """
        if self.engine is None or not self.engine.initialized:
            return audio_bytes

        return self.engine.convert(audio_bytes)