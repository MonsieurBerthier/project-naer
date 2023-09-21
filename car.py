import os

import panda3d.core

import library.io

from config.logger import logger


class Item:

    def __init__(self, tag: str, name: str, model) -> None:

        self.tag = tag
        self.name = name
        self.model = model

    def unload_model(self) -> None:

        if self.model:
            self.model.removeNode()
            self.model = None


class Car:

    def __init__(self, main) -> None:

        self.main = main

        self.path = None
        self.json = None
        self.items = None
        self.nodepath = None

        self.load(tag=self.main.config_json["defaults"]["car"])

    def is_default(self, tag: str) -> bool:

        return tag in self.json["defaults"]

    def is_optional(self, tag: str) -> bool:

        return self.get_part_type(tag=tag) in self.json["optional"]

    @staticmethod
    def get_part_type(tag: str) -> str:

        return tag.split("_")[0]

    def get_items_of_same_part_type(self, tag: str) -> list:

        found_items = []
        part_type = self.get_part_type(tag=tag)

        for i in self.items:
            if "wheels" not in i:
                if self.items[i].tag.startswith(part_type) and self.items[i].model:
                    found_items.append(self.items[i].tag)

        return found_items

    def check_car_config_sanity(self, tag: str) -> None:

        car_parts_files = library.io.get_file_path(path=self.path, extension="glb", number=0)
        car_parts_files = [part.split(".")[0] for part in car_parts_files]

        car_parts_json = list(self.json["names"])

        assert sorted(car_parts_files) == sorted(car_parts_json), \
            f"mismatch between content in car folder \"{tag}\" and \"{self.main.PATH_ITEMS_CONFIG_JSON}\" file"

    def load(self, tag: str) -> None:

        if self.items:
            self.unload()

        logger.debug(f"Loading car \"{tag}\"")

        self.path = os.path.join(self.main.PATH_CARS, tag)
        self.json = library.io.get_json(path=os.path.join(self.path, self.main.PATH_ITEMS_CONFIG_JSON))
        self.nodepath = panda3d.core.NodePath("car")
        self.nodepath.reparentTo(self.main.render)
        self.items = {}

        self.check_car_config_sanity(tag=tag)

        for item_tag in self.json["names"]:

            if self.is_default(tag=item_tag):

                if "wheel" in item_tag:
                    self.load_wheels(tag=item_tag, oem=True)
                else:
                    self.load_part(tag=item_tag)

            else:
                self.items[item_tag] = Item(tag=item_tag, name=self.json["names"][item_tag], model=None)

    def load_part(self, tag: str) -> None:

        part_type = self.get_part_type(tag=tag)

        if part_type == "wheel":
            return
        elif tag not in self.json["names"]:
            return
        elif self.get_items_of_same_part_type(tag=tag) == [tag] and self.is_optional(tag=tag):
            self.unload_part(tag=tag)
            return

        logger.debug(f"Loading car part \"{tag}\"")

        for part in self.get_items_of_same_part_type(tag=tag):
            self.items[part].unload_model()

        self.items[tag] = Item(tag=tag,
                               name=self.json["names"][tag],
                               model=self.main.loader.loadModel(modelPath=os.path.join(self.path, tag + ".glb")))
        self.items[tag].model.setPos(tuple(self.json["chassis"]["position"]))
        self.items[tag].model.setHpr(tuple(self.json["chassis"]["rotation"]))
        self.items[tag].model.setScale(tuple(self.json["chassis"]["scale"]))
        self.items[tag].model.reparentTo(self.nodepath)

    def load_wheels(self, tag: str, oem: bool) -> None:

        if "wheels" in self.items:
            self.unload_wheels()

        logger.debug(f"Loading car wheels \"{tag}\"")

        if oem:
            wheel_path = os.path.join(self.path, tag + ".glb")
            wheel_name = self.json["names"][tag]
        else:
            wheel_path = os.path.join(self.main.PATH_WHEELS, tag, tag + ".glb")
            wheel_name = library.io.get_json(path=os.path.join(self.main.PATH_WHEELS,
                                                               tag, self.main.PATH_ITEMS_CONFIG_JSON))["name"]

        self.items["wheels"] = {}

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

        for item in list(self.items):

            if item not in ["chassis", "wheels"]:
                self.unload_part(tag=item)

        bodykit_partlist = [kit["parts"] for kit in self.json["bodykits"] if kit["name"] == bodykit][0]

        for part in bodykit_partlist:
            self.load_part(tag=part)

    def unload(self) -> None:

        logger.debug(f"Unloading car")

        for item in list(self.items):

            if isinstance(self.items[item], dict):
                self.unload_wheels()
            else:
                self.unload_part(tag=item)

        self.path = None
        self.json = None
        self.items = None

    def unload_part(self, tag: str) -> None:

        logger.debug(f"Unloading car part \"{tag}\"")

        self.items[tag].unload_model()

    def unload_wheels(self) -> None:

        logger.debug(f"Unloading car wheels")

        for axle in self.items["wheels"]:
            for wheel in self.items["wheels"][axle]:
                wheel.unload_model()

        self.items["wheels"] = {}

    def get_items(self) -> list:

        items = dict(self.items)
        items["wheels"] = [wheel for axle in items["wheels"] for wheel in items["wheels"][axle]]
        return [items[i] if isinstance(items[i], list) else [items[i]] for i in items]
