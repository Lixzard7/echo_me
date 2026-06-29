class ModelManager:

    def __init__(self):
        self.model = None
        self.index = None
        self.loaded = False

    async def load(self):
        """
        This will later load:
            - .pth
            - .index
        """
        print("Loading voice model...")

        self.loaded = True

    def is_loaded(self):
        return self.loaded