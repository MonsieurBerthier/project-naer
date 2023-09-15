import os

import panda3d.core

import library.io

from config.logger import logger


class Car:

    def __init__(self, main) -> None:

        self.main = main
        self.name = self.main.config_json["defaults"]["car"]

        self.path = None
        self.json = None
        self.models = None
        self.nodepath = None

        self.load(name=self.name)

    def load(self, name: str) -> None:

        if self.models:
            self.unload()

        logger.debug(f"Loading car \"{name}\"")

        self.path = os.path.join(self.main.PATH_CARS, name)
        self.json = library.io.get_json(path=os.path.join(self.path, self.main.PATH_ITEMS_CONFIG_JSON))
        self.nodepath = panda3d.core.NodePath("car")
        self.nodepath.reparentTo(self.main.render)

        self.models = {"chassis": self.main.loader.loadModel(modelPath=os.path.join(self.path,
                                                                                    self.main.PATH_CARS_CHASSIS)),
                       "wheels": {}}
        self.models["chassis"].reparentTo(self.nodepath)
        self.models["chassis"].setPos(tuple(self.json["chassis"]["position"]))
        self.models["chassis"].setHpr(tuple(self.json["chassis"]["rotation"]))
        self.models["chassis"].setScale(tuple(self.json["chassis"]["scale"]))

        for part in self.json["defaults"]:
            if "wheel" in part:
                self.load_wheels(name=part, oem=True)
            else:
                self.load_part(part=part)

    def load_part(self, part: str) -> None:

        logger.debug(f"Loading car part \"{part}\"")

        part_type = part.split("_")[0]

        if part_type in self.models:
            self.models[part_type].removeNode()

        self.models[part_type] = self.main.loader.loadModel(modelPath=os.path.join(self.path, part + ".glb"))
        self.models[part_type].setPos(tuple(self.json["chassis"]["position"]))
        self.models[part_type].setHpr(tuple(self.json["chassis"]["rotation"]))
        self.models[part_type].setScale(tuple(self.json["chassis"]["scale"]))
        self.models[part_type].reparentTo(self.nodepath)

    def load_bodykit(self, bodykit: str) -> None:

        logger.debug(f"Loading bodykit \"{bodykit}\"")

        for part in set(self.models.keys()) - {"chassis", "wheels"}:
            self.unload_part(part=part)

        bodykit_partlist = [kit["parts"] for kit in self.json["bodykits"] if kit["name"] == bodykit][0]

        for part in bodykit_partlist:
            self.load_part(part=part)

    def load_wheels(self, name: str, oem: bool) -> None:

        if self.models["wheels"]:
            self.unload_wheels()

        logger.debug(f"Loading car wheel \"{name}\"")

        if oem:
            wheel_path = os.path.join(self.path, name + ".glb")
        else:
            wheel_path = os.path.join(self.main.PATH_WHEELS, name, name + ".glb")

        for axle in self.json["wheels"]:
            self.models["wheels"][axle] = []
            for wheel in self.json["wheels"][axle]:
                wheel_model = self.main.loader.loadModel(modelPath=wheel_path)
                wheel_model.setPos(tuple(wheel["position"]))
                wheel_model.setHpr(tuple(wheel["rotation"]))
                wheel_model.setScale(tuple(wheel["scale"]))
                wheel_model.reparentTo(self.main.render)
                self.models["wheels"][axle].append(wheel_model)

    def unload(self):

        logger.debug(f"Unloading car \"{self.name}\"")

        self.path = None
        self.json = None

        for item in list(self.models):
            if isinstance(self.models[item], dict):
                self.unload_wheels()
            else:
                self.unload_part(part=item)

        self.models = None

    def unload_part(self, part: str) -> None:

        logger.debug(f"Unloading car part \"{part}\"")

        self.models[part].removeNode()
        self.models.pop(part)

    def unload_wheels(self) -> None:

        logger.debug(f"Unloading car wheels")

        for axle in self.models["wheels"]:
            for wheel in self.models["wheels"][axle]:
                wheel.removeNode()

        self.models["wheels"] = {}
