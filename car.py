import os

import panda3d.core

import library.io

from config.logger import logger


class Item:

    def __init__(self, tag: str, name: str, model) -> None:

        self.tag = tag
        self.name = name
        self.model = model

    def unload_model(self):

        self.model.removeNode()


class Car:

    def __init__(self, main) -> None:

        self.main = main

        self.name = None
        self.path = None
        self.json = None
        self.items = None
        self.nodepath = None

        self.load(tag=self.main.config_json["defaults"]["car"])

    @staticmethod
    def get_part_type(tag: str) -> str:

        return tag.split("_")[0]

    def load(self, tag: str) -> None:

        if self.items:
            self.unload()

        logger.debug(f"Loading car \"{tag}\"")

        self.path = os.path.join(self.main.PATH_CARS, tag)
        self.json = library.io.get_json(path=os.path.join(self.path, self.main.PATH_ITEMS_CONFIG_JSON))
        self.name = self.json["name"]
        self.nodepath = panda3d.core.NodePath("car")
        self.nodepath.reparentTo(self.main.render)

        self.items = {"chassis": Item(tag=tag,
                                      name="Main Body",
                                      model=self.main.loader.loadModel(
                                          modelPath=os.path.join(self.path, self.main.PATH_CARS_CHASSIS))),
                      "wheels": {}}

        self.items["chassis"].model.reparentTo(self.nodepath)
        self.items["chassis"].model.setPos(tuple(self.json["chassis"]["position"]))
        self.items["chassis"].model.setHpr(tuple(self.json["chassis"]["rotation"]))
        self.items["chassis"].model.setScale(tuple(self.json["chassis"]["scale"]))

        for part in self.json["defaults"]:
            if "wheel" in part:
                self.load_wheels(tag=part, oem=True)
            else:
                self.load_part(tag=part)

    def load_part(self, tag: str) -> None:

        logger.debug(f"Loading car part \"{tag}\"")

        part_type = self.get_part_type(tag=tag)

        if part_type in self.items:
            self.items[part_type].unload_model()

        self.items[part_type] = Item(tag=tag,
                                     name=self.json["names"][tag],
                                     model=self.main.loader.loadModel(
                                         modelPath=os.path.join(self.path, tag + ".glb")))

        self.items[part_type].model.setPos(tuple(self.json["chassis"]["position"]))
        self.items[part_type].model.setHpr(tuple(self.json["chassis"]["rotation"]))
        self.items[part_type].model.setScale(tuple(self.json["chassis"]["scale"]))
        self.items[part_type].model.reparentTo(self.nodepath)

    def load_wheels(self, tag: str, oem: bool) -> None:

        if self.items["wheels"]:
            self.unload_wheels()

        logger.debug(f"Loading car wheel \"{tag}\"")

        if oem:
            wheel_path = os.path.join(self.path, tag + ".glb")
            wheel_name = self.json["names"][tag]
        else:
            wheel_path = os.path.join(self.main.PATH_WHEELS, tag, tag + ".glb")
            wheel_name = library.io.get_json(path=os.path.join(self.main.PATH_WHEELS,
                                                               tag, self.main.PATH_ITEMS_CONFIG_JSON))["name"]

        for axle in self.json["wheels"]:
            self.items["wheels"][axle] = []
            for wheel in self.json["wheels"][axle]:
                wheel_item = Item(tag=tag,
                                  name=wheel_name,
                                  model=self.main.loader.loadModel(modelPath=wheel_path))
                wheel_item.model.setPos(tuple(wheel["position"]))
                wheel_item.model.setHpr(tuple(wheel["rotation"]))
                wheel_item.model.setScale(tuple(wheel["scale"]))
                wheel_item.model.reparentTo(self.main.render)
                self.items["wheels"][axle].append(wheel_item)

    def load_bodykit(self, bodykit: str) -> None:

        logger.debug(f"Loading bodykit \"{bodykit}\"")

        for part in set(self.items.keys()) - {"chassis", "wheels"}:
            self.unload_part(tag=part)

        bodykit_partlist = [kit["parts"] for kit in self.json["bodykits"] if kit["name"] == bodykit][0]

        for part in bodykit_partlist:
            self.load_part(tag=part)

    def unload(self) -> None:

        logger.debug(f"Unloading car \"{self.items['chassis'].tag}\"")

        self.path = None
        self.json = None

        for item in list(self.items):
            if item == "chassis":
                self.items["chassis"].unload_model()
            elif isinstance(self.items[item], dict):
                self.unload_wheels()
            else:
                self.unload_part(tag=item)

        self.items = None

    def unload_part(self, tag: str) -> None:

        logger.debug(f"Unloading car part \"{tag}\"")

        part_type = self.get_part_type(tag=tag)

        if part_type in list(self.items):
            self.items[part_type].unload_model()
            self.items.pop(part_type)

    def unload_wheels(self) -> None:

        logger.debug(f"Unloading car wheels")

        for axle in self.items["wheels"]:
            for wheel in self.items["wheels"][axle]:
                wheel.unload_model()

        self.items["wheels"] = {}

    def get_items_status(self):

        items = []

        car_parts = library.io.get_file_path(path=self.main.car.path, extension="glb", number=0)
        car_parts.remove(self.main.PATH_CARS_CHASSIS)
        car_parts = [part.split(".")[0] for part in car_parts]

        for part in car_parts:

            tag = part.split(".")[0]
            part_type = self.get_part_type(tag=tag)

            part_not_installed = {"tag": tag,
                                  "name": self.json["names"][tag],
                                  "installed": False,
                                  "color": (0, 0, 0, 0)}

            if part_type in self.items:

                if self.items[part_type].tag == tag:

                    if self.items[part_type].model.findMaterial("paint"):
                        paint_color = self.items[part_type].model.findMaterial("paint").getBaseColor()
                    else:
                        paint_color = (0, 0, 0, 0)

                    items.append({"tag": tag,
                                  "name": self.items[part_type].name,
                                  "installed": True,
                                  "color": paint_color})
                else:
                    items.append(part_not_installed)
            else:
                items.append(part_not_installed)

        return items
