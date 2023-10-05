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


class Main(direct.showbase.ShowBase.ShowBase):

    PATH_CONFIG = "config"
    PATH_CONFIG_JSON = os.path.join(PATH_CONFIG, "config.json")

    PATH_CONTENT = "content"
    PATH_GROUNDS = os.path.join(PATH_CONTENT, "grounds")
    PATH_CUBEMAPS = os.path.join(PATH_CONTENT, "cubemaps")

    PATH_FONTS = os.path.join(PATH_CONTENT, "fonts")
    PATH_FONT_MENU = os.path.join(PATH_FONTS, "gobold/Gobold Regular.otf")

    PATH_CARS = os.path.join(PATH_CONTENT, "cars")
    PATH_CARS_CHASSIS = "chassis.glb"

    PATH_WHEELS = os.path.join(PATH_CONTENT, "wheels")

    PATH_ITEMS_CONFIG_JSON = "config.json"

    def __init__(self) -> None:

        self.config_json = library.io.get_json(path=Main.PATH_CONFIG_JSON)

        super().__init__(self)
        simplepbr.init(env_map=self.get_cubemap_path(cubemap=self.config_json["defaults"]["cubemap"]),
                       use_occlusion_maps=True,
                       use_emission_maps=True,
                       use_normal_maps=True,
                       enable_shadows=True,
                       use_330=True)

        self.autorotate = True
        self.window_resolution = (self.win.getXSize(), self.win.getYSize())
        self.light_on_camera_node = None
        self.light_shadow_node = None
        self.light_top_node = None

        self.ground = ground.Ground(main=self)
        self.car = car.Car(main=self)
        self.font = self.loader.loadFont(self.PATH_FONT_MENU)
        self.ui = ui.UI(main=self)

        self.initialize_lights()
        self.initialize_camera()

        self.render.setAntialias(panda3d.core.AntialiasAttrib.MMultisample)

        self.taskMgr.add(self.spin_camera, "SpinCameraTask")

    @staticmethod
    def get_cubemap_path(cubemap) -> str:

        current_cubemap_path = os.path.join(Main.PATH_CUBEMAPS, cubemap)

        logger.debug(f"Loading cubemap \"{cubemap}\"")
        return os.path.join(current_cubemap_path,
                            library.io.get_file_path(path=current_cubemap_path,
                                                     extension="env"))

    def initialize_lights(self) -> None:

        light_on_camera = direct.showbase.ShowBase.PointLight("CameraLight")
        self.light_on_camera_node = self.render.attachNewNode(light_on_camera)
        light_on_camera.setAttenuation((0, 0, 0.005))
        self.render.setLight(self.light_on_camera_node)

        light_top = direct.showbase.ShowBase.PointLight("TopLight")
        light_top.setAttenuation((0, 0, 0.06))
        self.light_top_node = self.render.attachNewNode(light_top)
        self.light_top_node.setPos((0, 0, 7))
        self.render.setLight(self.light_top_node)
        self.ground.set_light(light=self.light_top_node)

        # To avoid Shadow Acne on ground textures on which shadows are projected :
        #    Blender > Material > Settings > Check "Backface culling"
        light_shadow = direct.showbase.ShowBase.Spotlight("ShadowLight")
        light_shadow.setAttenuation((0, 0, 0.035))
        light_shadow.set_shadow_caster(True, 1024, 1024)
        light_shadow_lens = direct.showbase.ShowBase.PerspectiveLens(160, 160)
        light_shadow.setLens(light_shadow_lens)
        self.light_shadow_node = self.render.attachNewNode(light_shadow)
        self.light_shadow_node.setPos(0, 1, 12)
        self.light_shadow_node.lookAt(0, 0, 0)
        self.ground.set_light(light=self.light_shadow_node)

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

    def initialize_camera(self) -> None:

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
