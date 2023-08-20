import direct.gui.DirectGui

from config.logger import logger


MARGIN = 16
BUTTON_Y_SIZE = 32
BUTTON_BAR_Y_SIZE = 4
BLACK = (0, 0, 0, 1)
GREY = (0.2, 0.2, 0.2, 1)
RED = (1, 0, 0, 1)
WHITE = (1, 1, 1, 1)
TRANSPARENT = (0, 0, 0, 0)


class MainMenu:

    def __init__(self, main, ground, car) -> None:

        self._main = main
        self._ground = ground
        self._car = car

        self._window_resolution = (self._main.win.getXSize(), self._main.win.getYSize())
        self._window_ratio = self._window_resolution[0] / self._window_resolution[1]
        self.font_menu = self._main.loader.loadFont(self._main.PATH_FONT_MENU)

        self._button_main = (
            direct.gui.DirectGui.DirectFrame(frameColor=TRANSPARENT,
                                             frameSize=(0, BUTTON_Y_SIZE, 0, -BUTTON_Y_SIZE),
                                             pos=(MARGIN, 0, -MARGIN),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self._main.pixel2d))

        self._button_main_line_1 = (
            direct.gui.DirectGui.DirectFrame(frameColor=WHITE,
                                             frameSize=(0, BUTTON_Y_SIZE, 0, -BUTTON_BAR_Y_SIZE),
                                             pos=(MARGIN, 0, -MARGIN),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self._main.pixel2d))

        self._button_main_line_2 = (
            direct.gui.DirectGui.DirectFrame(frameColor=WHITE,
                                             frameSize=(0, BUTTON_Y_SIZE, 0, -BUTTON_BAR_Y_SIZE),
                                             pos=(MARGIN, 0, - (BUTTON_Y_SIZE / 2) - MARGIN + (BUTTON_BAR_Y_SIZE / 2)),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self._main.pixel2d))

        self._button_main_line_3 = (
            direct.gui.DirectGui.DirectFrame(frameColor=WHITE,
                                             frameSize=(0, BUTTON_Y_SIZE, 0, -BUTTON_BAR_Y_SIZE),
                                             pos=(MARGIN, 0, - BUTTON_Y_SIZE - MARGIN + BUTTON_BAR_Y_SIZE),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self._main.pixel2d))

        # TODO frameSize=(1, 2, 3, 4)  # (left, right, bottom, top)
        # TODO setPos(1, 0, 2)         # (horizontal, 0, vertical)

        self._button_main.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                               command=self.toto,
                               extraArgs=[self._button_main, "in"])
        self._button_main.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                               command=self.toto,
                               extraArgs=[self._button_main, "out"])

    def toto(self, a, b, _):

        if b == "in":
            a.setColor(RED)
        else:
            a.setColor(TRANSPARENT)
