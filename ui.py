import os
import sys
import enum
import logging
import datetime

import autologging

import direct.gui.DirectGui

from config.logger import logger

logging.basicConfig(level=autologging.TRACE, stream=sys.stderr,
                    format=f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} "
                           f"| %(levelname)s | %(name)s.%(funcName)s@%(lineno)d : :%(message)s")


MARGIN = 16
GREY = (0.2, 0.2, 0.2, 1)
RED = (1, 0, 0, 1)
WHITE = (1, 1, 1, 1)
TRANSPARENT = (0, 0, 0, 0)
FONT_SIZE = 20
BUTTON_Y_SIZE = 32
MAIN_BUTTON_BAR_Y_SIZE = 4
SUBMENU_BUTTON_X_SIZE = [140, 280, 280, 280]
SUBMENU_BUTTON_Y_POSITIONS = [MARGIN,
                              MARGIN + BUTTON_Y_SIZE,
                              MARGIN + (2 * BUTTON_Y_SIZE),
                              MARGIN + (3 * BUTTON_Y_SIZE),
                              MARGIN + (4 * BUTTON_Y_SIZE),
                              MARGIN + (5 * BUTTON_Y_SIZE),
                              MARGIN + (6 * BUTTON_Y_SIZE),
                              MARGIN + (7 * BUTTON_Y_SIZE)]
TEXT_PADDING_LEFT = 20


class SUBMENU_0_BUTTON_TEXT(enum.Enum):
    CARS = "Cars"
    WHEELS = "Wheels"
    GROUNDS = "Grounds"
    SAVE_CAR = "Save Car"
    LOAD_CAR = "Load Car"
    SAVE_IMAGE = "Save Image"
    AUTOROTATE = "Autorotate"
    EXIT = "Exit"


class TEXT_JUSTIFY(enum.Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2


@autologging.traced()
class MainButton:

    def __init__(self, main, position_x: int, position_y: int) -> None:

        self.main = main
        self.position_x = position_x
        self.position_y = position_y
        self.keep_activate = False

        self.background = (
            direct.gui.DirectGui.DirectFrame(frameColor=TRANSPARENT,
                                             frameSize=(0, BUTTON_Y_SIZE, 0, -BUTTON_Y_SIZE),
                                             pos=(MARGIN, 0, -MARGIN),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))

        self.line_top = (
            direct.gui.DirectGui.DirectFrame(frameColor=WHITE,
                                             frameSize=(0, BUTTON_Y_SIZE, 0, -MAIN_BUTTON_BAR_Y_SIZE),
                                             pos=(MARGIN, 0, -MARGIN),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))

        self.line_mid = (
            direct.gui.DirectGui.DirectFrame(frameColor=WHITE,
                                             frameSize=(0, BUTTON_Y_SIZE, 0, -MAIN_BUTTON_BAR_Y_SIZE),
                                             pos=(MARGIN, 0, - (BUTTON_Y_SIZE / 2) - MARGIN +
                                                  (MAIN_BUTTON_BAR_Y_SIZE / 2)),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))

        self.line_bot = (
            direct.gui.DirectGui.DirectFrame(frameColor=WHITE,
                                             frameSize=(0, BUTTON_Y_SIZE, 0, -MAIN_BUTTON_BAR_Y_SIZE),
                                             pos=(MARGIN, 0, - BUTTON_Y_SIZE - MARGIN + MAIN_BUTTON_BAR_Y_SIZE),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))

        # REMINDER  frameSize=(1, 2, 3, 4)  (left, right, bottom, top)
        # REMINDER  setPos(1, 0, 2)         (horizontal, 0, vertical)


@autologging.traced()
class MenuButton:

    def __init__(self, main, position_x: int, position_y: int, text: str, font, menu_x_size: int) -> None:

        self.frame = direct.gui.DirectGui.DirectFrame(frameColor=RED,
                                                      text=text,
                                                      text_fg=WHITE,
                                                      text_font=font,
                                                      text_scale=FONT_SIZE,
                                                      text_align=TEXT_JUSTIFY.LEFT.value,
                                                      text_pos=(TEXT_PADDING_LEFT, -BUTTON_Y_SIZE + 7, 0),
                                                      frameSize=(0, menu_x_size, 0, -BUTTON_Y_SIZE),
                                                      pos=(position_x, 0, -position_y),
                                                      state=direct.gui.DirectGui.DGG.NORMAL,
                                                      parent=main.pixel2d)
        self.frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                        command=self.set_button_mouseover)
        self.frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                        command=self.set_button_mouseout)

    def set_button_mouseover(self, _):
        self.frame.setColor(WHITE)
        self.frame["text_fg"] = GREY

    def set_button_mouseout(self, _):
        self.frame.setColor(RED)
        self.frame["text_fg"] = WHITE


@autologging.traced()
class MainMenu:

    button = None
    close = None
    menus = []

    def __init__(self, main, ground, car) -> None:

        self.main = main
        self.ground = ground
        self.car = car

        self.font = self.main.loader.loadFont(self.main.PATH_FONT_MENU)  # FIXME Avoid to reload the font x times

        self.button = MainButton(main=self.main, position_x=MARGIN, position_y=MARGIN)
        self.button.background.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                    command=self.create_new_submenu,
                                    extraArgs=[self.get_new_submenu_level(),
                                               [t.value for t in SUBMENU_0_BUTTON_TEXT]])

    def get_new_submenu_level(self):

        return len(self.menus)

    def create_new_submenu(self, level, items, trash):

        if level == 0:
            self.button.background.setColor(WHITE)
            self.close = direct.gui.DirectGui.DirectFrame(frameColor=TRANSPARENT,
                                                          frameSize=(0, 1920, 0, -1080),
                                                          # FIXME Use windows resolution instead
                                                          pos=(0, 0, 0),
                                                          state=direct.gui.DirectGui.DGG.NORMAL,
                                                          parent=self.main.pixel2d)
            self.close.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                            command=self.callback_close_mainmenu)
            self.close_submenu(level=1)

        if level != 0:
            items = sorted(items)

        if len(self.menus) >= level:
            self.close_submenu(level=level)

        buttons = []
        for i in range(len(items)):

            button = MenuButton(main=self.main,
                                position_x=MARGIN + BUTTON_Y_SIZE + sum(SUBMENU_BUTTON_X_SIZE[:level]),
                                position_y=SUBMENU_BUTTON_Y_POSITIONS[i],
                                text=items[i],
                                font=self.font,
                                menu_x_size=SUBMENU_BUTTON_X_SIZE[level])
            button.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                              command=self.clic_on_button,
                              extraArgs=[button])
            buttons.append(button)

        self.menus.append(buttons)

    def clic_on_button(self, button, trash):

        logger.debug(f"Button \"{button.frame['text']}\" clicked")

        if button.frame['text'] == SUBMENU_0_BUTTON_TEXT.CARS.value:

            cars_list = os.listdir(self.main.PATH_CARS)
            self.create_new_submenu(level=1, items=cars_list, trash=trash)

        elif button.frame['text'] == SUBMENU_0_BUTTON_TEXT.WHEELS.value:

            wheels_list = os.listdir(self.main.PATH_WHEELS)
            self.create_new_submenu(level=1, items=wheels_list, trash=trash)

        elif button.frame['text'] == SUBMENU_0_BUTTON_TEXT.GROUNDS.value:

            grounds_list = os.listdir(self.main.PATH_GROUNDS)
            self.create_new_submenu(level=1, items=grounds_list, trash=trash)

        elif button.frame['text'] == SUBMENU_0_BUTTON_TEXT.EXIT.value:

            sys.exit()

    def callback_close_mainmenu(self, _):

        self.close_submenu(level=0)
        self.button.background.setColor(TRANSPARENT)
        self.close.destroy()

    def close_submenu(self, level):

        for menu in self.menus[level:]:
            for button in menu:
                button.frame.destroy()

        self.menus = self.menus[:level]
