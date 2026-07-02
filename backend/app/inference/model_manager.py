class ModelManager:

    def __init__(self):
        self.model = None
        self.index = None
        self.loaded = False

    async def load(self):
        """
        Locate and validate the single hardcoded model files.
        Sets `self.model` and `self.index` to filesystem paths (or None).
        """
        from pathlib import Path

        print("Loading voice model...")

        # backend directory is two parents up from this file (backend/app/inference)
        backend_dir = Path(__file__).resolve().parents[2]
        model_dir = backend_dir / "models"

        model_path = model_dir / "my_voice.pth"
        index_path = model_dir / "my_voice.index"

        if model_path.exists():
            self.model = str(model_path)
            print(f"Found model: {self.model}")
        else:
            print(f"Warning: model not found at {model_path}")

        if index_path.exists():
            self.index = str(index_path)
            print(f"Found index: {self.index}")
        else:
            print(f"Warning: index not found at {index_path}")

        self.loaded = True

    def is_loaded(self):
        return self.loaded