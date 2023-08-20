import os
import math

import simplepbr
import panda3d.core
import direct.task.Task
import direct.gui.DirectGui
import direct.showbase.ShowBase

import ui
import car
import ground
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

    PATH_FONTS = os.path.join(PATH_CONTENT, "fonts")
    PATH_FONT_MENU = os.path.join(PATH_FONTS, "gobold/Gobold Regular.otf")

    PATH_CARS = os.path.join(PATH_CONTENT, "cars")
    PATH_CARS_CONFIG = "config.json"
    PATH_CARS_CHASSIS = "chassis.glb"

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

        self.light_on_camera_node = None

        self.ground = ground.Ground(main=self, ground=self.config_json["default"]["ground"])
        self.car = car.Car(main=self, car=self.config_json["default"]["car"])
        self.ui = ui.Menu(main=self, ground=self.ground, car=self.car)

        self.initialize_lights()
        self.initialize_camera()

        self.render.setAntialias(panda3d.core.AntialiasAttrib.MMultisample)

        self.taskMgr.add(self.spin_camera, "SpinCameraTask")

    @staticmethod
    def get_cubemap_path(cubemap):

        current_cubemap_path = os.path.join(Main.PATH_CUBEMAPS, cubemap)

        logger.debug(f"Loading cubemap \"{cubemap}\"")
        return os.path.join(current_cubemap_path,
                            library.io.get_file_path(path=current_cubemap_path,
                                                     extension="env"))

    def initialize_lights(self):

        light_on_camera = direct.showbase.ShowBase.PointLight("CameraLight")
        self.light_on_camera_node = self.render.attachNewNode(light_on_camera)
        light_on_camera.setAttenuation((0, 0, 0.005))
        self.render.setLight(self.light_on_camera_node)

        light_top = direct.showbase.ShowBase.PointLight("TopLight")
        light_top.setAttenuation((0, 0, 0.02))
        light_node_top = self.render.attachNewNode(light_top)
        light_node_top.setPos((0, 0, 7))
        self.render.setLight(light_node_top)

        light_left = direct.showbase.ShowBase.PointLight("LeftLight")
        light_left.setAttenuation((0, 0, 0.001))
        light_node_left = self.render.attachNewNode(light_left)
        light_node_left.setPos((21, 0, 5))
        self.render.setLight(light_node_left)

        light_right = direct.showbase.ShowBase.PointLight("RightLight")
        light_right.setAttenuation((0, 0, 0.001))
        light_node_right = self.render.attachNewNode(light_right)
        light_node_right.setPos((-21, 0, 5))
        self.render.setLight(light_node_right)

        light_front = direct.showbase.ShowBase.PointLight("FrontLight")
        light_front.setAttenuation((0, 0, 0.004))
        light_node_front = self.render.attachNewNode(light_front)
        light_node_front.setPos((0, -12, 6))
        self.render.setLight(light_node_front)

        light_rear = direct.showbase.ShowBase.PointLight("RearLight")
        light_rear.setAttenuation((0, 0, 0.006))
        light_node_rear = self.render.attachNewNode(light_rear)
        light_node_rear.setPos((0, 12, 6))
        self.render.setLight(light_node_rear)

        self.ground.get_ground_model().setLight(light_node_top)

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
