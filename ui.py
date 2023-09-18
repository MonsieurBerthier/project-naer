import os
import sys
import math
import tkinter.filedialog

import direct.gui.DirectGui

import library.io

from config.logger import logger


class Button:

    def __init__(self, main, text: str, position_x: int, position_y: int, size_x: int, size_y: int, parent) -> None:

        self.border = direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                                       frameSize=(0, size_x + UI.BUTTON_BORDER_SIZE * 2, 0,
                                                                  size_y + UI.BUTTON_BORDER_SIZE * 2),
                                                       pos=(position_x - UI.BUTTON_BORDER_SIZE, 0,
                                                            -position_y - UI.BUTTON_BORDER_SIZE),
                                                       parent=parent)

        self.frame = direct.gui.DirectGui.DirectFrame(text=text,
                                                      text_fg=UI.WHITE,
                                                      text_font=main.font,
                                                      text_scale=UI.FONT_SIZE,
                                                      text_align=UI.TEXT_JUSTIFY_CENTER,
                                                      text_pos=(size_x / 2,
                                                                (size_y - UI.FONT_SIZE) / 2 + UI.BUTTON_TEXT_Y_OFFSET,
                                                                0),
                                                      frameColor=UI.RED,
                                                      frameSize=(0, size_x, 0, size_y),
                                                      pos=(position_x, 0, -position_y),
                                                      state=direct.gui.DirectGui.DGG.NORMAL,
                                                      parent=parent)

        self.frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                        command=self.set_button_mouseover_style)
        self.frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                        command=self.set_button_mouseout_style)

    def set_button_mouseover_style(self, _) -> None:

        self.frame["frameColor"] = UI.WHITE
        self.frame["text_fg"] = UI.GREY

    def set_button_mouseout_style(self, _) -> None:

        self.frame["frameColor"] = UI.RED
        self.frame["text_fg"] = UI.WHITE


class MenuButton:

    def __init__(self, main, text: str, font, position_x: int, position_y: int, size_x: int, size_y: int,
                 auto_event: bool, icon_mouseover: str, icon_mouseout: str,
                 image_pos_x: int, text_pad_x: int) -> None:

        self.icon_mouseover = icon_mouseover
        self.icon_mouseout = icon_mouseout

        self.frame = direct.gui.DirectGui.DirectFrame(frameColor=UI.RED,
                                                      text=text,
                                                      text_fg=UI.WHITE,
                                                      text_font=font,
                                                      text_scale=UI.FONT_SIZE,
                                                      text_align=UI.TEXT_JUSTIFY_LEFT,
                                                      text_pos=(text_pad_x,
                                                                -UI.BUTTON_Y_SIZE +
                                                                (UI.BUTTON_Y_SIZE - UI.FONT_SIZE) / 2 +
                                                                UI.BUTTON_TEXT_Y_OFFSET, 0),
                                                      frameSize=(0, size_x, 0, size_y),
                                                      pos=(position_x, 0, -position_y),
                                                      state=direct.gui.DirectGui.DGG.NORMAL,
                                                      parent=main.pixel2d,
                                                      image=self.icon_mouseout,
                                                      image_scale=MainMenu.BUTTON_ICON_SIZE,
                                                      image_pos=(image_pos_x, 0, -UI.BUTTON_Y_SIZE / 2))

        if auto_event:

            self.frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                            command=self.set_button_mouseover_style)

            self.frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                            command=self.set_button_mouseout_style)

    def set_button_mouseover_style(self, _) -> None:

        self.frame["frameColor"] = UI.WHITE
        self.frame["text_fg"] = UI.GREY
        self.frame["image"] = self.icon_mouseover

    def set_button_mouseout_style(self, _) -> None:

        self.frame["frameColor"] = UI.RED
        self.frame["text_fg"] = UI.WHITE
        self.frame["image"] = self.icon_mouseout


class CarPartButton:

    PART_STATUS_INSTALLED = "INSTALLED"

    def __init__(self, text: str, font, position_x: int, position_y: int, size_x: int, size_y: int, parent) -> None:

        self.part_is_installed = False

        self.frame = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.RED,
                                             text=text,
                                             text_fg=UI.WHITE,
                                             text_font=font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             text_pos=(UI.FONT_SIZE + UI.MARGIN, size_y - UI.FONT_SIZE - 5, 0),
                                             frameSize=(0, size_x, 0, size_y),
                                             pos=(position_x, 0, position_y),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=parent))

        self.part_color = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.RED,
                                             frameSize=(0, UI.FONT_SIZE, 0, UI.FONT_SIZE),
                                             pos=(6, 0, (size_y - UI.FONT_SIZE) / 2),
                                             parent=self.frame))

        self.status = direct.gui.DirectGui.DirectLabel(text="",
                                                       text_fg=UI.WHITE,
                                                       text_bg=UI.RED,
                                                       text_font=font,
                                                       text_scale=UI.FONT_SIZE - 8,
                                                       text_align=UI.TEXT_JUSTIFY_RIGHT,
                                                       pos=(size_x - 50, 0, (size_y - UI.FONT_SIZE) / 2 + 4),
                                                       parent=self.frame)

        self.frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                        command=self.set_button_mouseover_style)

        self.frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                        command=self.set_button_mouseout_style)

    def set_button_mouseover_style(self, _) -> None:

        self.frame["frameColor"] = UI.WHITE
        self.frame["text_fg"] = UI.GREY

        self.status["text_bg"] = UI.WHITE
        self.status["text_fg"] = UI.GREY

        if not self.part_is_installed:
            self.part_color["frameColor"] = UI.TRANSPARENT

    def set_button_mouseout_style(self, _) -> None:

        self.frame["frameColor"] = UI.RED
        self.frame["text_fg"] = UI.WHITE

        self.status["text_bg"] = UI.RED
        self.status["text_fg"] = UI.WHITE

        if not self.part_is_installed:
            self.part_color["frameColor"] = UI.TRANSPARENT

    def update_part_status(self, status: dict) -> None:

        if status["installed"]:
            self.part_is_installed = True
            self.status["text"] = CarPartButton.PART_STATUS_INSTALLED
            self.part_color["frameColor"] = status["color"]
        else:
            self.part_is_installed = False
            self.status["text"] = ""
            self.part_color["frameColor"] = UI.TRANSPARENT


class CheckButton:

    def __init__(self, text: str, font, position_x: int, position_y: int, size_x: int, size_y: int, parent) -> None:

        self.active = False

        self.frame = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.RED,
                                             text=text,
                                             text_fg=UI.WHITE,
                                             text_font=font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             text_pos=(UI.FONT_SIZE + UI.MARGIN, size_y - UI.FONT_SIZE - 5, 0),
                                             frameSize=(0, size_x, 0, size_y),
                                             pos=(position_x, 0, position_y),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=parent))

        self.check_button_border = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                             frameSize=(0, UI.FONT_SIZE, 0, UI.FONT_SIZE),
                                             pos=(0, 0, (size_y - UI.FONT_SIZE) / 2),
                                             parent=self.frame))

        self.check_button = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.RED,
                                             frameSize=(0, UI.FONT_SIZE - 6, 0, UI.FONT_SIZE - 6),
                                             pos=(3, 0, (size_y - UI.FONT_SIZE) / 2 + 3),
                                             parent=self.frame))

        self.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                        command=self.toggle_check_button)

    def toggle_check_button(self, _):

        if self.active:
            self.check_button["frameColor"] = UI.RED
            self.active = False
        else:
            self.check_button["frameColor"] = UI.WHITE
            self.active = True


class SubMenu:

    TEXT_PADDING_LEFT = 50
    BUTTON_ICON_POS = int(TEXT_PADDING_LEFT / 2)

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
                                text=items[i][1],
                                font=self.main.font,
                                text_pad_x=SubMenu.TEXT_PADDING_LEFT,
                                position_x=UI.MARGIN + UI.BUTTON_Y_SIZE + MainMenu.MAIN_MENU_X_SIZE,
                                position_y=-UI.get_button_y_position(index=i),
                                size_x=self.menu_x_size, size_y=-UI.BUTTON_Y_SIZE,
                                auto_event=True,
                                image_pos_x=SubMenu.BUTTON_ICON_POS,
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

    def callback_load_car(self, tag, _) -> None:

        self.main.car.load(tag=tag)

    def callback_load_wheels(self, tag, _) -> None:

        self.main.car.load_wheels(tag=tag, oem=False)

    def callback_load_ground(self, tag, _) -> None:

        self.main.ground.change(tag=tag)

    def close(self) -> None:

        for button in self.buttons:
            button.frame.destroy()
        self.buttons = []


class MainMenu:

    TEXT_PADDING_LEFT = 60
    BUTTON_ICON_SIZE = (16, 0, 11)
    BUTTON_ICON_POS = int(TEXT_PADDING_LEFT / 2)

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
            direct.gui.DirectGui.DirectFrame(frameColor=UI.TRANSPARENT,
                                             frameSize=(0, UI.BUTTON_Y_SIZE, 0, -UI.BUTTON_Y_SIZE),
                                             pos=(UI.MARGIN, 0, -UI.MARGIN),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))
        self.open_button["TopLine"] = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                             frameSize=(0, UI.BUTTON_Y_SIZE, 0, -MainMenu.MAIN_BUTTON_BAR_Y_SIZE),
                                             pos=(UI.MARGIN, 0, -UI.MARGIN),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))
        self.open_button["MiddleLine"] = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                             frameSize=(0, UI.BUTTON_Y_SIZE, 0, -MainMenu.MAIN_BUTTON_BAR_Y_SIZE),
                                             pos=(UI.MARGIN, 0, - (UI.BUTTON_Y_SIZE / 2) - UI.MARGIN +
                                                  (MainMenu.MAIN_BUTTON_BAR_Y_SIZE / 2)),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))
        self.open_button["BottomLine"] = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                             frameSize=(0, UI.BUTTON_Y_SIZE, 0, -MainMenu.MAIN_BUTTON_BAR_Y_SIZE),
                                             pos=(UI.MARGIN, 0,
                                                  -UI.BUTTON_Y_SIZE - UI.MARGIN + MainMenu.MAIN_BUTTON_BAR_Y_SIZE),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.main.pixel2d))

        self.open_button["Background"].bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                            command=self.open_main_menu)

    def open_main_menu(self, _) -> None:

        if self.menu_buttons:
            return

        self.open_button["Background"]["frameColor"] = UI.WHITE
        self.close_button = direct.gui.DirectGui.DirectFrame(frameColor=UI.TRANSPARENT,
                                                             frameSize=(0, self.main.window_resolution[0], 0,
                                                                        -self.main.window_resolution[1]),
                                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                                             parent=self.main.pixel2d)
        self.close_button.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                               command=self.close_main_menu)

        self.menu_buttons[MainMenu.TEXT_CARS] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_CARS,
                       font=self.main.font,
                       text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                       position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       position_y=UI.MARGIN,
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-UI.BUTTON_Y_SIZE,
                       auto_event=False,
                       image_pos_x=MainMenu.BUTTON_ICON_POS,
                       icon_mouseover=MainMenu.ICON_CARS_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_CARS_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_CARS].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                         command=self.open_cars_submenu)

        self.menu_buttons[MainMenu.TEXT_WHEELS] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_WHEELS,
                       font=self.main.font,
                       text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                       position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       position_y=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-UI.BUTTON_Y_SIZE,
                       auto_event=False,
                       image_pos_x=MainMenu.BUTTON_ICON_POS,
                       icon_mouseover=MainMenu.ICON_WHEELS_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_WHEELS_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_WHEELS].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                           command=self.open_wheels_submenu)

        self.menu_buttons[MainMenu.TEXT_GROUNDS] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_GROUNDS,
                       font=self.main.font,
                       text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                       position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       position_y=UI.MARGIN + (2 * UI.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-UI.BUTTON_Y_SIZE,
                       auto_event=False,
                       image_pos_x=MainMenu.BUTTON_ICON_POS,
                       icon_mouseover=MainMenu.ICON_GROUNDS_MOUSEOVER,
                       icon_mouseout=MainMenu.ICON_GROUNDS_MOUSEOUT))
        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                                            command=self.open_grounds_submenu)

        self.menu_buttons[MainMenu.TEXT_GARAGE] = (
            MenuButton(main=self.main,
                       text=MainMenu.TEXT_GARAGE,
                       font=self.main.font,
                       text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                       position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       position_y=UI.MARGIN + (3 * UI.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-UI.BUTTON_Y_SIZE,
                       auto_event=False,
                       image_pos_x=MainMenu.BUTTON_ICON_POS,
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
                       text=MainMenu.TEXT_BODY_SHOP,
                       font=self.main.font,
                       text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                       position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       position_y=UI.MARGIN + (4 * UI.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-UI.BUTTON_Y_SIZE,
                       auto_event=False,
                       image_pos_x=MainMenu.BUTTON_ICON_POS,
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
                       text=MainMenu.TEXT_SAVE_CAR,
                       font=self.main.font,
                       text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                       position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       position_y=UI.MARGIN + (5 * UI.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-UI.BUTTON_Y_SIZE,
                       auto_event=False,
                       image_pos_x=MainMenu.BUTTON_ICON_POS,
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
                       text=MainMenu.TEXT_LOAD_CAR,
                       font=self.main.font,
                       text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                       position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       position_y=UI.MARGIN + (6 * UI.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-UI.BUTTON_Y_SIZE,
                       auto_event=False,
                       image_pos_x=MainMenu.BUTTON_ICON_POS,
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
                       text=MainMenu.TEXT_SAVE_IMAGE,
                       font=self.main.font,
                       text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                       position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       position_y=UI.MARGIN + (7 * UI.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-UI.BUTTON_Y_SIZE,
                       auto_event=False,
                       image_pos_x=MainMenu.BUTTON_ICON_POS,
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
                       text=MainMenu.TEXT_AUTOROTATE,
                       font=self.main.font,
                       text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                       position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       position_y=UI.MARGIN + (8 * UI.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-UI.BUTTON_Y_SIZE,
                       auto_event=False,
                       image_pos_x=MainMenu.BUTTON_ICON_POS,
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
                       text=MainMenu.TEXT_EXIT,
                       font=self.main.font,
                       text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                       position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                       position_y=UI.MARGIN + (9 * UI.BUTTON_Y_SIZE),
                       size_x=MainMenu.MAIN_MENU_X_SIZE, size_y=-UI.BUTTON_Y_SIZE,
                       auto_event=False,
                       image_pos_x=MainMenu.BUTTON_ICON_POS,
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
        button.frame["frameColor"] = UI.WHITE
        button.frame["text_fg"] = UI.GREY
        button.frame["image"] = button.icon_mouseover

    @staticmethod
    def set_button_mouseout_style(button, _) -> None:

        button.frame["frameColor"] = UI.RED
        button.frame["text_fg"] = UI.WHITE
        button.frame["image"] = button.icon_mouseout

    def close_main_menu(self, _) -> None:

        self.close_button.destroy()

        self.close_all_submenus()

        for button in self.menu_buttons:
            self.menu_buttons[button].frame.destroy()
        self.menu_buttons = {}

        self.open_button["Background"]["frameColor"] = UI.TRANSPARENT

    def open_cars_submenu(self, _) -> None:

        self.close_all_submenus()

        self.menu_buttons[MainMenu.TEXT_CARS].frame["frameColor"] = UI.WHITE
        self.menu_buttons[MainMenu.TEXT_CARS].frame["text_fg"] = UI.GREY
        self.menu_buttons[MainMenu.TEXT_CARS].frame["image"] = MainMenu.ICON_CARS_MOUSEOVER

        self.submenu_cars.open(content_path=self.main.PATH_CARS)

    def close_cars_submenu(self, _) -> None:

        self.submenu_cars.close()

        self.menu_buttons[MainMenu.TEXT_CARS].frame["frameColor"] = UI.RED
        self.menu_buttons[MainMenu.TEXT_CARS].frame["text_fg"] = UI.WHITE
        self.menu_buttons[MainMenu.TEXT_CARS].frame["image"] = MainMenu.ICON_CARS_MOUSEOUT

    def open_wheels_submenu(self, _) -> None:

        self.close_all_submenus()

        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["frameColor"] = UI.WHITE
        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["text_fg"] = UI.GREY
        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["image"] = MainMenu.ICON_WHEELS_MOUSEOVER

        self.submenu_wheels.open(content_path=self.main.PATH_WHEELS)

    def close_wheels_submenu(self, _) -> None:

        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["frameColor"] = UI.RED
        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["text_fg"] = UI.WHITE
        self.menu_buttons[MainMenu.TEXT_WHEELS].frame["image"] = MainMenu.ICON_WHEELS_MOUSEOUT

        self.submenu_wheels.close()

    def open_grounds_submenu(self, _) -> None:

        self.close_all_submenus()

        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["frameColor"] = UI.WHITE
        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["text_fg"] = UI.GREY
        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["image"] = MainMenu.ICON_GROUNDS_MOUSEOVER

        self.submenu_grounds.open(content_path=self.main.PATH_GROUNDS)

    def close_grounds_submenu(self, _) -> None:

        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["frameColor"] = UI.RED
        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["text_fg"] = UI.WHITE
        self.menu_buttons[MainMenu.TEXT_GROUNDS].frame["image"] = MainMenu.ICON_GROUNDS_MOUSEOUT

        self.submenu_grounds.close()

    def close_all_submenus(self) -> None:

        self.close_cars_submenu(None)
        self.close_wheels_submenu(None)
        self.close_grounds_submenu(None)

    def display_garage(self, _) -> None:

        logger.debug("Button \"Garage\" clicked")

        self.close_main_menu(None)
        Garage(main=self.main)

    def display_body_shop(self, _) -> None:

        logger.debug("Button \"Body Shop\" clicked")

        self.close_main_menu(None)
        BodyShop(main=self.main)

    def save_car(self, _) -> None:

        logger.debug("Button \"Save Car\" clicked")

        root = tkinter.Tk()
        root.iconify()

        path_to_car = tkinter.filedialog.asksaveasfile(mode="w",
                                                       title="Save car",
                                                       defaultextension=".pnc")

        self.close_main_menu(None)

    def load(self, _) -> None:

        logger.debug("Button \"Load Car\" clicked")

        root = tkinter.Tk()
        root.iconify()

        path_to_car = tkinter.filedialog.askopenfilename(title="Load a car (*.pnc)",
                                                         defaultextension=".pnc")

        self.close_main_menu(None)

    def save_image(self, _) -> None:

        logger.debug("Button \"Save Image\" clicked")

        root = tkinter.Tk()
        root.iconify()

        path_to_image = tkinter.filedialog.asksaveasfile(mode="w",
                                                         title="Save image",
                                                         defaultextension=".png")

        self.close_main_menu(None)

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
                self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame["image"] = MainMenu.ICON_AUTOROTATE_ON_MOUSEOVER
            else:
                self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame["image"] = MainMenu.ICON_AUTOROTATE_ON_MOUSEOUT
            self.menu_buttons[MainMenu.TEXT_AUTOROTATE].icon_mouseout = MainMenu.ICON_AUTOROTATE_ON_MOUSEOUT
            self.menu_buttons[MainMenu.TEXT_AUTOROTATE].icon_mouseover = MainMenu.ICON_AUTOROTATE_ON_MOUSEOVER
        else:
            if b1press:
                self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame["image"] = MainMenu.ICON_AUTOROTATE_OFF_MOUSEOVER
            else:
                self.menu_buttons[MainMenu.TEXT_AUTOROTATE].frame["image"] = MainMenu.ICON_AUTOROTATE_OFF_MOUSEOUT
            self.menu_buttons[MainMenu.TEXT_AUTOROTATE].icon_mouseout = MainMenu.ICON_AUTOROTATE_OFF_MOUSEOUT
            self.menu_buttons[MainMenu.TEXT_AUTOROTATE].icon_mouseover = MainMenu.ICON_AUTOROTATE_OFF_MOUSEOVER

    def exit(self, _) -> None:

        logger.debug("Button \"Exit\" clicked")

        sys.exit()


class SideWindow:

    def __init__(self, main, size_x: int, size_y: int) -> None:

        self.main = main

        self.frame = direct.gui.DirectGui.DirectFrame(frameColor=UI.RED,
                                                      frameSize=(0, size_x, 0, size_y),
                                                      pos=(self.main.window_resolution[0] - size_x, 0,
                                                           -size_y - ((self.main.window_resolution[1] - size_y) / 2)),
                                                      parent=self.main.pixel2d)

        self.button_done = Button(main=self.main,
                                  text="OK",
                                  position_x=int((size_x - UI.BUTTON_MEDIUM_X_SIZE) / 2),
                                  position_y=-UI.MARGIN,
                                  size_x=UI.BUTTON_MEDIUM_X_SIZE,
                                  size_y=UI.BUTTON_Y_SIZE,
                                  parent=self.frame)
        self.button_done.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                    command=self.close)

    def close(self, _) -> None:

        self.frame.destroy()


class Garage(SideWindow):

    SLIDER_SCALE = 80
    FRAME_X_SIZE = 500
    FRAME_Y_SIZE = 1080
    NB_ITEMS_SCROLLED_FRAME = 5

    def __init__(self, main) -> None:

        super().__init__(main=main, size_x=self.FRAME_X_SIZE, size_y=self.FRAME_Y_SIZE)

        self.car_ride_height_slider = None
        self.car_pitch_slider = None

        self.wheel_diameter_slider = {}
        self.wheel_width_slider = {}
        self.wheel_offset_slider = {}
        self.wheel_camber_slider = {}
        self.wheel_toe_slider = {}

        self.bodykits_frame = None
        self.bodykits_buttons = []

        self.display_car_parameters()
        self.display_wheels_parameters()
        self.display_bodykits()

    def display_car_parameters(self):

        direct.gui.DirectGui.DirectLabel(text="Car",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_TITLE_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0, Garage.FRAME_Y_SIZE - UI.MARGIN - UI.FONT_SIZE * 1.5),
                                         parent=self.frame)

        direct.gui.DirectGui.DirectLabel(text="Ride Height",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN * 2, 0, Garage.FRAME_Y_SIZE - 90),
                                         parent=self.frame)

        self.car_ride_height_slider = (
            direct.gui.DirectGui.DirectSlider(range=(-0.6, 0.6),
                                              value=self.main.car.nodepath.getPos()[2],
                                              pageSize=0.02,
                                              pos=(Garage.FRAME_X_SIZE / 2, 0, Garage.FRAME_Y_SIZE - 82),
                                              scale=Garage.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.update_car_ride_height,
                                              parent=self.frame))

        direct.gui.DirectGui.DirectLabel(text="Pitch",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN * 2, 0, Garage.FRAME_Y_SIZE - 130),
                                         parent=self.frame)

        self.car_pitch_slider = (
            direct.gui.DirectGui.DirectSlider(range=(-4, 4),
                                              value=self.main.car.nodepath.getHpr()[1],
                                              pageSize=0.2,
                                              pos=(Garage.FRAME_X_SIZE / 2, 0, Garage.FRAME_Y_SIZE - 122),
                                              scale=Garage.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.update_car_pitch,
                                              parent=self.frame))

    def display_wheels_parameters(self):

        index = 0

        for axle in self.main.car.json["wheels"]:

            json_wheel_diameter = self.main.car.json["wheels"][axle][0]["scale"][1]
            current_wheel_diameter = self.main.car.items["wheels"][axle][0].model.getScale()[1]

            json_wheel_width = self.main.car.json["wheels"][axle][0]["scale"][0]
            current_wheel_width = self.main.car.items["wheels"][axle][0].model.getScale()[0]

            json_wheel_offset = self.main.car.json["wheels"][axle][0]["position"][0]
            current_wheel_offset = self.main.car.items["wheels"][axle][0].model.getPos()[0]

            json_wheel_camber = self.main.car.json["wheels"][axle][0]["rotation"][2]
            current_wheel_camber = self.main.car.items["wheels"][axle][0].model.getHpr()[2]

            json_wheel_toe = self.main.car.json["wheels"][axle][0]["rotation"][0]
            current_wheel_toe = self.main.car.items["wheels"][axle][0].model.getHpr()[0]

            direct.gui.DirectGui.DirectLabel(text=f"{axle.title()} Wheels",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_TITLE_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN, 0, -255 * index + 900),
                                             parent=self.frame)

            direct.gui.DirectGui.DirectLabel(text="Diameter",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN * 2, 0, -250 * index + 855),
                                             parent=self.frame)

            self.wheel_diameter_slider[axle] = (
                direct.gui.DirectGui.DirectSlider(range=(0.5 * json_wheel_diameter, 1.50 * json_wheel_diameter),
                                                  value=current_wheel_diameter,
                                                  pageSize=0.05,
                                                  pos=(Garage.FRAME_X_SIZE / 2, 0, -250 * index + 863),
                                                  scale=Garage.SLIDER_SCALE,
                                                  color=UI.WHITE,
                                                  thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                                  thumb_color=UI.WHITE,
                                                  command=self.update_wheel_diameter,
                                                  extraArgs=[axle],
                                                  parent=self.frame))

            direct.gui.DirectGui.DirectLabel(text="Width",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN * 2, 0, -250 * index + 815),
                                             parent=self.frame)

            self.wheel_width_slider[axle] = (
                direct.gui.DirectGui.DirectSlider(range=(0.4 * json_wheel_width, 1.6 * json_wheel_width),
                                                  value=current_wheel_width,
                                                  pageSize=0.1,
                                                  pos=(Garage.FRAME_X_SIZE / 2, 0, -250 * index + 823),
                                                  scale=Garage.SLIDER_SCALE,
                                                  color=UI.WHITE,
                                                  thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                                  thumb_color=UI.WHITE,
                                                  command=self.update_wheel_width,
                                                  extraArgs=[axle],
                                                  parent=self.frame))

            direct.gui.DirectGui.DirectLabel(text="Offset",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN * 2, 0, -250 * index + 775),
                                             parent=self.frame)

            self.wheel_offset_slider[axle] = (
                direct.gui.DirectGui.DirectSlider(range=(0.66 * json_wheel_offset, 1.34 * json_wheel_offset),
                                                  value=current_wheel_offset,
                                                  pageSize=0.02,
                                                  pos=(Garage.FRAME_X_SIZE / 2, 0, -250 * index + 783),
                                                  scale=Garage.SLIDER_SCALE,
                                                  color=UI.WHITE,
                                                  thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                                  thumb_color=UI.WHITE,
                                                  command=self.update_wheel_offset,
                                                  extraArgs=[axle],
                                                  parent=self.frame))

            direct.gui.DirectGui.DirectLabel(text="Camber",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN * 2, 0, -250 * index + 735),
                                             parent=self.frame)

            self.wheel_camber_slider[axle] = (
                direct.gui.DirectGui.DirectSlider(range=(json_wheel_camber - 45, json_wheel_camber + 45),
                                                  value=current_wheel_camber,
                                                  pageSize=0.5,
                                                  pos=(Garage.FRAME_X_SIZE / 2, 0, -250 * index + 743),
                                                  scale=Garage.SLIDER_SCALE,
                                                  color=UI.WHITE,
                                                  thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                                  thumb_color=UI.WHITE,
                                                  command=self.update_wheel_camber,
                                                  extraArgs=[axle],
                                                  parent=self.frame))

            direct.gui.DirectGui.DirectLabel(text="Toe",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN * 2, 0, -250 * index + 695),
                                             parent=self.frame)

            self.wheel_toe_slider[axle] = (
                direct.gui.DirectGui.DirectSlider(range=(json_wheel_toe - 10, json_wheel_toe + 10),
                                                  value=current_wheel_toe,
                                                  pageSize=0.3,
                                                  pos=(Garage.FRAME_X_SIZE / 2, 0, -250 * index + 703),
                                                  scale=Garage.SLIDER_SCALE,
                                                  color=UI.WHITE,
                                                  thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                                  thumb_color=UI.WHITE,
                                                  command=self.update_wheel_toe,
                                                  extraArgs=[axle],
                                                  parent=self.frame))

            index += 1

    def display_bodykits(self):

        nb_bodykits = len(self.main.car.json["bodykits"])

        direct.gui.DirectGui.DirectLabel(text="Bodykits",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_TITLE_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0, Garage.FRAME_Y_SIZE - 685),
                                         parent=self.frame)

        self.bodykits_frame = (
            direct.gui.DirectGui.DirectScrolledFrame(canvasSize=(0, Garage.FRAME_X_SIZE - (4 * UI.MARGIN),
                                                                 0, UI.BUTTON_Y_SIZE * nb_bodykits),
                                                     frameSize=(0, Garage.FRAME_X_SIZE - (2 * UI.MARGIN),
                                                                0, UI.BUTTON_Y_SIZE * Garage.NB_ITEMS_SCROLLED_FRAME),
                                                     pos=(UI.MARGIN, 0, BodyShop.FRAME_Y_SIZE -
                                                          Garage.NB_ITEMS_SCROLLED_FRAME * UI.BUTTON_Y_SIZE - 704),
                                                     frameColor=UI.RED,
                                                     scrollBarWidth=UI.MARGIN * 1.5,
                                                     verticalScroll_color=UI.WHITE,
                                                     verticalScroll_incButton_relief=False,
                                                     verticalScroll_decButton_relief=False,
                                                     parent=self.frame))

        for i in range(len(self.main.car.json["bodykits"])):

            bodykit_button = (
                direct.gui.DirectGui.DirectFrame(text=self.main.car.json["bodykits"][i]["name"],
                                                 text_fg=UI.WHITE,
                                                 text_font=self.main.font,
                                                 text_scale=UI.FONT_SIZE,
                                                 text_align=UI.TEXT_JUSTIFY_LEFT,
                                                 text_pos=(0, (UI.FONT_SIZE / 2) - 3, 0),
                                                 frameColor=UI.RED,
                                                 frameSize=(0, Garage.FRAME_X_SIZE - 2 * UI.MARGIN,
                                                            0, UI.BUTTON_Y_SIZE),
                                                 pos=(UI.MARGIN, 0,
                                                      (UI.BUTTON_Y_SIZE * (nb_bodykits - 1)) - (UI.BUTTON_Y_SIZE * i)),
                                                 state=direct.gui.DirectGui.DGG.NORMAL,
                                                 parent=self.bodykits_frame.getCanvas()))

            bodykit_button.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                                command=self.set_button_mouseover_style,
                                extraArgs=[bodykit_button])
            bodykit_button.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                                command=self.set_button_mouseout_style,
                                extraArgs=[bodykit_button])
            bodykit_button.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                command=self.callback_load_bodykit,
                                extraArgs=[self.main.car.json["bodykits"][i]["name"]])

            self.bodykits_buttons.append(bodykit_button)

    def update_car_ride_height(self):

        current_car_position = self.main.car.nodepath.getPos()

        self.main.car.nodepath.setPos((current_car_position[0],
                                       current_car_position[1],
                                       self.car_ride_height_slider["value"]))

    def update_car_pitch(self):

        current_car_rotation = self.main.car.nodepath.getHpr()

        self.main.car.nodepath.setHpr((current_car_rotation[0],
                                       self.car_pitch_slider["value"],
                                       current_car_rotation[2]))

    def update_wheel_diameter(self, axle):

        for i in range(len(self.main.car.json["wheels"][axle])):

            current_wheel_scale = self.main.car.items["wheels"][axle][i].model.getScale()

            self.main.car.items["wheels"][axle][i].model.setScale((current_wheel_scale[0],
                                                                   self.wheel_diameter_slider[axle]["value"],
                                                                   self.wheel_diameter_slider[axle]["value"]))

    def update_wheel_width(self, axle):

        for i in range(len(self.main.car.items["wheels"][axle])):

            current_wheel_scale = self.main.car.items["wheels"][axle][i].model.getScale()

            self.main.car.items["wheels"][axle][i].model.setScale((self.wheel_width_slider[axle]["value"],
                                                                   current_wheel_scale[1],
                                                                   current_wheel_scale[2]))

    def update_wheel_offset(self, axle):

        for i in range(len(self.main.car.items["wheels"][axle])):

            current_wheel_position = self.main.car.items["wheels"][axle][i].model.getPos()

            self.main.car.items["wheels"][axle][i].model.setPos((math.copysign(self.wheel_offset_slider[axle]["value"],
                                                                               current_wheel_position[0]),
                                                                 current_wheel_position[1],
                                                                 current_wheel_position[2]))

    def update_wheel_camber(self, axle):

        for i in range(len(self.main.car.items["wheels"][axle])):

            current_wheel_rotation = self.main.car.items["wheels"][axle][i].model.getHpr()

            if current_wheel_rotation[2] > 90:
                new_wheel_camber = 180 - self.wheel_camber_slider[axle]["value"]
            else:
                new_wheel_camber = self.wheel_camber_slider[axle]["value"]

            self.main.car.items["wheels"][axle][i].model.setHpr((current_wheel_rotation[0],
                                                                 current_wheel_rotation[1],
                                                                 new_wheel_camber))

    def update_wheel_toe(self, axle):

        for i in range(len(self.main.car.items["wheels"][axle])):

            current_wheel_rotation = self.main.car.items["wheels"][axle][i].model.getHpr()

            if current_wheel_rotation[2] > 90:
                new_wheel_toe = - self.wheel_toe_slider[axle]["value"]
            else:
                new_wheel_toe = self.wheel_toe_slider[axle]["value"]

            self.main.car.items["wheels"][axle][i].model.setHpr((new_wheel_toe,
                                                                 current_wheel_rotation[1],
                                                                 current_wheel_rotation[2]))

    @staticmethod
    def set_button_mouseover_style(button, _) -> None:

        button["frameColor"] = UI.WHITE
        button["text_fg"] = UI.GREY

    @staticmethod
    def set_button_mouseout_style(button, _) -> None:

        button["frameColor"] = UI.RED
        button["text_fg"] = UI.WHITE

    def callback_load_bodykit(self, name, _):

        self.main.car.load_bodykit(bodykit=name)


class BodyShop(SideWindow):

    SLIDER_SCALE = 80
    FRAME_X_SIZE = 500
    FRAME_Y_SIZE = 1080
    NB_ITEMS_SCROLLED_FRAME = 12

    def __init__(self, main) -> None:

        super().__init__(main=main, size_x=self.FRAME_X_SIZE, size_y=self.FRAME_Y_SIZE)

        self.car_parts_frame = None

        self.car_parts_buttons = []

        self.selected_part = None
        self.paint_metallic = None
        self.paint_brilliance = None
        self.paint_red = None
        self.paint_green = None
        self.paint_blue = None
        self.paint_preview = None
        self.paint_code = None
        self.paint_all_parts = None

        self.display_car_parts()
        self.display_paint_selector()

    def display_car_parts(self):

        car_items_status = self.main.car.get_items_status()
        nb_car_items = len(car_items_status)

        direct.gui.DirectGui.DirectLabel(text="Car Parts",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_TITLE_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0, BodyShop.FRAME_Y_SIZE - UI.MARGIN - UI.FONT_SIZE * 1.5),
                                         parent=self.frame)

        self.car_parts_frame = (
            direct.gui.DirectGui.DirectScrolledFrame(canvasSize=(0, BodyShop.FRAME_X_SIZE - (4 * UI.MARGIN),
                                                                 0, UI.BUTTON_Y_SIZE * nb_car_items),
                                                     frameSize=(0, BodyShop.FRAME_X_SIZE - (2 * UI.MARGIN), 0,
                                                                UI.BUTTON_Y_SIZE * BodyShop.NB_ITEMS_SCROLLED_FRAME),
                                                     pos=(UI.MARGIN, 0, BodyShop.FRAME_Y_SIZE -
                                                          BodyShop.NB_ITEMS_SCROLLED_FRAME * UI.BUTTON_Y_SIZE - 63),
                                                     frameColor=UI.RED,
                                                     scrollBarWidth=UI.MARGIN * 1.5,
                                                     verticalScroll_color=UI.WHITE,
                                                     verticalScroll_incButton_relief=False,
                                                     verticalScroll_decButton_relief=False,
                                                     parent=self.frame))

        for i in range(nb_car_items):

            car_part_button = CarPartButton(text=car_items_status[i]["name"],
                                            font=self.main.font,
                                            position_x=UI.MARGIN,
                                            position_y=(UI.BUTTON_Y_SIZE * (nb_car_items - 1)) - (UI.BUTTON_Y_SIZE * i),
                                            size_x=BodyShop.FRAME_X_SIZE - 2 * UI.MARGIN,
                                            size_y=UI.BUTTON_Y_SIZE,
                                            parent=self.car_parts_frame.getCanvas())

            car_part_button.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                                       command=self.callback_load_car_part,
                                       extraArgs=[car_items_status[i]["tag"]])

            car_part_button.update_part_status(status=car_items_status[i])

            self.car_parts_buttons.append(car_part_button)

    def refresh_car_items(self):

        car_items_status = self.main.car.get_items_status()

        for i in range(len(car_items_status)):
            self.car_parts_buttons[i].update_part_status(status=car_items_status[i])

    def display_paint_selector(self):

        direct.gui.DirectGui.DirectLabel(text="Paint",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_TITLE_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0, BodyShop.FRAME_Y_SIZE - 491),
                                         parent=self.frame)

        direct.gui.DirectGui.DirectLabel(text="Selected part :",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN * 2, 0, BodyShop.FRAME_Y_SIZE - 541),
                                         parent=self.frame)

        self.selected_part = direct.gui.DirectGui.DirectLabel(text="ALL",
                                                              text_fg=UI.WHITE,
                                                              text_bg=UI.RED,
                                                              text_font=self.main.font,
                                                              text_scale=UI.FONT_SIZE,
                                                              text_align=UI.TEXT_JUSTIFY_LEFT,
                                                              pos=(180, 0, BodyShop.FRAME_Y_SIZE - 541),
                                                              parent=self.frame)

        direct.gui.DirectGui.DirectLabel(text="Metallic",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN * 2, 0, BodyShop.FRAME_Y_SIZE - 581),
                                         parent=self.frame)

        self.paint_metallic = (
            direct.gui.DirectGui.DirectSlider(range=(0, 1),
                                              value=0,
                                              pageSize=0.1,
                                              pos=(BodyShop.FRAME_X_SIZE / 2, 0, BodyShop.FRAME_Y_SIZE - 573),
                                              scale=BodyShop.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_paint_metallic,
                                              parent=self.frame))

        direct.gui.DirectGui.DirectLabel(text="Brilliance",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN * 2, 0, BodyShop.FRAME_Y_SIZE - 621),
                                         parent=self.frame)

        self.paint_brilliance = (
            direct.gui.DirectGui.DirectSlider(range=(0, 1),
                                              value=0,
                                              pageSize=0.1,
                                              pos=(BodyShop.FRAME_X_SIZE / 2, 0, BodyShop.FRAME_Y_SIZE - 613),
                                              scale=BodyShop.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_paint_brilliance,
                                              parent=self.frame))

        direct.gui.DirectGui.DirectLabel(text="Red",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN * 2, 0, BodyShop.FRAME_Y_SIZE - 661),
                                         parent=self.frame)

        self.paint_red = (
            direct.gui.DirectGui.DirectSlider(range=(0, 1),
                                              value=0.5,
                                              pageSize=0.1,
                                              pos=(BodyShop.FRAME_X_SIZE / 2, 0, BodyShop.FRAME_Y_SIZE - 653),
                                              scale=BodyShop.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_paint_color,
                                              parent=self.frame))

        direct.gui.DirectGui.DirectLabel(text="Green",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN * 2, 0, BodyShop.FRAME_Y_SIZE - 701),
                                         parent=self.frame)

        self.paint_green = (
            direct.gui.DirectGui.DirectSlider(range=(0, 1),
                                              value=0.5,
                                              pageSize=0.1,
                                              pos=(BodyShop.FRAME_X_SIZE / 2, 0, BodyShop.FRAME_Y_SIZE - 693),
                                              scale=BodyShop.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_paint_color,
                                              parent=self.frame))

        direct.gui.DirectGui.DirectLabel(text="Blue",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN * 2, 0, BodyShop.FRAME_Y_SIZE - 741),
                                         parent=self.frame)

        self.paint_blue = (
            direct.gui.DirectGui.DirectSlider(range=(0, 1),
                                              value=0.5,
                                              pageSize=0.1,
                                              pos=(BodyShop.FRAME_X_SIZE / 2, 0, BodyShop.FRAME_Y_SIZE - 733),
                                              scale=BodyShop.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_paint_color,
                                              parent=self.frame))

        direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                         frameSize=(0, 100, 0, 120),
                                         pos=(370, 0, BodyShop.FRAME_Y_SIZE - 713),
                                         parent=self.frame)

        self.paint_preview = (
            direct.gui.DirectGui.DirectFrame(frameColor=(0, 1, 0, 1),
                                             frameSize=(0, 94, 0, 94),
                                             pos=(370 + 3, 0, BodyShop.FRAME_Y_SIZE - 710),
                                             parent=self.frame))

        self.paint_code = (
            direct.gui.DirectGui.DirectEntry(initialText="FF00FF00FF",
                                             text_fg=UI.GREY,
                                             entryFont=self.main.font,
                                             frameColor=UI.WHITE,
                                             numLines=1,
                                             scale=18,
                                             width=5,
                                             pos=(375, 0, BodyShop.FRAME_Y_SIZE - 619),
                                             parent=self.frame))

        self.paint_all_parts = CheckButton(text="Paint all car parts",
                                           font=self.main.font,
                                           position_x=UI.MARGIN * 2,
                                           position_y=BodyShop.FRAME_Y_SIZE - 790,
                                           size_x=BodyShop.FRAME_X_SIZE - 3 * UI.MARGIN,
                                           size_y=UI.BUTTON_Y_SIZE,
                                           parent=self.frame)

    @staticmethod
    def set_button_mouseover_style(button, _) -> None:

        button["frameColor"] = UI.WHITE
        button["text_fg"] = UI.GREY

    @staticmethod
    def set_button_mouseout_style(button, _) -> None:

        button["frameColor"] = UI.RED
        button["text_fg"] = UI.WHITE

    def callback_load_car_part(self, name, _):

        self.main.car.load_part(tag=name)
        self.refresh_car_items()

    def callback_update_paint_metallic(self):

        self.main.car.items["chassis"].model.findMaterial("paint").setMetallic(self.paint_metallic["value"])

    def callback_update_paint_brilliance(self):

        self.main.car.items["chassis"].model.findMaterial("paint").setRoughness(1 - self.paint_brilliance["value"])

    def callback_update_paint_color(self):

        new_color = (self.paint_red["value"],
                     self.paint_green["value"],
                     self.paint_blue["value"], 1)

        self.paint_preview.setColor(new_color)
        self.main.car.items["chassis"].model.findMaterial("paint").setBaseColor(new_color)


class UI:

    # TODO Utiliser la liste names dans le JSON de la voiture pour créer l'ordre dans le BodyShop
    # TODO Add chassis and wheels in the return list get_items_status()
    # FIXME Reloading the same car keeps the same paint color
    # TODO Update Garage menu: keep wheels adjustments when changing wheels
    # TODO Update Garage menu: add DirectEntry at the right for each car/wheel parameter
    # TODO Encapsulate all DirectGUI elements in frames
    # TODO Update Garage menu: increasing wheel diameter should change wheel z-position and car pitch
    # FIXME Help freeing memory when changing cars, grounds, ... with : ModelPool.releaseModel("path/to/model.egg")
    # TODO Make a fade out/in lights when changing the car (to be confirmed)

    MARGIN = 16
    FONT_SIZE = 20
    FONT_TITLE_SIZE = 24
    BUTTON_Y_SIZE = 32
    BUTTON_BORDER_SIZE = 3
    BUTTON_TEXT_Y_OFFSET = 1
    BUTTON_MEDIUM_X_SIZE = 100

    GREY = (0.2, 0.2, 0.2, 1)
    RED = (1, 0, 0, 1)
    WHITE = (1, 1, 1, 1)
    TRANSPARENT = (0, 0, 0, 0)

    TEXT_JUSTIFY_LEFT = 0
    TEXT_JUSTIFY_RIGHT = 1
    TEXT_JUSTIFY_CENTER = 2

    def __init__(self, main) -> None:

        self.main = main

        self.main_menu = MainMenu(main=self.main)

    @staticmethod
    def get_button_y_position(index: int) -> int:
        return -UI.MARGIN - (index * UI.BUTTON_Y_SIZE)
