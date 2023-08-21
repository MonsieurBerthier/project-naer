import os
import library.io

from config.logger import logger


class Car:

    def __init__(self, main, car: str) -> None:

        self.main = main
        self.name = car

        self.path = os.path.join(self.main.PATH_CARS, self.name)
        self.json = library.io.get_json(path=os.path.join(self.path, self.main.PATH_CARS_CONFIG))
        self.models = {}

        self.load_car()

    def load_car(self):

        logger.debug(f"Loading car \"{self.name}\"")

        self.models["chassis"] = self.main.loader.loadModel(modelPath=os.path.join(self.path,
                                                                                   self.main.PATH_CARS_CHASSIS))
        self.models["chassis"].reparentTo(self.main.render)
        self.models["chassis"].setPos(tuple(self.json["chassis"]["position"]))
        self.models["chassis"].setHpr(tuple(self.json["chassis"]["rotation"]))
        self.models["chassis"].setScale(tuple(self.json["chassis"]["scale"]))

        # FIXME Use default wheels provided with the car instead
        wheels_json = library.io.get_json(path="content/wheels/japanracing_jr3/config.json")
        for wheel in self.json["wheels"]:
            logger.debug(f"Loading wheel \"{'japanracing_jr3'}\"")
            wheel_x = self.main.loader.loadModel(modelPath="content/wheels/japanracing_jr3/model.glb")
            wheel_x.setPos(tuple([a + b for a, b in zip(wheel["position"], wheels_json["position"])]))
            wheel_x.setHpr(tuple([a + b for a, b in zip(wheel["rotation"], wheels_json["rotation"])]))
            wheel_x.setScale(tuple([a * b for a, b in zip(wheel["scale"], wheels_json["scale"])]))
            wheel_x.reparentTo(self.main.render)

        for part in self.json["default"]:
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
        self.models[part_type].reparentTo(self.main.render)
