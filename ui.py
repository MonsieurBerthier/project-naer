import direct.gui.DirectGui

from config.logger import logger


MARGIN = 16
GREY = (0.2, 0.2, 0.2, 1)
RED = (1, 0, 0, 1)
WHITE = (1, 1, 1, 1)
TRANSPARENT = (0, 0, 0, 0)
FONT_SIZE = 20
BUTTON_Y_SIZE = 32
MAIN_BUTTON_BAR_Y_SIZE = 4
SUBMENU1_MENU_BUTTON_X_SIZE = 140
SUBMENU1_BUTTON_Y_POSITIONS = [MARGIN,
                               MARGIN + BUTTON_Y_SIZE,
                               MARGIN + (2 * BUTTON_Y_SIZE),
                               MARGIN + (3 * BUTTON_Y_SIZE),
                               MARGIN + (4 * BUTTON_Y_SIZE),
                               MARGIN + (5 * BUTTON_Y_SIZE),
                               MARGIN + (6 * BUTTON_Y_SIZE)]
SUBMENU2_MENU_BUTTON_X_SIZE_ = 280
TEXT_PADDING_LEFT = 20


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


class MenuButton:

    def __init__(self, main, position_x: int, position_y: int, text: str, font) -> None:

        self.frame = direct.gui.DirectGui.DirectFrame(frameColor=RED,
                                                      text=text,
                                                      text_fg=WHITE,
                                                      text_font=font,
                                                      text_scale=FONT_SIZE,
                                                      text_pos=(position_x + TEXT_PADDING_LEFT, -BUTTON_Y_SIZE + 7, 0),
                                                      frameSize=(0, SUBMENU1_MENU_BUTTON_X_SIZE, 0, -BUTTON_Y_SIZE),
                                                      pos=(position_x, 0, -position_y),
                                                      state=direct.gui.DirectGui.DGG.NORMAL,
                                                      parent=main.pixel2d)


class MainMenu:

    def __init__(self, main, ground, car) -> None:

        self.main = main
        self.ground = ground
        self.car = car

        self.font = self.main.loader.loadFont(self.main.PATH_FONT_MENU)

        self.main_button = MainButton(main=self.main, position_x=MARGIN, position_y=MARGIN)
        self.main_button.background.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                         command=self.event_main_button_in)

        self.menu_1 = []

    def event_main_button_in(self, _):

        self.main_button.background.setColor(WHITE)
        submenu1 = ["Grounds", "Cars", "Wheels", "Save Car", "Load Car", "Save Image", "Exit"]

        for i in range(len(submenu1)):

            button = MenuButton(main=self.main,
                                position_x=MARGIN + BUTTON_Y_SIZE,
                                position_y=SUBMENU1_BUTTON_Y_POSITIONS[i],
                                text=submenu1[i],
                                font=self.font)
            button.frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                              command=self.event_cursor_in,
                              extraArgs=[button])
            button.frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                              command=self.event_cursor_out,
                              extraArgs=[button])
            self.menu_1.append(button)

    def event_cursor_in(self, button, _):

        button.frame.setColor(WHITE)
        button.frame["text_fg"] = GREY

    def event_cursor_out(self, button, _):

        button.frame.setColor(RED)
        button.frame["text_fg"] = WHITE
