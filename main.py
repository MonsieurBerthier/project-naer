import math
import os.path

import simplepbr
import panda3d.core
import direct.task.Task
import direct.showbase.ShowBase

import library.io

from config.logger import logger

panda3d.core.loadPrcFile("config/debug.prc")

# TODO Find a way to change an object color material from Python
# TODO Fix the shadow under the car: could be forced in image


class Main(direct.showbase.ShowBase.ShowBase):

    PATH_CONFIG = "config"
    PATH_CONFIG_JSON = os.path.join(PATH_CONFIG, "config.json")
    PATH_CONTENT = "content"
    PATH_GROUNDS = os.path.join(PATH_CONTENT, "grounds")
    PATH_CUBEMAPS = os.path.join(PATH_CONTENT, "cubemaps")
    PATH_CARS = os.path.join(PATH_CONTENT, "cars")
    PATH_WHEELS = os.path.join(PATH_CONTENT, "wheels")

    def __init__(self):

        self.config_json = library.io.get_json(path=Main.PATH_CONFIG_JSON)

        super().__init__(self)
        simplepbr.init(env_map=self.get_cubemap_path(cubemap=self.config_json["default"]["cubemap"]),
                       use_occlusion_maps=True,
                       use_emission_maps=True,
                       use_normal_maps=True,
                       enable_shadows=True,
                       use_330=True)

        self.light_on_camera = None
        self.light_on_camera_node = None
        self.light_top = None
        self.light_left = None
        self.light_right = None
        self.light_front = None
        self.light_rear = None
        self.light_node_top = None
        self.light_node_left = None
        self.light_node_right = None
        self.light_node_front = None
        self.light_node_rear = None
        self.ground = None
        self.car = None

        self.initialize_ground(ground=self.config_json["default"]["ground"])
        self.initialize_car(car=self.config_json["default"]["car"])
        self.initialize_lights()
        self.initialize_camera()

        self.render.setAntialias(panda3d.core.AntialiasAttrib.MMultisample)

        self.taskMgr.add(self.spin_camera, "SpinCameraTask")

    @staticmethod
    def get_cubemap_path(cubemap):

        current_cubemap_path = os.path.join(Main.PATH_CUBEMAPS, cubemap)

        return os.path.join(current_cubemap_path,
                            library.io.get_file_path(path=current_cubemap_path,
                                                     extension="env"))

    def initialize_ground(self, ground):

        current_ground_path = os.path.join(Main.PATH_GROUNDS, ground)
        ground_glb = library.io.get_file_path(path=current_ground_path, extension="glb")

        self.ground = self.loader.loadModel(modelPath=os.path.join(current_ground_path, ground_glb))
        self.ground.reparentTo(self.render)

    def initialize_car(self, car):

        car_path = os.path.join(Main.PATH_CARS, car)
        car_json = library.io.get_json(path=os.path.join(car_path, "config.json"))
        car_chassis = library.io.get_file_path(path=car_path, extension="glb")

        logger.debug(f"Loading car {car_json['name']}")
        self.car = self.loader.loadModel(modelPath=os.path.join(car_path, car_chassis))
        self.car.reparentTo(self.render)
        self.car.setPos(tuple(car_json["chassis"]["position"]))
        self.car.setHpr(tuple(car_json["chassis"]["rotation"]))
        self.car.setScale(tuple(car_json["chassis"]["scale"]))

        # FIXME Use default wheels provided with the car instead
        wheels_json = library.io.get_json(path="content/wheels/japanracing_jr3/config.json")
        for wheel in car_json["wheels"]:
            logger.debug(f"Loading wheel {wheels_json['name']}")
            wheel_x = self.loader.loadModel(modelPath="content/wheels/japanracing_jr3/model.glb")
            wheel_x.setPos(tuple([a + b for a, b in zip(wheel["position"], wheels_json["position"])]))
            wheel_x.setHpr(tuple([a + b for a, b in zip(wheel["rotation"], wheels_json["rotation"])]))
            wheel_x.setScale(tuple([a * b for a, b in zip(wheel["scale"], wheels_json["scale"])]))
            wheel_x.reparentTo(self.render)

    def initialize_lights(self):

        self.light_on_camera = direct.showbase.ShowBase.PointLight("CameraLight")
        self.light_on_camera_node = self.render.attachNewNode(self.light_on_camera)
        self.light_on_camera.setAttenuation((0, 0, 0.005))
        self.render.setLight(self.light_on_camera_node)

        self.light_top = direct.showbase.ShowBase.PointLight("TopLight")
        self.light_top.setAttenuation((0, 0, 0.02))
        self.light_node_top = self.render.attachNewNode(self.light_top)
        self.light_node_top.setPos((0, 0, 7))
        self.render.setLight(self.light_node_top)

        self.light_left = direct.showbase.ShowBase.PointLight("LeftLight")
        self.light_left.setAttenuation((0, 0, 0.001))
        self.light_node_left = self.render.attachNewNode(self.light_left)
        self.light_node_left.setPos((21, 0, 5))
        self.render.setLight(self.light_node_left)

        self.light_right = direct.showbase.ShowBase.PointLight("RightLight")
        self.light_right.setAttenuation((0, 0, 0.001))
        self.light_node_right = self.render.attachNewNode(self.light_right)
        self.light_node_right.setPos((-21, 0, 5))
        self.render.setLight(self.light_node_right)

        self.light_front = direct.showbase.ShowBase.PointLight("FrontLight")
        self.light_front.setAttenuation((0, 0, 0.004))
        self.light_node_front = self.render.attachNewNode(self.light_front)
        self.light_node_front.setPos((0, -12, 6))
        self.render.setLight(self.light_node_front)

        self.light_rear = direct.showbase.ShowBase.PointLight("RearLight")
        self.light_rear.setAttenuation((0, 0, 0.006))
        self.light_node_rear = self.render.attachNewNode(self.light_rear)
        self.light_node_rear.setPos((0, 12, 6))
        self.render.setLight(self.light_node_rear)

        self.ground.setLightOff()
        self.ground.setLight(self.light_node_top)

    def initialize_camera(self):

        self.cam.setPos(0, -4, 1.5)
        self.cam.lookAt((0, 0, 1.1))

    def spin_camera(self, task):

        angle_degrees = task.time * 30.0
        angle_radians = angle_degrees * (math.pi / 180.0)

        self.camera.setPos(20 * math.sin(angle_radians), -20 * math.cos(angle_radians), 3)
        self.camera.setHpr(angle_degrees, 0, 0)
        self.light_on_camera_node.setPos(self.camera.getPos())

        return direct.task.Task.cont


main = Main()
main.run()
