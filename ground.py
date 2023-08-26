import os
import library.io

from config.logger import logger


class Ground:

    def __init__(self, main) -> None:

        self.main = main
        self.name = self.main.config_json["default"]["ground"]

        self.path = os.path.join(self.main.PATH_GROUNDS, self.name)
        self.model = None

        self.load_ground()

    def load_ground(self) -> None:

        logger.debug(f"Loading ground \"{self.name}\"")

        glb = library.io.get_file_path(path=self.path, extension="glb")
        self.model = self.main.loader.loadModel(modelPath=os.path.join(self.path, glb))
        self.model.setLightOff()
        self.model.reparentTo(self.main.render)
