import os
import library.io


class Ground:

    def __init__(self, main) -> None:

        self.main = main
        self.tag = self.main.config_json["defaults"]["ground"]

        self.path = None
        self.model = None

        self.load(tag=self.tag)

    def load(self, tag: str) -> None:

        if self.model:
            self.unload()

        self.tag = tag
        self.path = os.path.join(self.main.PATH_GROUNDS, tag)

        glb = library.io.get_file_path(path=self.path, extension="glb")
        self.model = self.main.loader.loadModel(modelPath=os.path.join(self.path, glb))
        self.model.setLightOff()
        self.model.reparentTo(self.main.render)

    def unload(self) -> None:

        self.tag = None
        self.path = None
        self.model.removeNode()

    def set_light(self, light) -> None:

        self.model.setLight(light)

    def change(self, tag: str) -> None:

        self.unload()
        self.load(tag=tag)
        self.set_light(self.main.light_shadow_node)
        self.set_light(self.main.light_top_node)
