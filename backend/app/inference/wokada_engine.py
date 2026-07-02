from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
WOKADA_SERVER = ROOT / "wokada" / "server"

if str(WOKADA_SERVER) not in sys.path:
    sys.path.insert(0, str(WOKADA_SERVER))


class WokadaEngine:
    def __init__(self):
        self.pipeline = None
        self.initialized = False
        self.model_path = None
        self.index_path = None
        self.rvc = None

    def initialize(self, model_path: str | None = None, index_path: str | None = None):
        """
        Basic initialization that records model/index paths and marks the engine ready.
        This is a lightweight stub that prepares the engine for later integration
        with the full W-Okada loaders already present under `wokada/server`.
        """
        if self.initialized:
            return

        print("Loading W-Okada engine...")

        self.model_path = model_path
        self.index_path = index_path

        if model_path:
            print(f"Using model: {model_path}")
        else:
            print("No model path provided to engine during initialization.")

        if index_path:
            print(f"Using index: {index_path}")

        # TODO: integrate with wokada/server loader functions here.

        self.initialized = True
        print("Engine Ready")

        # Try to wire up a minimal RVC instance from the W-Okada code if model is provided
        try:
            if model_path is not None:
                from voice_changer.RVC.RVC import RVC
                from voice_changer.RVC.RVCModelSlotGenerator import RVCModelSlotGenerator
                from data.ModelSlot import RVCModelSlot
                from voice_changer.VoiceChangerParamsManager import VoiceChangerParamsManager
                from voice_changer.utils.VoiceChangerParams import VoiceChangerParams

                print("Attempting to initialize RVC from wokada code...")

                # Minimal params: set model_dir to the parent directory of the model
                model_dir = str(Path(model_path).resolve().parents[0])
                params = VoiceChangerParams(
                    model_dir=model_dir,
                    content_vec_500="",
                    content_vec_500_onnx="",
                    content_vec_500_onnx_on=False,
                    hubert_base="",
                    hubert_base_jp="",
                    hubert_soft="",
                    nsf_hifigan="",
                    sample_mode="production",
                    crepe_onnx_full="",
                    crepe_onnx_tiny="",
                    rmvpe="",
                    rmvpe_onnx="",
                    whisper_tiny="",
                )

                # register params
                VoiceChangerParamsManager.get_instance().setParams(params)

                # Build slotInfo by probing the pytorch file (this will load small metadata)
                slot = RVCModelSlot()
                try:
                    slot = RVCModelSlotGenerator._setInfoByPytorch(model_path, slot)
                except Exception as e:
                    print(f"RVC slot probing failed: {e}")

                # Instantiate RVC and initialize pipeline
                try:
                    rvci = RVC(params, slot)
                    rvci.initialize()
                    self.rvc = rvci
                    print("RVC engine initialized and ready")
                except Exception as e:
                    print(f"Failed to initialize RVC instance: {e}")
                    self.rvc = None

        except Exception as e:
            print(f"Wokada integration skipped due to error: {e}")

    def convert(self, pcm):
        """
        Receives PCM audio.
        Returns converted PCM.
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")

        # If RVC instance available, run inference path
        if self.rvc is not None:
            try:
                # Accept raw bytes or numpy array
                if isinstance(pcm, (bytes, bytearray)):
                    arr = np.frombuffer(pcm, dtype=np.int16)
                elif isinstance(pcm, np.ndarray):
                    arr = pcm
                else:
                    # unknown format, passthrough
                    return pcm

                # Use length as inputSize, no crossfade for now
                input_size = int(arr.shape[0])
                crossfade = 0

                data = self.rvc.generate_input(arr, input_size, crossfade)
                out = self.rvc.inference(data)

                if out is None:
                    return pcm

                # out is float numpy array in model sampling; convert to int16 bytes
                out_int16 = (out * 32768.0).astype(np.int16)
                return out_int16.tobytes()

            except Exception as e:
                print(f"RVC conversion failed: {e}")
                return pcm

        # Fallback: passthrough
        return pcm