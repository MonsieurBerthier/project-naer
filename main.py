import math
import simplepbr
import panda3d.core
import direct.task.Task
import direct.showbase.ShowBase

from config.logger import logger

panda3d.core.loadPrcFile("config/debug.prc")

# TODO Correct the way mate material are displayed: without spec, relfections, ...
# TODO Find a way to change an object color material from Python
# TODO Fix the shadow under the car: could be forced in image


class Main(direct.showbase.ShowBase.ShowBase):

    def __init__(self):

        super().__init__(self)
        simplepbr.init(use_330=True, env_map="content/cubemaps/lightbars/lightbars.env")

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

        self.initialize_ground()
        self.initialize_car()
        self.initialize_lights()
        self.initialize_camera()

        self.render.setAntialias(panda3d.core.AntialiasAttrib.MMultisample)

        self.taskMgr.add(self.spin_camera, "SpinCameraTask")

    def initialize_ground(self):

        self.ground = self.loader.loadModel(modelPath="content/grounds/concrete/concrete.glb")
        self.ground.reparentTo(self.render)
        self.ground.setScale(1, 1, 1)

    def initialize_car(self):

        self.car = self.loader.loadModel(modelPath="content/cars/nissan_rs13/notexture.glb")
        self.car.reparentTo(self.render)
        self.car.setScale(300, 300, 300)
        self.car.setPos((0, 0, -0.05))

    def initialize_lights(self):

        self.light_on_camera = direct.showbase.ShowBase.PointLight("PointLightCamera")
        self.light_on_camera.setColor((1, 1, 1, 1))
        self.light_on_camera_node = self.render.attachNewNode(self.light_on_camera)
        self.light_on_camera.setAttenuation((0, 0, 0.005))
        self.render.setLight(self.light_on_camera_node)

        self.light_top = direct.showbase.ShowBase.PointLight("TopLight")
        self.light_top.setColor((1, 1, 1, 1))
        self.light_top.setAttenuation((0, 0, 0.02))
        self.light_node_top = self.render.attachNewNode(self.light_top)
        self.light_node_top.setPos((0, 0, 7))
        self.render.setLight(self.light_node_top)

        self.light_left = direct.showbase.ShowBase.PointLight("PointLight1")
        self.light_left.setColor((1, 1, 1, 1))
        self.light_left.setAttenuation((0, 0, 0.02))
        self.light_node_left = self.render.attachNewNode(self.light_left)
        self.light_node_left.setPos((10, 0, 5))
        self.render.setLight(self.light_node_left)

        self.light_right = direct.showbase.ShowBase.PointLight("PointLight1")
        self.light_right.setColor((1, 1, 1, 1))
        self.light_right.setAttenuation((0, 0, 0.02))
        self.light_node_right = self.render.attachNewNode(self.light_right)
        self.light_node_right.setPos((-10, 0, 5))
        self.render.setLight(self.light_node_right)

        self.light_front = direct.showbase.ShowBase.PointLight("PointLight1")
        self.light_front.setColor((1, 1, 1, 1))
        self.light_front.setAttenuation((0, 0, 0.04))
        self.light_node_front = self.render.attachNewNode(self.light_front)
        self.light_node_front.setPos((0, -12, 2.5))
        self.render.setLight(self.light_node_front)

        self.light_rear = direct.showbase.ShowBase.PointLight("PointLight1")
        self.light_rear.setColor((1, 1, 1, 1))
        self.light_rear.setAttenuation((0, 0, 0.04))
        self.light_node_rear = self.render.attachNewNode(self.light_rear)
        self.light_node_rear.setPos((0, 12, 5))
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
