import os
import library.io

from config.logger import logger


class Ground:

    def __init__(self, main) -> None:

        self.main = main
        self.name = self.main.config_json["default"]["ground"]

        self.path = None
        self.model = None

        self.load(name=self.name)

    def load(self, name: str) -> None:

        if self.model:
            self.unload()

        logger.debug(f"Loading ground \"{name}\"")

        self.name = name
        self.path = os.path.join(self.main.PATH_GROUNDS, name)

        glb = library.io.get_file_path(path=self.path, extension="glb")
        self.model = self.main.loader.loadModel(modelPath=os.path.join(self.path, glb))
        self.model.setLightOff()
        self.model.reparentTo(self.main.render)

    def unload(self):

        logger.debug(f"Unloading ground \"{self.name}\"")

        self.name = None
        self.path = None
        self.model.removeNode()

