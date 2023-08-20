import os
import library.io

from config.logger import logger


class Ground:

    def __init__(self, main, ground: str) -> None:

        self._main = main
        self._ground_name = ground

        self._ground_path = os.path.join(self._main.PATH_GROUNDS, self._ground_name)
        self._ground_model = None

        self.load_ground()

    def load_ground(self) -> None:

        logger.debug(f"Loading ground \"{self._ground_name}\"")

        ground_glb = library.io.get_file_path(path=self._ground_path, extension="glb")
        self._ground_model = self._main.loader.loadModel(modelPath=os.path.join(self._ground_path, ground_glb))
        self._ground_model.setLightOff()
        self._ground_model.reparentTo(self._main.render)

    def get_ground_model(self):

        return self._ground_model