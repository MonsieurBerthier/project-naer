import os
import sys

import direct.gui.DirectGui

import library.io

from config.logger import logger


class Base:

    MARGIN = 16
    BUTTON_Y_SIZE = 32

    GREY = (0.2, 0.2, 0.2, 1)
    RED = (1, 0, 0, 1)
    WHITE = (1, 1, 1, 1)
    TRANSPARENT = (0, 0, 0, 0)

    TEXT_JUSTIFY_LEFT = 0
    TEXT_JUSTIFY_RIGHT = 1
    TEXT_JUSTIFY_CENTER = 2

    @staticmethod
    def get_button_y_position(index: int) -> int:

        return -Base.MARGIN - (index * Base.BUTTON_Y_SIZE)


class MenuButton:

    def __init__(self, main, text: str, font, position_x: int, position_y: int, size_x: int, size_y: int,
                 auto_event: bool, icon_mouseover: str, icon_mouseout: str) -> None:

        self.auto_event = auto_event
        self.icon_mouseover = icon_mouseover
        self.icon_mouseout = icon_mouseout

        self.frame = direct.gui.DirectGui.DirectFrame(frameColor=Base.RED,
                                                      text=text,
                                                      text_fg=Base.WHITE,
                                                      text_font=font,
                                                      text_scale=MainMenu.FONT_SIZE,
                                                      text_align=Base.TEXT_JUSTIFY_LEFT,
                                                      text_pos=(MainMenu.TEXT_PADDING_LEFT,
                                                                -Base.BUTTON_Y_SIZE + 7, 0),
                                                      frameSize=(0, size_x, 0, size_y),
                                                      pos=(position_x, 0, -position_y),
                                                      state=direct.gui.DirectGui.DGG.NORMAL,
                                                      parent=main.pixel2d,
                                                      image=self.icon_mouseout,
                                                      image_scale=(16, 0, 11),  # FIXME
                                                      image_pos=(25, 0, -16))   # FIXME

        if self.auto_event:
            self.frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                            command=self.set_button_mouseover_style)
            self.frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                            command=self.set_button_mouseout_style)

    def set_button_mouseover_style(self, _) -> None:

        self.frame["frameColor"] = Base.WHITE
        self.frame["text_fg"] = Base.GREY
        self.frame["image"] = self.icon_mouseover

    def set_button_mouseout_style(self, _) -> None:

        self.frame["frameColor"] = Base.RED
        self.frame["text_fg"] = Base.WHITE
        self.frame["image"] = self.icon_mouseout


class SubMenu:

    def __init__(self, main, folder: str, x_size: int, icon_mouseover: str, icon_mouseout: str) -> None:

        self.main = main
        self.folder = folder
        self.menu_x_size = x_size
        self.icon_mouseover = icon_mouseover
        self.icon_mouseout = icon_mouseout

        self.buttons = []

    def open(self, content_path: str) -> None:

        items = []
        for folder in os.listdir(self.folder):
            path_to_json = os.path.join(content_path, folder, self.main.PATH_ITEMS_CONFIG_JSON)
            json = library.io.get_json(path=path_to_json)
            items.append([folder, json["name"]])

        items = sorted(items, key=lambda x: x[1])

        for i in range(len(items)):
            button = MenuButton(main=self.main,
                                text=items[i][1], font=self.main.font,
                                position_x=Base.MARGIN + Base.BUTTON_Y_SIZE + MainMenu.MAIN_MENU_X_SIZE,
                                position_y=-Base.get_button_y_position(index=i),
                                size_x=self.menu_x_size, size_y=-Base.BUTTON_Y_SIZE,
                                auto_event=True,
                                icon_mouseover=self.icon_mouseover,
                                icon_mouseout=self.icon_mouseout)

            if MainMenu.TEXT_CARS.lower() in content_path:
                button.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                  command=self.callback_load_car,
                                  extraArgs=[items[i][0]])
            elif MainMenu.TEXT_WHEELS.lower() in content_path:
                button.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                  command=self.callback_load_wheels,
                                  extraArgs=[items[i][0]])
            elif MainMenu.TEXT_GROUNDS.lower() in content_path:
                button.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                  command=self.callback_load_ground,
                                  extraArgs=[items[i][0]])
            self.buttons.append(button)

    def callback_load_car(self, name, _) -> None:

        self.main.car.load(name=name)

    def callback_load_wheels(self, name, _) -> None:

        self.main.car.load_wheels(name=name, oem=False)

    def callback_load_ground(self, name, _) -> None:

        self.main.ground.change(name=name)

    def close(self) -> None:

        for button in self.buttons:
            button.frame.destroy()
        self.buttons = []


class MainMenu:

    FONT_SIZE = 20
    TEXT_PADDING_LEFT = 50

    MAIN_BUTTON_BAR_Y_SIZE = 4
    MAIN_MENU_X_SIZE = 200
    CARS_MENU_X_SIZE = 300
    GROUNDS_MENU_X_SIZE = 200
    WHEELS_MENU_X_SIZE = 300

    TEXT_CARS = "Cars"
    TEXT_WHEELS = "Wheels"
    TEXT_GROUNDS = "Grounds"
    TEXT_GARAGE = "Garage"
    TEXT_BODY_SHOP = "Body Shop"
    TEXT_SAVE_CAR = "Save Car"
    TEXT_LOAD_CAR = "Load Car"
    TEXT_SAVE_IMAGE = "Save Image"
    TEXT_AUTOROTATE = "Autorotate"
    TEXT_EXIT = "Exit"

    ICON_CARS_MOUSEOVER = "content/images/ui/menu/icon_cars_mouseover.png"
    ICON_CARS_MOUSEOUT = "content/images/ui/menu/icon_cars_mouseout.png"
    ICON_CAR_MOUSEOVER = "content/images/ui/menu/icon_car_mouseover.png"
    ICON_CAR_MOUSEOUT = "content/images/ui/menu/icon_car_mouseout.png"
    ICON_WHEELS_MOUSEOVER = "content/images/ui/menu/icon_wheels_mouseover.png"
    ICON_WHEELS_MOUSEOUT = "content/images/ui/menu/icon_wheels_mouseout.png"
    ICON_WHEEL_MOUSEOVER = "content/images/ui/menu/icon_wheel_mouseover.png"
    ICON_WHEEL_MOUSEOUT = "content/images/ui/menu/icon_wheel_mouseout.png"
    ICON_GROUNDS_MOUSEOVER = "content/images/ui/menu/icon_grounds_mouseover.png"
    ICON_GROUNDS_MOUSEOUT = "content/images/ui/menu/icon_grounds_mouseout.png"
    ICON_GROUND_MOUSEOVER = "content/images/ui/menu/icon_ground_mouseover.png"
    ICON_GROUND_MOUSEOUT = "content/images/ui/menu/icon_ground_mouseout.png"
    ICON_GARAGE_MOUSEOVER = "content/images/ui/menu/icon_garage_mouseover.png"
    ICON_GARAGE_MOUSEOUT = "content/images/ui/menu/icon_garage_mouseout.png"
    ICON_BODY_SHOP_MOUSEOVER = "content/images/ui/menu/icon_bodyshop_mouseover.png"
    ICON_BODY_SHOP_MOUSEOUT = "content/images/ui/menu/icon_bodyshop_mouseout.png"
    ICON_SAVE_CAR_MOUSEOVER = "content/images/ui/menu/icon_savecar_mouseover.png"
    ICON_SAVE_CAR_MOUSEOUT = "content/images/ui/menu/icon_savecar_mouseout.png"
    ICON_LOAD_CAR_MOUSEOVER = "content/images/ui/menu/icon_loadcar_mouseover.png"
    ICON_LOAD_CAR_MOUSEOUT = "content/images/ui/menu/icon_loadcar_mouseout.png"
    ICON_SAVE_IMAGE_MOUSEOVER = "content/images/ui/menu/icon_saveimage_mouseover.png"
    ICON_SAVE_IMAGE_MOUSEOUT = "content/images/ui/menu/icon_saveimage_mouseout.png"
    ICON_AUTOROTATE_ON_MOUSEOVER = "content/images/ui/menu/icon_autorotateon_mouseover.png"
    ICON_AUTOROTATE_ON_MOUSEOUT = "content/images/ui/menu/icon_autorotateon_mouseout.png"
    ICON_AUTOROTATE_OFF_MOUSEOVER = "content/images/ui/menu/icon_autorotateoff_mouseover.png"
    ICON_AUTOROTATE_OFF_MOUSEOUT = "content/images/ui/menu/icon_autorotateoff_mouseout.png"
    ICON_EXIT_MOUSEOVER = "content/images/ui/menu/icon_exit_mouseover.png"
    ICON_EXIT_MOUSEOUT = "content/images/ui/menu/icon_exit_mouseout.png"

    def __init__(self, main) -> None:

        self.main = main

        self.open_button = {}
        self.close_button = None
        self.menu_buttons = {}

        self.submenu_cars = SubMenu(main=self.main,
                                    folder=self.main.PATH_CARS,
                                    x_size=MainMenu.CARS_MENU_X_SIZE,
                                    icon_mouseover=MainMenu.ICON_CAR_MOUSEOVER,
                                    icon_mouseout=MainMenu.ICON_CAR_MOUSEOUT)
        self.submenu_wheels = SubMenu(main=self.main,
                                      folder=self.main.PATH_WHEELS,
                                      x_size=MainMenu.WHEELS_MENU_X_SIZE,
                                      icon_mouseover=MainMenu.ICON_WHEEL_MOUSEOVER,
                                      icon_mouseout=MainMenu.ICON_WHEEL_MOUSEOUT)
        self.submenu_grounds = SubMenu(main=self.main,
                                       folder=self.main.PATH_GROUNDS,
                                       x_size=MainMenu.GROUNDS_MENU_X_SIZE,
                                       icon_mouseover=MainMenu.ICON_GROUND_MOUSEOVER,
                                       icon_mouseout=MainMenu.ICON_GROUND_MOUSEOUT)

        self.open_button["Background"] = (
            direct.gui.DirectGui.DirectFrame(frameColor=Base.TRANSPARENT,
                                             frameSize=(0, Base.BUTTON_Y_SIZE, 0, -Base.BUTTON_Y_SIZE),
                                             pos=(Base.MARGIN, 0, -Base.MARGIN),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))
        self.open_button["TopLine"] = (
            direct.gui.DirectGui.DirectFrame(frameColor=Base.WHITE,
                                             frameSize=(0, Base.BUTTON_Y_SIZE, 0, -MainMenu.MAIN_BUTTON_BAR_Y_SIZE),
                                             pos=(Base.MARGIN, 0, -Base.MARGIN),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))
        self.open_button["MiddleLine"] = (
            direct.gui.DirectGui.DirectFrame(frameColor=Base.WHITE,
                                             frameSize=(0, Base.BUTTON_Y_SIZE, 0, -MainMenu.MAIN_BUTTON_BAR_Y_SIZE),
                                             pos=(Base.MARGIN, 0, - (Base.BUTTON_Y_SIZE / 2) - Base.MARGIN +
                                                  (MainMenu.MAIN_BUTTON_BAR_Y_SIZE / 2)),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))
        self.open_button["BottomLine"] = (
            direct.gui.DirectGui.DirectFrame(frameColor=Base.WHITE,
                                             frameSize=(0, Base.BUTTON_Y_SIZE, 0, -MainMenu.MAIN_BUTTON_BAR_Y_SIZE),
                                             pos=(Base.MARGIN, 0,
                                                  -Base.BUTTON_Y_SIZE - Base.MARGIN + MainMenu.MAIN_BUTTON_BAR_Y_SIZE),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))

        self.open_button["Background"].bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                            command=self.open_main_menu)

    def open_main_menu(self, _) -> None:

        if self.menu_buttons:
            return

        self.open_button["Background"]["frameColor"] = Base.WHITE
        self.close_button = direct.gui.DirectGui.DirectFrame(frameColor=Base.TRANSPARENT,
                                                             frameSize=(0, self.main.window_resolution[0]-5, 0,
                                                                        -self.main.window_resolution[0]+5),
                                                             pos=(0, 0, 0),
                                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                                             parent=self.main.pixel2d)
        self.close_button.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                               command=self.close_main_menu)

        self.menu_buttons[MainMenu.TEXT_CARS] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_CARS, font=self.main.font,
                       position_x=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       position_y=Base.MARGIN,
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-Base.BUTTON_Y_SIZE,
                       auto_event=False,
                       icon_mouseover=MainMenu.ICON_CARS_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_CARS_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_CARS].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                         command=self.open_cars_submenu)

        self.menu_buttons[MainMenu.TEXT_WHEELS] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_WHEELS, font=self.main.font,
                       position_x=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       position_y=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-Base.BUTTON_Y_SIZE,
                       auto_event=False,
                       icon_mouseover=MainMenu.ICON_WHEELS_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_WHEELS_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_WHEELS].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                           command=self.open_wheels_submenu)

        self.menu_buttons[MainMenu.TEXT_GROUNDS] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_GROUNDS, font=self.main.font,
                       position_x=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       position_y=Base.MARGIN + (2 * Base.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-Base.BUTTON_Y_SIZE,
                       auto_event=False,
                       icon_mouseover=MainMenu.ICON_GROUNDS_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_GROUNDS_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                            command=self.open_grounds_submenu)

        self.menu_buttons[MainMenu.TEXT_GARAGE] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_GARAGE, font=self.main.font,
                       position_x=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       position_y=Base.MARGIN + (3 * Base.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-Base.BUTTON_Y_SIZE,
                       auto_event=False,
                       icon_mouseover=MainMenu.ICON_GARAGE_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_GARAGE_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_GARAGE].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                           command=self.set_button_mouseover_style,
                                                           extraArgs=[self.menu_buttons[MainMenu.TEXT_GARAGE]])
        self.menu_buttons[MainMenu.TEXT_GARAGE].frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                                                           command=self.set_button_mouseout_style,
                                                           extraArgs=[self.menu_buttons[MainMenu.TEXT_GARAGE]])
        self.menu_buttons[MainMenu.TEXT_GARAGE].frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                                           command=self.display_garage)

        self.menu_buttons[MainMenu.TEXT_BODY_SHOP] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_BODY_SHOP, font=self.main.font,
                       position_x=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       position_y=Base.MARGIN + (4 * Base.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-Base.BUTTON_Y_SIZE,
                       auto_event=False,
                       icon_mouseover=MainMenu.ICON_BODY_SHOP_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_BODY_SHOP_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_BODY_SHOP].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                              command=self.set_button_mouseover_style,
                                                              extraArgs=[self.menu_buttons[MainMenu.TEXT_BODY_SHOP]])
        self.menu_buttons[MainMenu.TEXT_BODY_SHOP].frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                                                              command=self.set_button_mouseout_style,
                                                              extraArgs=[self.menu_buttons[MainMenu.TEXT_BODY_SHOP]])
        self.menu_buttons[MainMenu.TEXT_BODY_SHOP].frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                                              command=self.display_body_shop)

        self.menu_buttons[MainMenu.TEXT_SAVE_CAR] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_SAVE_CAR, font=self.main.font,
                       position_x=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       position_y=Base.MARGIN + (5 * Base.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-Base.BUTTON_Y_SIZE,
                       auto_event=False,
                       icon_mouseover=MainMenu.ICON_SAVE_CAR_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_SAVE_CAR_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_SAVE_CAR].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                             command=self.set_button_mouseover_style,
                                                             extraArgs=[self.menu_buttons[MainMenu.TEXT_SAVE_CAR]])
        self.menu_buttons[MainMenu.TEXT_SAVE_CAR].frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                                                             command=self.set_button_mouseout_style,
                                                             extraArgs=[self.menu_buttons[MainMenu.TEXT_SAVE_CAR]])
        self.menu_buttons[MainMenu.TEXT_SAVE_CAR].frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                                             command=self.save_car)

        self.menu_buttons[MainMenu.TEXT_LOAD_CAR] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_LOAD_CAR, font=self.main.font,
                       position_x=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       position_y=Base.MARGIN + (6 * Base.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-Base.BUTTON_Y_SIZE,
                       auto_event=False,
                       icon_mouseover=MainMenu.ICON_LOAD_CAR_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_LOAD_CAR_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_LOAD_CAR].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                             command=self.set_button_mouseover_style,
                                                             extraArgs=[self.menu_buttons[MainMenu.TEXT_LOAD_CAR]])
        self.menu_buttons[MainMenu.TEXT_LOAD_CAR].frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                                                             command=self.set_button_mouseout_style,
                                                             extraArgs=[self.menu_buttons[MainMenu.TEXT_LOAD_CAR]])
        self.menu_buttons[MainMenu.TEXT_LOAD_CAR].frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                                             command=self.load)

        self.menu_buttons[MainMenu.TEXT_SAVE_IMAGE] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_SAVE_IMAGE, font=self.main.font,
                       position_x=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       position_y=Base.MARGIN + (7 * Base.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-Base.BUTTON_Y_SIZE,
                       auto_event=False,
                       icon_mouseover=MainMenu.ICON_SAVE_IMAGE_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_SAVE_IMAGE_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_SAVE_IMAGE].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                               command=self.set_button_mouseover_style,
                                                               extraArgs=[self.menu_buttons[MainMenu.TEXT_SAVE_IMAGE]])
        self.menu_buttons[MainMenu.TEXT_SAVE_IMAGE].frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                                                               command=self.set_button_mouseout_style,
                                                               extraArgs=[self.menu_buttons[MainMenu.TEXT_SAVE_IMAGE]])
        self.menu_buttons[MainMenu.TEXT_SAVE_IMAGE].frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                                               command=self.save_image)

        self.menu_buttons[MainMenu.TEXT_AUTOROTATE] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_AUTOROTATE, font=self.main.font,
                       position_x=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       position_y=Base.MARGIN + (8 * Base.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-Base.BUTTON_Y_SIZE,
                       auto_event=False,
                       icon_mouseover=MainMenu.ICON_AUTOROTATE_ON_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_AUTOROTATE_ON_MOUSEOUT))
        self.update_autorotate_icon(b1press=False)
        self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                               command=self.set_button_mouseover_style,
                                                               extraArgs=[self.menu_buttons[MainMenu.TEXT_AUTOROTATE]])
        self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                                                               command=self.set_button_mouseout_style,
                                                               extraArgs=[self.menu_buttons[MainMenu.TEXT_AUTOROTATE]])
        self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                                               command=self.toggle_autorotate)

        self.menu_buttons[MainMenu.TEXT_EXIT] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_EXIT, font=self.main.font,
                       position_x=Base.MARGIN + Base.BUTTON_Y_SIZE,
                       position_y=Base.MARGIN + (9 * Base.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-Base.BUTTON_Y_SIZE,
                       auto_event=False,
                       icon_mouseover=MainMenu.ICON_EXIT_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_EXIT_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_EXIT].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                         command=self.set_button_mouseover_style,
                                                         extraArgs=[self.menu_buttons[MainMenu.TEXT_EXIT]])
        self.menu_buttons[MainMenu.TEXT_EXIT].frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                                                         command=self.set_button_mouseout_style,
                                                         extraArgs=[self.menu_buttons[MainMenu.TEXT_EXIT]])
        self.menu_buttons[MainMenu.TEXT_EXIT].frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                                         command=self.exit)

    def set_button_mouseover_style(self, button, _) -> None:

        self.close_all_submenus()
        button.frame["frameColor"] = Base.WHITE
        button.frame["text_fg"] = Base.GREY
        button.frame["image"] = button.icon_mouseover

    @staticmethod
    def set_button_mouseout_style(button, _) -> None:

        button.frame["frameColor"] = Base.RED
        button.frame["text_fg"] = Base.WHITE
        button.frame["image"] = button.icon_mouseout

    def close_main_menu(self, _) -> None:

        self.close_button.destroy()

        self.close_all_submenus()

        for button in self.menu_buttons:
            self.menu_buttons[button].frame.destroy()
        self.menu_buttons = {}

        self.open_button["Background"]["frameColor"] = Base.TRANSPARENT

    def open_cars_submenu(self, _) -> None:

        self.close_all_submenus()

        self.menu_buttons[MainMenu.TEXT_CARS].frame["frameColor"] = Base.WHITE
        self.menu_buttons[MainMenu.TEXT_CARS].frame["text_fg"] = Base.GREY
        self.menu_buttons[MainMenu.TEXT_CARS].frame["image"] = MainMenu.ICON_CARS_MOUSEOVER

        self.submenu_cars.open(content_path=self.main.PATH_CARS)

    def close_cars_submenu(self, _) -> None:

        self.submenu_cars.close()

        self.menu_buttons[MainMenu.TEXT_CARS].frame["frameColor"] = Base.RED
        self.menu_buttons[MainMenu.TEXT_CARS].frame["text_fg"] = Base.WHITE
        self.menu_buttons[MainMenu.TEXT_CARS].frame["image"] = MainMenu.ICON_CARS_MOUSEOUT

    def open_wheels_submenu(self, _) -> None:

        self.close_all_submenus()

        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["frameColor"] = Base.WHITE
        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["text_fg"] = Base.GREY
        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["image"] = MainMenu.ICON_WHEELS_MOUSEOVER

        self.submenu_wheels.open(content_path=self.main.PATH_WHEELS)

    def close_wheels_submenu(self, _) -> None:

        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["frameColor"] = Base.RED
        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["text_fg"] = Base.WHITE
        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["image"] = MainMenu.ICON_WHEELS_MOUSEOUT

        self.submenu_wheels.close()

    def open_grounds_submenu(self, _) -> None:

        self.close_all_submenus()

        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["frameColor"] = Base.WHITE
        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["text_fg"] = Base.GREY
        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["image"] = MainMenu.ICON_GROUNDS_MOUSEOVER

        self.submenu_grounds.open(content_path=self.main.PATH_GROUNDS)

    def close_grounds_submenu(self, _) -> None:

        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["frameColor"] = Base.RED
        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["text_fg"] = Base.WHITE
        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["image"] = MainMenu.ICON_GROUNDS_MOUSEOUT

        self.submenu_grounds.close()

    def close_all_submenus(self) -> None:

        self.close_cars_submenu(None)
        self.close_wheels_submenu(None)
        self.close_grounds_submenu(None)

    def display_garage(self, _) -> None:

        logger.debug("Button \"Garage\" clicked")

    def display_body_shop(self, _) -> None:

        logger.debug("Button \"Body Shop\" clicked")

    def save_car(self, _) -> None:

        logger.debug("Button \"Save Car\" clicked")

    def load(self, _) -> None:

        logger.debug("Button \"Load Car\" clicked")

    def save_image(self, _) -> None:

        logger.debug("Button \"Save Image\" clicked")

    def toggle_autorotate(self, _) -> None:

        logger.debug("Button \"Autorotate\" clicked")

        if self.main.autorotate:
            self.main.autorotate = False
        else:
            self.main.autorotate = True

        self.update_autorotate_icon(b1press=True)

    def update_autorotate_icon(self, b1press) -> None:

        if self.main.autorotate:
            if b1press:
                self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame["image"] = MainMenu.ICON_AUTOROTATE_OFF_MOUSEOVER
            else:
                self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame["image"] = MainMenu.ICON_AUTOROTATE_OFF_MOUSEOUT
            self.menu_buttons[MainMenu.TEXT_AUTOROTATE].icon_mouseout = MainMenu.ICON_AUTOROTATE_OFF_MOUSEOUT
            self.menu_buttons[MainMenu.TEXT_AUTOROTATE].icon_mouseover = MainMenu.ICON_AUTOROTATE_OFF_MOUSEOVER
        else:
            if b1press:
                self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame["image"] = MainMenu.ICON_AUTOROTATE_ON_MOUSEOVER
            else:
                self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame["image"] = MainMenu.ICON_AUTOROTATE_ON_MOUSEOUT
            self.menu_buttons[MainMenu.TEXT_AUTOROTATE].icon_mouseout = MainMenu.ICON_AUTOROTATE_ON_MOUSEOUT
            self.menu_buttons[MainMenu.TEXT_AUTOROTATE].icon_mouseover = MainMenu.ICON_AUTOROTATE_ON_MOUSEOVER

    def exit(self, _) -> None:

        logger.debug("Button \"Exit\" clicked")

        sys.exit()


class UI:

    # FIXME Remove all hardcoded values in this module
    # TODO Create the Garage interface (ride height, wheels, camber, quick-lists, ...)
    # TODO Create the Body Shop interface
    # FIXME Help freeing memory when changing cars, grounds, ... with : ModelPool.releaseModel("path/to/model.egg")
    # TODO Make a fade out/in lights when changing the car (to be confirmed)

    def __init__(self, main) -> None:

        self.main = main

        self.main_menu = MainMenu(main=self.main)
