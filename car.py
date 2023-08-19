import os
import library.io

from config.logger import logger


class Car:

    def __init__(self, main, car: str) -> None:

        self._main = main
        self._car_name = car

        self._car_path = os.path.join(self._main.PATH_CARS, self._car_name)
        self._car_json = library.io.get_json(path=os.path.join(self._car_path, self._main.PATH_CARS_CONFIG))
        self._car_models = {}

        self.load_car()

    def load_car(self):

        logger.debug(f"Loading car \"{self._car_name}\"")

        self._car_models["chassis"] = self._main.loader.loadModel(modelPath=os.path.join(self._car_path, self._main.PATH_CARS_CHASSIS))
        self._car_models["chassis"].reparentTo(self._main.render)
        self._car_models["chassis"].setPos(tuple(self._car_json["chassis"]["position"]))
        self._car_models["chassis"].setHpr(tuple(self._car_json["chassis"]["rotation"]))
        self._car_models["chassis"].setScale(tuple(self._car_json["chassis"]["scale"]))

        # FIXME Use default wheels provided with the car instead
        wheels_json = library.io.get_json(path="content/wheels/japanracing_jr3/config.json")
        for wheel in self._car_json["wheels"]:
            logger.debug(f"Loading wheel \"{'japanracing_jr3'}\"")
            wheel_x = self._main.loader.loadModel(modelPath="content/wheels/japanracing_jr3/model.glb")
            wheel_x.setPos(tuple([a + b for a, b in zip(wheel["position"], wheels_json["position"])]))
            wheel_x.setHpr(tuple([a + b for a, b in zip(wheel["rotation"], wheels_json["rotation"])]))
            wheel_x.setScale(tuple([a * b for a, b in zip(wheel["scale"], wheels_json["scale"])]))
            wheel_x.reparentTo(self._main.render)

        for part in self._car_json["default"]:
            self.load_part(part=part)

    def load_part(self, part: str) -> None:

        logger.debug(f"Loading car part \"{part}\"")

        part_type = part.split("_")[0]

        if part_type in self._car_models:
            logger.debug(self._car_models[part_type])
            self._car_models[part_type].removeNode()

        self._car_models[part_type] = self._main.loader.loadModel(modelPath=os.path.join(self._car_path, part + ".glb"))
        self._car_models[part_type].setPos(tuple(self._car_json["chassis"]["position"]))
        self._car_models[part_type].setHpr(tuple(self._car_json["chassis"]["rotation"]))
        self._car_models[part_type].setScale(tuple(self._car_json["chassis"]["scale"]))
        self._car_models[part_type].reparentTo(self._main.render)
