import os
import re
import sys
import math
import datetime
import tkinter.filedialog
from typing import Union

import panda3d.core
import direct.task.Task
import direct.gui.DirectGui
import direct.gui.OnscreenText
import direct.gui.OnscreenImage
import direct.showbase.ShowBase

import car
import library.io


class ClickButton:

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
                        command=self.set_mouseover_style)

        self.frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                        command=self.set_mouseout_style)

    def set_mouseover_style(self, _) -> None:

        self.frame["frameColor"] = UI.WHITE
        self.frame["text_fg"] = UI.GREY

    def set_mouseout_style(self, _) -> None:

        self.frame["frameColor"] = UI.RED
        self.frame["text_fg"] = UI.WHITE


class BurgerButton:

    def __init__(self, position_x: int, position_y: int, size_x: int, size_y: int, bar_size_y: int,
                 callback_within: callable, parent) -> None:

        self.callback_within = callback_within

        self.background = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.TRANSPARENT,
                                             frameSize=(0, size_x, 0, -size_y),
                                             pos=(position_x, 0, position_y),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=parent))
        self.top_line = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                             frameSize=(0, size_x, 0, -bar_size_y),
                                             pos=(0, 0, 0),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.background))
        self.middle_line = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                             frameSize=(0, size_x, 0, -bar_size_y),
                                             pos=(0, 0, - (size_y / 2) + (bar_size_y / 2)),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.background))
        self.bottom_line = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                             frameSize=(0, size_x, 0, -bar_size_y),
                                             pos=(0, 0, -size_y + bar_size_y),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=self.background))
        self.set_invisible()

        self.background.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                             command=self.set_active)

    def set_active(self, _) -> None:

        if not MainMenu.inhibited:
            self.background["frameColor"] = UI.WHITE
            self.callback_within()

    def set_inactive(self) -> None:

        self.background["frameColor"] = UI.TRANSPARENT

    def set_invisible(self) -> None:

        self.background["frameColor"] = UI.TRANSPARENT
        self.top_line["frameColor"] = UI.TRANSPARENT
        self.middle_line["frameColor"] = UI.TRANSPARENT
        self.bottom_line["frameColor"] = UI.TRANSPARENT

    def set_visible(self) -> None:

        self.top_line["frameColor"] = UI.WHITE
        self.middle_line["frameColor"] = UI.WHITE
        self.bottom_line["frameColor"] = UI.WHITE


class CloseMenuButton:

    def __init__(self, size_x: int, size_y: int, callback_b1press: callable, parent) -> None:

        self.callback_b1press = callback_b1press

        self.frame = direct.gui.DirectGui.DirectFrame(frameColor=UI.TRANSPARENT,
                                                      frameSize=(0, size_x, 0, -size_y),
                                                      state=direct.gui.DirectGui.DGG.NORMAL,
                                                      parent=parent)

        self.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                        command=self.remove)

    def remove(self, _):

        self.frame.destroy()
        self.callback_b1press()


class MenuButton:

    def __init__(self, text: str, font, position_x: int, position_y: int, size_x: int, size_y: int, auto_event: bool,
                 icon_mouseover: str, icon_mouseout: str, image_pos_x: int, icon_size_x: int, icon_size_y: int,
                 text_pad_x: int, parent, callback_b1press: callable = None, callback_b1press_arg=None,
                 callback_mouseover: callable = None, callback_mouseover_arg=None,
                 callback_mouseout: callable = None, callback_mouseout_arg=None) -> None:

        self.auto_event = auto_event
        self.icon_mouseover = icon_mouseover
        self.icon_mouseout = icon_mouseout
        self.callback_b1press = callback_b1press
        self.callback_b1press_arg = callback_b1press_arg
        self.callback_mouseover = callback_mouseover
        self.callback_mouseover_arg = callback_mouseover_arg
        self.callback_mouseout = callback_mouseout
        self.callback_mouseout_arg = callback_mouseout_arg

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
                                                      image=self.icon_mouseout,
                                                      image_scale=(icon_size_x, 0, icon_size_y),
                                                      image_pos=(image_pos_x, 0, -UI.BUTTON_Y_SIZE / 2),
                                                      parent=parent)

        if self.callback_b1press:
            self.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                            command=self.do_b1press_actions)

        if callback_mouseover or auto_event:
            self.frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                            command=self.do_mouseover_actions)

        if callback_mouseout or auto_event:
            self.frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                            command=self.do_mouseout_actions)

    def do_b1press_actions(self, _) -> None:

        if self.callback_b1press:
            if self.callback_b1press_arg:
                self.callback_b1press(self.callback_b1press_arg)
            else:
                self.callback_b1press()

    def do_mouseover_actions(self, _) -> None:

        if self.auto_event:
            self.set_mouseover_style()

        if self.callback_mouseover:
            if self.callback_mouseover_arg:
                self.callback_mouseover(self.callback_mouseover_arg)
            else:
                self.callback_mouseover()

    def do_mouseout_actions(self, _) -> None:

        if self.auto_event:
            self.set_mouseout_style()

        if self.callback_mouseout:
            if self.callback_mouseout_arg:
                self.callback_mouseout(self.callback_mouseout_arg)
            else:
                self.callback_mouseout()

    def set_mouseover_style(self):

        self.frame["frameColor"] = UI.WHITE
        self.frame["text_fg"] = UI.GREY
        self.frame["image"] = self.icon_mouseover

    def set_mouseout_style(self):

        self.frame["frameColor"] = UI.RED
        self.frame["text_fg"] = UI.WHITE
        self.frame["image"] = self.icon_mouseout

    def remove(self):

        self.frame.destroy()


class ListButton:

    def __init__(self, text: str, font, position_x: int, position_y: int, size_x: int, size_y: int,
                 callback_b1press: callable, parent) -> None:

        self.frame = direct.gui.DirectGui.DirectFrame(text=text,
                                                      text_fg=UI.WHITE,
                                                      text_font=font,
                                                      text_scale=UI.FONT_SIZE,
                                                      text_align=UI.TEXT_JUSTIFY_LEFT,
                                                      text_pos=(0, (UI.FONT_SIZE / 2) - 3, 0),
                                                      frameColor=UI.RED,
                                                      frameSize=(0, size_x, 0, size_y),
                                                      pos=(position_x, 0, position_y),
                                                      state=direct.gui.DirectGui.DGG.NORMAL,
                                                      parent=parent)

        self.frame.bind(event=direct.gui.DirectGui.DGG.WITHIN,
                        command=self.set_mouseover_style)

        self.frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                        command=self.set_mouseout_style)

        self.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                        command=callback_b1press,
                        extraArgs=[self.frame["text"]])

    def set_mouseover_style(self, _) -> None:

        self.frame["frameColor"] = UI.WHITE
        self.frame["text_fg"] = UI.GREY

    def set_mouseout_style(self, _) -> None:

        self.frame["frameColor"] = UI.RED
        self.frame["text_fg"] = UI.WHITE


class CarItemButton:

    BORDER = 2
    PART_STATUS_INSTALLED = "INSTALLED"

    def __init__(self, text: str, font, paint_name: str, position_x: int, position_y: int, size_x: int, size_y: int,
                 callback_b1press: callable, callback_b1press_arg, parent) -> None:

        self.paint_name = paint_name
        self.item_is_installed = False

        self.frame = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.RED,
                                             text=text,
                                             text_fg=UI.WHITE,
                                             text_font=font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             text_pos=(UI.FONT_SIZE + 10, size_y - UI.FONT_SIZE - 5, 0),
                                             frameSize=(0, size_x, 0, size_y),
                                             pos=(position_x, 0, position_y),
                                             state=direct.gui.DirectGui.DGG.NORMAL,
                                             parent=parent))

        self.item_color_border = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                             frameSize=(0, UI.FONT_SIZE, 0, UI.FONT_SIZE),
                                             pos=(2, 0, (size_y - UI.FONT_SIZE) / 2),
                                             parent=self.frame))

        self.item_color = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.RED,
                                             frameSize=(0, UI.FONT_SIZE - (2 * CarItemButton.BORDER),
                                                        0, UI.FONT_SIZE - (2 * CarItemButton.BORDER)),
                                             pos=(2 + CarItemButton.BORDER, 0,
                                                  (size_y - UI.FONT_SIZE) / 2 + CarItemButton.BORDER),
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
                        command=self.set_mouseover_style)

        self.frame.bind(event=direct.gui.DirectGui.DGG.WITHOUT,
                        command=self.set_mouseout_style)

        self.frame.bind(event=direct.gui.DirectGui.DGG.B1PRESS,
                        command=callback_b1press,
                        extraArgs=[callback_b1press_arg])

    def set_mouseover_style(self, _) -> None:

        self.frame["frameColor"] = UI.WHITE
        self.frame["text_fg"] = UI.GREY

        self.status["text_bg"] = UI.WHITE
        self.status["text_fg"] = UI.GREY

        if not self.item_is_installed:
            self.item_color_border["frameColor"] = UI.TRANSPARENT
            self.item_color["frameColor"] = UI.TRANSPARENT

    def set_mouseout_style(self, _) -> None:

        self.frame["frameColor"] = UI.RED
        self.frame["text_fg"] = UI.WHITE

        self.status["text_bg"] = UI.RED
        self.status["text_fg"] = UI.WHITE

        if not self.item_is_installed:
            self.item_color_border["frameColor"] = UI.TRANSPARENT
            self.item_color["frameColor"] = UI.TRANSPARENT

    def update_item_status(self, item: car.Item) -> None:

        if item.model:

            self.item_is_installed = True
            self.status["text"] = CarItemButton.PART_STATUS_INSTALLED
            item_paint = item.model.findMaterial(self.paint_name)

            if item_paint:
                self.item_color["frameColor"] = item_paint.getBaseColor()
                self.item_color_border["frameColor"] = UI.WHITE
            else:
                self.item_color_border["frameColor"] = UI.TRANSPARENT
                self.item_color["frameColor"] = UI.TRANSPARENT

        else:

            self.item_is_installed = False
            self.status["text"] = ""
            self.item_color_border["frameColor"] = UI.TRANSPARENT
            self.item_color["frameColor"] = UI.TRANSPARENT


class CheckButton:

    def __init__(self, text: str, font, position_x: int, position_y: int, size_x: int, size_y: int,
                 callback_b1press: callable, parent) -> None:

        self.callback_b1press = callback_b1press
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
                        command=self.toggle)

    def toggle(self, _) -> None:

        if self.active:
            self.check_button["frameColor"] = UI.RED
            self.active = False
            self.callback_b1press(False)
        else:
            self.check_button["frameColor"] = UI.WHITE
            self.active = True
            self.callback_b1press(True)


class Paint:

    def __init__(self, color: Union[tuple, None], metallic: Union[float, None], brilliance: Union[float, None]) -> None:

        self.color = color
        self.metallic = metallic
        self.brilliance = brilliance


class PaintPreview:

    HAS_PAINT = ""
    HASNT_PAINT = "NO PAINT"
    BORDER = 3
    REGEX_COLOR_CODE = "^(?:[0-9a-fA-F]{2}){5}$"

    def __init__(self, font, position_x: int, position_y: int, size_x: int, size_y: int,
                 callback: callable, parent) -> None:

        self.callback = callback
        self.current_color_hex = "0" * 10

        self.border_frame = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                             frameSize=(0, size_x, 0, size_y),
                                             pos=(position_x, 0, position_y),
                                             parent=parent))

        self.paint_preview = (
            direct.gui.DirectGui.DirectFrame(frameColor=UI.WHITE,
                                             frameSize=(0, size_x - (2 * PaintPreview.BORDER),
                                                        0, size_y - PaintPreview.BORDER - 28),
                                             pos=(PaintPreview.BORDER, 0, PaintPreview.BORDER + 25),
                                             parent=self.border_frame))

        self.paint_code_entry = (
            direct.gui.DirectGui.DirectEntry(initialText=self.current_color_hex,
                                             text_fg=UI.GREY,
                                             entryFont=font,
                                             frameColor=UI.TRANSPARENT,
                                             numLines=1,
                                             scale=18,
                                             width=6,
                                             pos=((size_x / 2) - 48, 0, 6),
                                             command=self.get_user_entry,
                                             extraArgs=[],
                                             parent=self.border_frame))

        self.no_paint_label = (
            direct.gui.DirectGui.DirectLabel(text="",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_CENTER,
                                             pos=(size_x / 2, 0, (size_y / 2) + 6),
                                             parent=self.border_frame))

    def get_user_entry(self, paint_code: str) -> None:

        if bool(re.match(PaintPreview.REGEX_COLOR_CODE, paint_code)):

            new_paint_code_upper = paint_code.upper()
            self.paint_code_entry.set(new_paint_code_upper)
            self.current_color_hex = new_paint_code_upper

            new_paint = Paint(color=(self.hex_to_float(paint_code[:2]),
                                     self.hex_to_float(paint_code[2:4]),
                                     self.hex_to_float(paint_code[4:6])),
                              metallic=self.hex_to_float(paint_code[6:8]),
                              brilliance=self.hex_to_float(paint_code[8:10]))
            self.callback(paint=new_paint)

        else:

            self.paint_code_entry.set(self.current_color_hex)

    def update_paint(self, paint: Paint) -> None:

        if paint.color:

            self.no_paint_label["text"] = PaintPreview.HAS_PAINT
            self.paint_preview["frameColor"] = paint.color

            hex_color = ""
            for x in paint.color[:3]:
                hex_color += self.float_to_hex(x)
            hex_color += self.float_to_hex(paint.metallic)
            hex_color += self.float_to_hex(paint.brilliance)

            self.paint_code_entry.set(hex_color)

        else:

            self.no_paint_label["text"] = PaintPreview.HASNT_PAINT
            self.paint_preview["frameColor"] = UI.RED

            self.paint_code_entry.set("")

        self.current_color_hex = self.paint_code_entry.get()

    @staticmethod
    def float_to_hex(a: float) -> str:

        return hex(int(round(a * 255, 0)))[2:].upper().rjust(2, "0")

    @staticmethod
    def hex_to_float(a: str) -> float:

        return int(a, 16) / 255


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

            callback = None
            callback_arg = None

            if MainMenu.TEXT_CARS.lower() in content_path:
                callback = self.callback_load_car
                callback_arg = items[i][0]
            elif MainMenu.TEXT_WHEELS.lower() in content_path:
                callback = self.callback_load_wheels
                callback_arg = items[i][0]
            elif MainMenu.TEXT_GROUNDS.lower() in content_path:
                callback = self.callback_load_ground
                callback_arg = items[i][0]

            button = MenuButton(text=items[i][1],
                                font=self.main.font,
                                text_pad_x=SubMenu.TEXT_PADDING_LEFT,
                                position_x=UI.MARGIN + UI.BUTTON_Y_SIZE + MainMenu.MAIN_MENU_X_SIZE,
                                position_y=-UI.get_button_y_position(index=i),
                                size_x=self.menu_x_size, size_y=-UI.BUTTON_Y_SIZE,
                                image_pos_x=SubMenu.BUTTON_ICON_POS,
                                auto_event=True,
                                icon_mouseover=self.icon_mouseover,
                                icon_mouseout=self.icon_mouseout,
                                icon_size_x=MainMenu.BUTTON_ICON_SIZE_X,
                                icon_size_y=MainMenu.BUTTON_ICON_SIZE_Y,
                                callback_b1press=callback,
                                callback_b1press_arg=callback_arg,
                                parent=self.main.pixel2d)

            self.buttons.append(button)

    def callback_load_car(self, tag: str) -> None:

        self.main.car.load(tag=tag)

        Garage.car_ride_height_offset = 0
        Garage.car_pitch_offset = 0

    def callback_load_wheels(self, tag: str) -> None:

        self.main.car.load_wheels(tag=tag, oem=False)

    def callback_load_ground(self, tag: str) -> None:

        self.main.ground.change(tag=tag)

    def close(self) -> None:

        for button in self.buttons:
            button.frame.destroy()
        self.buttons = []


class MainMenu:

    TEXT_PADDING_LEFT = 60
    BUTTON_ICON_SIZE_X = 16
    BUTTON_ICON_SIZE_Y = 11
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

    inhibited = True

    def __init__(self, main) -> None:

        self.main = main

        self.close_main_menu_button = None
        self.menu_buttons = {}

        self.burger_menu = BurgerButton(position_x=UI.MARGIN,
                                        position_y=-UI.MARGIN,
                                        size_x=UI.BUTTON_Y_SIZE,
                                        size_y=UI.BUTTON_Y_SIZE,
                                        bar_size_y=MainMenu.MAIN_BUTTON_BAR_Y_SIZE,
                                        callback_within=self.callback_open_main_menu,
                                        parent=self.main.pixel2d)

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

    def callback_open_main_menu(self) -> None:

        if self.menu_buttons:
            return

        self.close_main_menu_button = CloseMenuButton(size_x=self.main.window_resolution[0],
                                                      size_y=self.main.window_resolution[1],
                                                      callback_b1press=self.close_main_menu,
                                                      parent=self.main.pixel2d)

        main_menu_buttons_data = [
            {"text": MainMenu.TEXT_CARS,
             "auto_event": False,
             "icon_mouseover": MainMenu.ICON_CARS_MOUSEOVER,
             "icon_mouseout": MainMenu.ICON_CARS_MOUSEOUT,
             "callback_b1press": None,
             "callback_mouseover": self.open_cars_submenu},
            {"text": MainMenu.TEXT_WHEELS,
             "auto_event": False,
             "icon_mouseover": MainMenu.ICON_WHEELS_MOUSEOVER,
             "icon_mouseout": MainMenu.ICON_WHEELS_MOUSEOUT,
             "callback_b1press": None,
             "callback_mouseover": self.open_wheels_submenu},
            {"text": MainMenu.TEXT_GROUNDS,
             "auto_event": False,
             "icon_mouseover": MainMenu.ICON_GROUNDS_MOUSEOVER,
             "icon_mouseout": MainMenu.ICON_GROUNDS_MOUSEOUT,
             "callback_b1press": None,
             "callback_mouseover": self.open_grounds_submenu},
            {"text": MainMenu.TEXT_GARAGE,
             "auto_event": True,
             "icon_mouseover": MainMenu.ICON_GARAGE_MOUSEOVER,
             "icon_mouseout": MainMenu.ICON_GARAGE_MOUSEOUT,
             "callback_b1press": self.display_garage,
             "callback_mouseover": self.close_all_submenus},
            {"text": MainMenu.TEXT_BODY_SHOP,
             "auto_event": True,
             "icon_mouseover": MainMenu.ICON_BODY_SHOP_MOUSEOVER,
             "icon_mouseout": MainMenu.ICON_BODY_SHOP_MOUSEOUT,
             "callback_b1press": self.display_body_shop,
             "callback_mouseover": self.close_all_submenus},
            # {"text": MainMenu.TEXT_SAVE_CAR,
            #  "auto_event": True,
            #  "icon_mouseover": MainMenu.ICON_SAVE_CAR_MOUSEOVER,
            #  "icon_mouseout": MainMenu.ICON_SAVE_CAR_MOUSEOUT,
            #  "callback_b1press": self.save_car,
            #  "callback_mouseover": self.close_all_submenus},
            # {"text": MainMenu.TEXT_LOAD_CAR,
            #  "auto_event": True,
            #  "icon_mouseover": MainMenu.ICON_LOAD_CAR_MOUSEOVER,
            #  "icon_mouseout": MainMenu.ICON_LOAD_CAR_MOUSEOUT,
            #  "callback_b1press": self.load,
            #  "callback_mouseover": self.close_all_submenus},
            {"text": MainMenu.TEXT_SAVE_IMAGE,
             "auto_event": True,
             "icon_mouseover": MainMenu.ICON_SAVE_IMAGE_MOUSEOVER,
             "icon_mouseout": MainMenu.ICON_SAVE_IMAGE_MOUSEOUT,
             "callback_b1press": self.save_image,
             "callback_mouseover": self.close_all_submenus},
            {"text": MainMenu.TEXT_AUTOROTATE,
             "auto_event": True,
             "icon_mouseover": MainMenu.ICON_AUTOROTATE_ON_MOUSEOVER,
             "icon_mouseout": MainMenu.ICON_AUTOROTATE_ON_MOUSEOUT,
             "callback_b1press": self.toggle_autorotate,
             "callback_mouseover": self.close_all_submenus},
            {"text": MainMenu.TEXT_EXIT,
             "auto_event": True,
             "icon_mouseover": MainMenu.ICON_EXIT_MOUSEOVER,
             "icon_mouseout": MainMenu.ICON_EXIT_MOUSEOUT,
             "callback_b1press": self.exit,
             "callback_mouseover": self.close_all_submenus}]

        for i, button in enumerate(main_menu_buttons_data):

            self.menu_buttons[button["text"]] = (
                MenuButton(text=button["text"],
                           font=self.main.font,
                           text_pad_x=MainMenu.TEXT_PADDING_LEFT,
                           position_x=UI.MARGIN + UI.BUTTON_Y_SIZE,
                           position_y=UI.MARGIN + (i * UI.BUTTON_Y_SIZE),
                           size_x=MainMenu.MAIN_MENU_X_SIZE,
                           size_y=-UI.BUTTON_Y_SIZE,
                           auto_event=button["auto_event"],
                           image_pos_x=MainMenu.BUTTON_ICON_POS,
                           icon_mouseover=button["icon_mouseover"],
                           icon_mouseout=button["icon_mouseout"],
                           icon_size_x=MainMenu.BUTTON_ICON_SIZE_X,
                           icon_size_y=MainMenu.BUTTON_ICON_SIZE_Y,
                           callback_b1press=button["callback_b1press"],
                           callback_mouseover=button["callback_mouseover"],
                           parent=self.main.pixel2d))

        self.update_autorotate_icon(b1press=False)

    def close_main_menu(self) -> None:

        self.close_all_submenus()

        for button in self.menu_buttons:
            self.menu_buttons[button].remove()
        self.menu_buttons = {}

        self.burger_menu.set_inactive()

    def open_cars_submenu(self) -> None:

        self.close_all_submenus()
        self.menu_buttons[MainMenu.TEXT_CARS].set_mouseover_style()
        self.submenu_cars.open(content_path=self.main.PATH_CARS)

    def close_cars_submenu(self) -> None:

        self.submenu_cars.close()

        if self.menu_buttons:
            self.menu_buttons[MainMenu.TEXT_CARS].set_mouseout_style()

    def open_wheels_submenu(self) -> None:

        self.close_all_submenus()
        self.menu_buttons[MainMenu.TEXT_WHEELS].set_mouseover_style()
        self.submenu_wheels.open(content_path=self.main.PATH_WHEELS)

    def close_wheels_submenu(self) -> None:

        self.submenu_wheels.close()

        if self.menu_buttons:
            self.menu_buttons[MainMenu.TEXT_WHEELS].set_mouseout_style()

    def open_grounds_submenu(self) -> None:

        self.close_all_submenus()
        self.menu_buttons[MainMenu.TEXT_GROUNDS].set_mouseover_style()
        self.submenu_grounds.open(content_path=self.main.PATH_GROUNDS)

    def close_grounds_submenu(self) -> None:

        self.submenu_grounds.close()

        if self.menu_buttons:
            self.menu_buttons[MainMenu.TEXT_GROUNDS].set_mouseout_style()

    def close_all_submenus(self) -> None:

        self.close_cars_submenu()
        self.close_wheels_submenu()
        self.close_grounds_submenu()

    def display_garage(self) -> None:

        self.close_main_menu_button.remove(None)
        self.close_main_menu()

        Garage(main=self.main)

    def display_body_shop(self) -> None:

        self.close_main_menu_button.remove(None)
        self.close_main_menu()

        BodyShop(main=self.main)

    def save_car(self) -> None:

        root = tkinter.Tk()
        root.iconify()

        path_to_car = tkinter.filedialog.asksaveasfile(mode="w",
                                                       title="Save car",
                                                       defaultextension=".pnc")

        self.close_main_menu()

    def load(self) -> None:

        root = tkinter.Tk()
        root.iconify()

        path_to_car = tkinter.filedialog.askopenfilename(title="Load a car (*.pnc)",
                                                         defaultextension=".pnc")

        self.close_main_menu()

    def save_image(self) -> None:

        self.close_main_menu_button.remove(None)
        self.close_main_menu()
        self.burger_menu.set_invisible()

        if not os.path.exists(path=self.main.PATH_SCREENSHOTS):
            os.mkdir(path=self.main.PATH_SCREENSHOTS)

        filename = os.path.basename(self.main.car.path) + datetime.datetime.now().strftime("_%Y%m%d_%H%M%S.png")
        fullpath = os.path.join(self.main.PATH_SCREENSHOTS, filename)

        self.main.graphicsEngine.renderFrame()
        self.main.graphicsEngine.renderFrame()
        direct.showbase.ShowBase.ShowBase.screenshot(self.main,
                                                     defaultFilename=False,
                                                     namePrefix=fullpath)
        self.burger_menu.set_visible()

    def toggle_autorotate(self) -> None:

        if self.main.autorotate:
            self.main.change_camera_rotation_mode()
        else:
            self.main.change_camera_rotation_mode()

        self.update_autorotate_icon(b1press=True)

        self.close_main_menu_button.remove(None)
        self.close_main_menu()

    def update_autorotate_icon(self, b1press: bool) -> None:

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

    @staticmethod
    def exit() -> None:

        sys.exit()


class SideWindow:

    def __init__(self, main, size_x: int, size_y: int) -> None:

        self.main = main

        self.frame = direct.gui.DirectGui.DirectFrame(frameColor=UI.RED,
                                                      frameSize=(0, size_x, 0, size_y),
                                                      pos=(self.main.window_resolution[0] - size_x, 0,
                                                           -size_y - ((self.main.window_resolution[1] - size_y) / 2)),
                                                      parent=self.main.pixel2d)

        self.button_done = ClickButton(main=self.main,
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
        MainMenu.inhibited = False


class Garage(SideWindow):

    SLIDER_SCALE = 80
    FRAME_X_SIZE = 390
    FRAME_Y_SIZE = 1080
    NB_ITEMS_SCROLLED_FRAME = 4
    CAR_PARAMETERS_FRAME_Y_SIZE = 103
    EXHAUST_PARAMETERS_FRAME_Y_SIZE = 139
    WHEELS_PARAMETERS_FRAME_Y_SIZE = 457
    BODYKITS_FRAME_Y_SIZE = 168

    car_ride_height_offset = 0
    car_pitch_offset = 0

    def __init__(self, main) -> None:

        MainMenu.inhibited = True

        super().__init__(main=main, size_x=self.FRAME_X_SIZE, size_y=self.FRAME_Y_SIZE)

        self.car_parameters_frame = None
        self.car_ride_height_slider = None
        self.car_pitch_slider = None

        self.exhaust_parameters_frame = None
        self.exhaust_horizontal_slider = None
        self.exhaust_vertical_slider = None
        self.exhaust_offset_slider = None

        self.wheels_parameters_frame = None
        self.wheels_diameter_slider = {}
        self.wheels_width_slider = {}
        self.wheels_offset_slider = {}
        self.wheels_camber_slider = {}
        self.wheels_toe_slider = {}

        self.bodykits_frame = None
        self.bodykits_buttons = []

        self.display_car_parameters()
        self.display_exhaust_parameters()
        self.display_wheels_parameters()
        self.display_bodykits()

    def display_car_parameters(self) -> None:

        self.car_parameters_frame = (
            direct.gui.DirectGui.DirectFrame(frameSize=(0, Garage.FRAME_X_SIZE - (2 * UI.MARGIN),
                                                        0, Garage.CAR_PARAMETERS_FRAME_Y_SIZE),
                                             pos=(UI.MARGIN, 0, Garage.FRAME_Y_SIZE
                                                  - UI.MARGIN - Garage.CAR_PARAMETERS_FRAME_Y_SIZE),
                                             frameColor=UI.RED,
                                             parent=self.frame))

        direct.gui.DirectGui.DirectLabel(text="Car",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_TITLE_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(0, 0, Garage.CAR_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE),
                                         parent=self.car_parameters_frame)

        direct.gui.DirectGui.DirectLabel(text="Ride Height",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              Garage.CAR_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              1 * (UI.MARGIN + UI.FONT_SIZE)),
                                         parent=self.car_parameters_frame)

        self.car_ride_height_slider = (
            direct.gui.DirectGui.DirectSlider(range=(-0.6, 0.6),
                                              value=self.main.car.nodepath.getPos()[2] - Garage.car_ride_height_offset,
                                              pageSize=0.02,
                                              pos=((Garage.FRAME_X_SIZE / 2) + 40, 0,
                                                   Garage.CAR_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                   1 * (UI.MARGIN + UI.FONT_SIZE) + 8),
                                              scale=Garage.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_car_ride_height,
                                              parent=self.car_parameters_frame))

        direct.gui.DirectGui.DirectLabel(text="Pitch",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              Garage.CAR_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              2 * (UI.MARGIN + UI.FONT_SIZE)),
                                         parent=self.car_parameters_frame)

        self.car_pitch_slider = (
            direct.gui.DirectGui.DirectSlider(range=(-6, 6),
                                              value=self.main.car.nodepath.getHpr()[1] - Garage.car_pitch_offset,
                                              pageSize=0.2,
                                              pos=((Garage.FRAME_X_SIZE / 2) + 40, 0,
                                                   Garage.CAR_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                   2 * (UI.MARGIN + UI.FONT_SIZE) + 8),
                                              scale=Garage.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_car_pitch,
                                              parent=self.car_parameters_frame))

    def display_exhaust_parameters(self) -> None:

        json_exhaust_position = self.main.car.json["chassis"]["position"]

        exhaust_tag = self.main.car.get_items_of_same_part_type(tag="exhaust")
        if exhaust_tag:
            exhaust_position = self.main.car.items[exhaust_tag[0]].model.getPos()
        else:
            exhaust_position = (0, 0, 0)

        self.exhaust_parameters_frame = (
            direct.gui.DirectGui.DirectFrame(frameSize=(0, Garage.FRAME_X_SIZE - (2 * UI.MARGIN),
                                                        0, Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE),
                                             pos=(UI.MARGIN, 0, Garage.FRAME_Y_SIZE -
                                                  (2 * UI.MARGIN) - Garage.CAR_PARAMETERS_FRAME_Y_SIZE -
                                                  UI.MARGIN - Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE),
                                             frameColor=UI.RED,
                                             parent=self.frame))

        direct.gui.DirectGui.DirectLabel(text="Exhaust",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_TITLE_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(0, 0, Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE),
                                         parent=self.exhaust_parameters_frame)

        direct.gui.DirectGui.DirectLabel(text="Horizontal",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              1 * (UI.MARGIN + UI.FONT_SIZE)),
                                         parent=self.exhaust_parameters_frame)

        self.exhaust_horizontal_slider = (
            direct.gui.DirectGui.DirectSlider(range=(json_exhaust_position[0] + 1, json_exhaust_position[0] - 1),
                                              value=exhaust_position[0],
                                              pageSize=0.02,
                                              pos=((Garage.FRAME_X_SIZE / 2) + 40, 0,
                                                   Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                   1 * (UI.MARGIN + UI.FONT_SIZE) + 8),
                                              scale=Garage.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_exhaust_horizontal,
                                              parent=self.exhaust_parameters_frame))

        direct.gui.DirectGui.DirectLabel(text="Vertical",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              2 * (UI.MARGIN + UI.FONT_SIZE)),
                                         parent=self.exhaust_parameters_frame)

        self.exhaust_vertical_slider = (
            direct.gui.DirectGui.DirectSlider(range=(json_exhaust_position[2] - 1, json_exhaust_position[2] + 1),
                                              value=exhaust_position[2],
                                              pageSize=0.02,
                                              pos=((Garage.FRAME_X_SIZE / 2) + 40, 0,
                                                   Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                   2 * (UI.MARGIN + UI.FONT_SIZE) + 8),
                                              scale=Garage.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_exhaust_offset,
                                              parent=self.exhaust_parameters_frame))

        direct.gui.DirectGui.DirectLabel(text="Offset",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              3 * (UI.MARGIN + UI.FONT_SIZE)),
                                         parent=self.exhaust_parameters_frame)

        self.exhaust_offset_slider = (
            direct.gui.DirectGui.DirectSlider(range=(json_exhaust_position[1] - 1, json_exhaust_position[1] + 1),
                                              value=exhaust_position[1],
                                              pageSize=0.02,
                                              pos=((Garage.FRAME_X_SIZE / 2) + 40, 0,
                                                   Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                   3 * (UI.MARGIN + UI.FONT_SIZE) + 8),
                                              scale=Garage.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_exhaust_vertical,
                                              parent=self.exhaust_parameters_frame))

    def display_wheels_parameters(self) -> None:

        self.wheels_parameters_frame = (
            direct.gui.DirectGui.DirectFrame(frameSize=(0, Garage.FRAME_X_SIZE - (2 * UI.MARGIN),
                                                        0, Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE),
                                             pos=(UI.MARGIN, 0, Garage.FRAME_Y_SIZE -
                                                  UI.MARGIN - Garage.CAR_PARAMETERS_FRAME_Y_SIZE -
                                                  (2 * UI.MARGIN) - Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE -
                                                  (2 * UI.MARGIN) - Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE),
                                             frameColor=UI.RED,
                                             parent=self.frame))

        for i, axle in enumerate(self.main.car.json["wheels"]):

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
                                             pos=(0, 0, Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE -
                                                  UI.FONT_TITLE_SIZE - 246 * i),
                                             parent=self.wheels_parameters_frame)

            direct.gui.DirectGui.DirectLabel(text="Diameter",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN, 0, Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE -
                                                  UI.FONT_TITLE_SIZE - 1 * (UI.MARGIN + UI.FONT_SIZE) - 246 * i),
                                             parent=self.wheels_parameters_frame)

            self.wheels_diameter_slider[axle] = (
                direct.gui.DirectGui.DirectSlider(range=(0.8 * json_wheel_diameter, 1.2 * json_wheel_diameter),
                                                  value=current_wheel_diameter,
                                                  pageSize=0.05,
                                                  pos=((Garage.FRAME_X_SIZE / 2) + 40, 0,
                                                       Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                       1 * (UI.MARGIN + UI.FONT_SIZE) - (246 * i) + 8),
                                                  scale=Garage.SLIDER_SCALE,
                                                  color=UI.WHITE,
                                                  thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                                  thumb_color=UI.WHITE,
                                                  command=self.callback_update_wheel_diameter,
                                                  extraArgs=[axle],
                                                  parent=self.wheels_parameters_frame))

            direct.gui.DirectGui.DirectLabel(text="Width",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN, 0, Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE -
                                                  UI.FONT_TITLE_SIZE - 2 * (UI.MARGIN + UI.FONT_SIZE) - 246 * i),
                                             parent=self.wheels_parameters_frame)

            self.wheels_width_slider[axle] = (
                direct.gui.DirectGui.DirectSlider(range=(0.4 * json_wheel_width, 1.6 * json_wheel_width),
                                                  value=current_wheel_width,
                                                  pageSize=0.1,
                                                  pos=((Garage.FRAME_X_SIZE / 2) + 40, 0,
                                                       Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                       2 * (UI.MARGIN + UI.FONT_SIZE) - (246 * i) + 8),
                                                  scale=Garage.SLIDER_SCALE,
                                                  color=UI.WHITE,
                                                  thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                                  thumb_color=UI.WHITE,
                                                  command=self.callback_update_wheel_width,
                                                  extraArgs=[axle],
                                                  parent=self.wheels_parameters_frame))

            direct.gui.DirectGui.DirectLabel(text="Offset",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN, 0, Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE -
                                                  UI.FONT_TITLE_SIZE - 3 * (UI.MARGIN + UI.FONT_SIZE) - 246 * i),
                                             parent=self.wheels_parameters_frame)

            self.wheels_offset_slider[axle] = (
                direct.gui.DirectGui.DirectSlider(range=(0.66 * json_wheel_offset, 1.34 * json_wheel_offset),
                                                  value=current_wheel_offset,
                                                  pageSize=0.02,
                                                  pos=((Garage.FRAME_X_SIZE / 2) + 40, 0,
                                                       Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                       3 * (UI.MARGIN + UI.FONT_SIZE) - (246 * i) + 8),
                                                  scale=Garage.SLIDER_SCALE,
                                                  color=UI.WHITE,
                                                  thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                                  thumb_color=UI.WHITE,
                                                  command=self.callback_update_wheel_offset,
                                                  extraArgs=[axle],
                                                  parent=self.wheels_parameters_frame))

            direct.gui.DirectGui.DirectLabel(text="Camber",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN, 0, Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE -
                                                  UI.FONT_TITLE_SIZE - 4 * (UI.MARGIN + UI.FONT_SIZE) - 246 * i),
                                             parent=self.wheels_parameters_frame)

            self.wheels_camber_slider[axle] = (
                direct.gui.DirectGui.DirectSlider(range=(json_wheel_camber - 45, json_wheel_camber + 45),
                                                  value=current_wheel_camber,
                                                  pageSize=0.5,
                                                  pos=((Garage.FRAME_X_SIZE / 2) + 40, 0,
                                                       Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                       4 * (UI.MARGIN + UI.FONT_SIZE) - (246 * i) + 8),
                                                  scale=Garage.SLIDER_SCALE,
                                                  color=UI.WHITE,
                                                  thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                                  thumb_color=UI.WHITE,
                                                  command=self.callback_update_wheel_camber,
                                                  extraArgs=[axle],
                                                  parent=self.wheels_parameters_frame))

            direct.gui.DirectGui.DirectLabel(text="Toe",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(UI.MARGIN, 0, Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE -
                                                  UI.FONT_TITLE_SIZE - 5 * (UI.MARGIN + UI.FONT_SIZE) - 246 * i),
                                             parent=self.wheels_parameters_frame)

            self.wheels_toe_slider[axle] = (
                direct.gui.DirectGui.DirectSlider(range=(json_wheel_toe - 10, json_wheel_toe + 10),
                                                  value=current_wheel_toe,
                                                  pageSize=0.3,
                                                  pos=((Garage.FRAME_X_SIZE / 2) + 40, 0,
                                                       Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                       5 * (UI.MARGIN + UI.FONT_SIZE) - (246 * i) + 8),
                                                  scale=Garage.SLIDER_SCALE,
                                                  color=UI.WHITE,
                                                  thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                                  thumb_color=UI.WHITE,
                                                  command=self.callback_update_wheel_toe,
                                                  extraArgs=[axle],
                                                  parent=self.wheels_parameters_frame))

    def display_bodykits(self) -> None:

        nb_bodykits = len(self.main.car.json["bodykits"])

        self.bodykits_frame = (
            direct.gui.DirectGui.DirectFrame(frameSize=(0, Garage.FRAME_X_SIZE - (2 * UI.MARGIN),
                                                        0, Garage.BODYKITS_FRAME_Y_SIZE),
                                             pos=(UI.MARGIN, 0, Garage.FRAME_Y_SIZE -
                                                  UI.MARGIN - Garage.CAR_PARAMETERS_FRAME_Y_SIZE -
                                                  (2 * UI.MARGIN) - Garage.EXHAUST_PARAMETERS_FRAME_Y_SIZE -
                                                  (2 * UI.MARGIN) - Garage.WHEELS_PARAMETERS_FRAME_Y_SIZE -
                                                  (2 * UI.MARGIN) - Garage.BODYKITS_FRAME_Y_SIZE),
                                             frameColor=UI.RED,
                                             parent=self.frame))

        direct.gui.DirectGui.DirectLabel(text="Bodykits",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_TITLE_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(0, 0, Garage.BODYKITS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE),
                                         parent=self.bodykits_frame)

        bodykits_list_frame = (
            direct.gui.DirectGui.DirectScrolledFrame(canvasSize=(0, Garage.FRAME_X_SIZE - (4 * UI.MARGIN),
                                                                 0, UI.BUTTON_Y_SIZE * nb_bodykits),
                                                     frameSize=(0, Garage.FRAME_X_SIZE - (2 * UI.MARGIN),
                                                                0, UI.BUTTON_Y_SIZE * Garage.NB_ITEMS_SCROLLED_FRAME),
                                                     pos=(0, 0,
                                                          Garage.BODYKITS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE - UI.MARGIN
                                                          - (Garage.NB_ITEMS_SCROLLED_FRAME * UI.BUTTON_Y_SIZE)),
                                                     frameColor=UI.RED,
                                                     scrollBarWidth=UI.MARGIN * 1.5,
                                                     verticalScroll_color=UI.WHITE,
                                                     verticalScroll_incButton_relief=False,
                                                     verticalScroll_decButton_relief=False,
                                                     parent=self.bodykits_frame))

        for i in range(len(self.main.car.json["bodykits"])):

            bodykit_button = ListButton(text=self.main.car.json["bodykits"][i]["name"],
                                        font=self.main.font,
                                        position_x=UI.MARGIN,
                                        position_y=(UI.BUTTON_Y_SIZE * (nb_bodykits - 1)) - (UI.BUTTON_Y_SIZE * i),
                                        size_x=Garage.FRAME_X_SIZE - 2 * UI.MARGIN,
                                        size_y=UI.BUTTON_Y_SIZE,
                                        callback_b1press=self.callback_load_bodykit,
                                        parent=bodykits_list_frame.getCanvas())

            self.bodykits_buttons.append(bodykit_button)

    def callback_update_car_ride_height(self) -> None:

        current_car_position = self.main.car.nodepath.getPos()

        self.main.car.nodepath.setPos((current_car_position[0],
                                       current_car_position[1],
                                       self.car_ride_height_slider["value"] + Garage.car_ride_height_offset))

    def callback_update_car_pitch(self) -> None:

        current_car_rotation = self.main.car.nodepath.getHpr()

        self.main.car.nodepath.setHpr((current_car_rotation[0],
                                       self.car_pitch_slider["value"] + Garage.car_pitch_offset,
                                       current_car_rotation[2]))

    def callback_update_exhaust_horizontal(self) -> None:

        exhaust_tag = self.main.car.get_items_of_same_part_type(tag="exhaust")

        if exhaust_tag:
            exhaust_item = self.main.car.items[exhaust_tag[0]]
            exhaust_item.model.set_x(self.exhaust_horizontal_slider["value"])

    def callback_update_exhaust_vertical(self) -> None:

        exhaust_tag = self.main.car.get_items_of_same_part_type(tag="exhaust")

        if exhaust_tag:
            exhaust_item = self.main.car.items[exhaust_tag[0]]
            exhaust_item.model.set_y(self.exhaust_offset_slider["value"])

    def callback_update_exhaust_offset(self) -> None:

        exhaust_tag = self.main.car.get_items_of_same_part_type(tag="exhaust")

        if exhaust_tag:
            exhaust_item = self.main.car.items[exhaust_tag[0]]
            exhaust_item.model.set_z(self.exhaust_vertical_slider["value"])

    def callback_update_wheel_diameter(self, axle: str) -> None:

        diameter_slider_value = self.wheels_diameter_slider[axle]["value"]

        for i in range(len(self.main.car.json["wheels"][axle])):

            wheels_pos_json = self.main.car.json["wheels"][axle][i]["position"]
            wheels_scale_json = self.main.car.json["wheels"][axle][i]["scale"]
            current_wheel_scale = self.main.car.items["wheels"][axle][i].model.getScale()

            self.main.car.items["wheels"][axle][i].model.setScale(
                (current_wheel_scale[0],
                 diameter_slider_value,
                 diameter_slider_value))

            wheels_new_height = wheels_pos_json[2] * (diameter_slider_value / wheels_scale_json[2])
            wheels_current_position = self.main.car.items["wheels"][axle][i].model.getPos()
            self.main.car.items["wheels"][axle][i].model.setPos(
                (wheels_current_position[0],
                 wheels_current_position[1],
                 wheels_new_height))
            self.main.car.items[axle + "brakes"][i].model.setPos(self.main.car.items["wheels"][axle][i].model.getPos())

            self.update_car_ride_height_pitch_offsets()
            self.callback_update_car_ride_height()
            self.callback_update_car_pitch()

    def update_car_ride_height_pitch_offsets(self):

        if list(self.main.car.items["wheels"].keys()) == ['front', 'rear']:

            wheels_front_height = self.main.car.items["wheels"]["front"][0].model.getPos()[2]
            wheels_front_height_json = self.main.car.json["wheels"]["front"][0]["position"][2]
            wheels_rear_height = self.main.car.items["wheels"]["rear"][0].model.getPos()[2]
            wheels_rear_height_json = self.main.car.json["wheels"]["rear"][0]["position"][2]
            car_wheelbase = (math.fabs(self.main.car.json["wheels"]["front"][0]["position"][1]) +
                             math.fabs(self.main.car.json["wheels"]["rear"][0]["position"][1]))

            Garage.car_ride_height_offset = ((wheels_rear_height - wheels_rear_height_json)
                                             + (wheels_front_height - wheels_front_height_json)) / 2
            Garage.car_pitch_offset = 2 * math.degrees(
                math.atan(((wheels_rear_height - wheels_front_height) / car_wheelbase)))

    def callback_update_wheel_width(self, axle: str) -> None:

        for i in range(len(self.main.car.items["wheels"][axle])):

            current_wheel_scale = self.main.car.items["wheels"][axle][i].model.getScale()

            self.main.car.items["wheels"][axle][i].model.setScale((self.wheels_width_slider[axle]["value"],
                                                                   current_wheel_scale[1],
                                                                   current_wheel_scale[2]))

    def callback_update_wheel_offset(self, axle: str) -> None:

        for i in range(len(self.main.car.items["wheels"][axle])):

            current_wheel_position = self.main.car.items["wheels"][axle][i].model.getPos()

            self.main.car.items["wheels"][axle][i].model.setPos((math.copysign(self.wheels_offset_slider[axle]["value"],
                                                                               current_wheel_position[0]),
                                                                 current_wheel_position[1],
                                                                 current_wheel_position[2]))
            self.main.car.items[axle + "brakes"][i].model.setPos(self.main.car.items["wheels"][axle][i].model.getPos())

    def callback_update_wheel_camber(self, axle: str) -> None:

        for i in range(len(self.main.car.items["wheels"][axle])):

            current_wheel_rotation = self.main.car.items["wheels"][axle][i].model.getHpr()

            if current_wheel_rotation[2] > 90:
                new_wheel_camber = 180 - self.wheels_camber_slider[axle]["value"]
            else:
                new_wheel_camber = self.wheels_camber_slider[axle]["value"]

            self.main.car.items["wheels"][axle][i].model.setHpr((current_wheel_rotation[0],
                                                                 current_wheel_rotation[1],
                                                                 new_wheel_camber))

            new_wheel_camber = new_wheel_camber - 180 if current_wheel_rotation[2] > 90 else new_wheel_camber
            current_brakes_rotation = self.main.car.items[axle + "brakes"][i].model.getHpr()
            self.main.car.items[axle + "brakes"][i].model.setHpr(current_brakes_rotation[0],
                                                                 current_brakes_rotation[1],
                                                                 new_wheel_camber)

    def callback_update_wheel_toe(self, axle: str) -> None:

        for i in range(len(self.main.car.items["wheels"][axle])):

            current_wheel_rotation = self.main.car.items["wheels"][axle][i].model.getHpr()

            if current_wheel_rotation[2] > 90:
                new_wheel_toe = - self.wheels_toe_slider[axle]["value"]
            else:
                new_wheel_toe = self.wheels_toe_slider[axle]["value"]

            self.main.car.items["wheels"][axle][i].model.setHpr((new_wheel_toe,
                                                                 current_wheel_rotation[1],
                                                                 current_wheel_rotation[2]))

            current_brakes_rotation = self.main.car.items[axle + "brakes"][i].model.getHpr()
            self.main.car.items[axle + "brakes"][i].model.setHpr(new_wheel_toe,
                                                                 current_brakes_rotation[1],
                                                                 current_brakes_rotation[2])

    def callback_load_bodykit(self, name: str, _) -> None:

        self.main.car.load_bodykit(bodykit=name)


class BodyShop(SideWindow):

    SLIDER_SCALE = 80
    FRAME_X_SIZE = 500
    FRAME_Y_SIZE = 840
    CAR_ITEMS_FRAME_Y_SIZE = 424
    PAINT_SELECTOR_FRAME_Y_SIZE = 286
    SLIDER_PAGE_SIZE = (1 / 256) * 6
    NB_ITEMS_SCROLLED_FRAME = 12
    PAINT_ALL = "ALL"
    PAINT_NONE = "NONE"

    def __init__(self, main) -> None:

        MainMenu.inhibited = True

        super().__init__(main=main, size_x=BodyShop.FRAME_X_SIZE, size_y=BodyShop.FRAME_Y_SIZE)

        self.car_items_frame = None
        self.car_items_buttons = []

        self.paint_selector_frame = None
        self.paint_metallic_slider = None
        self.paint_brilliance_slider = None
        self.paint_red_slider = None
        self.paint_green_slider = None
        self.paint_blue_slider = None
        self.paint_preview = None
        self.paint_all_car_items_checkbutton = None

        self.selected_tag_to_paint = "chassis"
        self.selected_item_label = None

        self.display_car_items()
        self.display_paint_selector()

    def display_car_items(self) -> None:

        nb_car_items = len(self.main.car.items)

        self.car_items_frame = (
            direct.gui.DirectGui.DirectFrame(frameSize=(0, BodyShop.FRAME_X_SIZE - (2 * UI.MARGIN),
                                                        0, BodyShop.CAR_ITEMS_FRAME_Y_SIZE),
                                             pos=(UI.MARGIN, 0,
                                                  BodyShop.FRAME_Y_SIZE - BodyShop.CAR_ITEMS_FRAME_Y_SIZE - UI.MARGIN),
                                             frameColor=UI.RED,
                                             parent=self.frame))

        direct.gui.DirectGui.DirectLabel(text="Car Items",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_TITLE_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(0, 0, BodyShop.CAR_ITEMS_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE),
                                         parent=self.car_items_frame)

        car_items_scolledframe = (
            direct.gui.DirectGui.DirectScrolledFrame(canvasSize=(0, BodyShop.FRAME_X_SIZE - (4 * UI.MARGIN),
                                                                 0, UI.BUTTON_Y_SIZE * nb_car_items),
                                                     frameSize=(0, BodyShop.FRAME_X_SIZE - (2 * UI.MARGIN), 0,
                                                                UI.BUTTON_Y_SIZE * BodyShop.NB_ITEMS_SCROLLED_FRAME),
                                                     pos=(0, 0, BodyShop.CAR_ITEMS_FRAME_Y_SIZE -
                                                          (BodyShop.NB_ITEMS_SCROLLED_FRAME * UI.BUTTON_Y_SIZE) -
                                                          UI.FONT_TITLE_SIZE - UI.MARGIN),
                                                     frameColor=UI.RED,
                                                     scrollBarWidth=UI.MARGIN * 1.5,
                                                     verticalScroll_color=UI.WHITE,
                                                     verticalScroll_incButton_relief=False,
                                                     verticalScroll_decButton_relief=False,
                                                     parent=self.car_items_frame))

        for i, tag in enumerate(self.main.car.items):

            if self.main.car.is_wheel(tag=tag):
                item = self.main.car.get_first_wheel()
            elif self.main.car.is_brake(tag=tag):
                item = self.main.car.get_first_brake(tag=tag)
            else:
                item = self.main.car.items[tag]

            car_item_button = CarItemButton(text=item.name,
                                            font=self.main.font,
                                            paint_name=self.main.GLB_PAINT_NAME,
                                            position_x=UI.MARGIN,
                                            position_y=(UI.BUTTON_Y_SIZE * (nb_car_items - 1)) - (UI.BUTTON_Y_SIZE * i),
                                            size_x=BodyShop.FRAME_X_SIZE - 2 * UI.MARGIN,
                                            size_y=UI.BUTTON_Y_SIZE,
                                            callback_b1press=self.callback_load_car_item,
                                            callback_b1press_arg=tag,
                                            parent=car_items_scolledframe.getCanvas())

            car_item_button.update_item_status(item=item)

            self.car_items_buttons.append(car_item_button)

    def display_paint_selector(self) -> None:

        chassis_paint = self.get_paint(item=self.main.car.items["chassis"])

        self.paint_selector_frame = (
            direct.gui.DirectGui.DirectFrame(frameSize=(0, BodyShop.FRAME_X_SIZE - (2 * UI.MARGIN),
                                                        0, BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE),
                                             pos=(UI.MARGIN, 0,
                                                  BodyShop.FRAME_Y_SIZE - UI.MARGIN - BodyShop.CAR_ITEMS_FRAME_Y_SIZE -
                                                  (2 * UI.MARGIN) - BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE),
                                             frameColor=UI.RED,
                                             parent=self.frame))

        direct.gui.DirectGui.DirectLabel(text="Paint",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_TITLE_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(0, 0, BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE),
                                         parent=self.paint_selector_frame)

        direct.gui.DirectGui.DirectLabel(text="Selected part :",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              UI.MARGIN - UI.FONT_SIZE),
                                         parent=self.paint_selector_frame)

        self.selected_item_label = (
            direct.gui.DirectGui.DirectLabel(text="",
                                             text_fg=UI.WHITE,
                                             text_bg=UI.RED,
                                             text_font=self.main.font,
                                             text_scale=UI.FONT_SIZE,
                                             text_align=UI.TEXT_JUSTIFY_LEFT,
                                             pos=(168, 0,
                                                  BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                  UI.MARGIN - UI.FONT_SIZE),
                                             parent=self.paint_selector_frame))
        self.selected_item_label["text"] = self.main.car.items[self.selected_tag_to_paint].name

        direct.gui.DirectGui.DirectLabel(text="Red",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              2 * (UI.MARGIN + UI.FONT_SIZE)),
                                         parent=self.paint_selector_frame)

        self.paint_red_slider = (
            direct.gui.DirectGui.DirectSlider(range=(0, 1),
                                              value=chassis_paint.color[0],
                                              pageSize=BodyShop.SLIDER_PAGE_SIZE,
                                              pos=(BodyShop.FRAME_X_SIZE / 2, 0,
                                                   BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                   2 * (UI.MARGIN + UI.FONT_SIZE) + 8),
                                              scale=BodyShop.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_paint,
                                              parent=self.paint_selector_frame))

        direct.gui.DirectGui.DirectLabel(text="Green",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              3 * (UI.MARGIN + UI.FONT_SIZE)),
                                         parent=self.paint_selector_frame)

        self.paint_green_slider = (
            direct.gui.DirectGui.DirectSlider(range=(0, 1),
                                              value=chassis_paint.color[1],
                                              pageSize=BodyShop.SLIDER_PAGE_SIZE,
                                              pos=(BodyShop.FRAME_X_SIZE / 2, 0,
                                                   BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                   3 * (UI.MARGIN + UI.FONT_SIZE) + 8),
                                              scale=BodyShop.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_paint,
                                              parent=self.paint_selector_frame))

        direct.gui.DirectGui.DirectLabel(text="Blue",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              4 * (UI.MARGIN + UI.FONT_SIZE)),
                                         parent=self.paint_selector_frame)

        self.paint_blue_slider = (
            direct.gui.DirectGui.DirectSlider(range=(0, 1),
                                              value=chassis_paint.color[2],
                                              pageSize=BodyShop.SLIDER_PAGE_SIZE,
                                              pos=(BodyShop.FRAME_X_SIZE / 2, 0,
                                                   BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                   4 * (UI.MARGIN + UI.FONT_SIZE) + 8),
                                              scale=BodyShop.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_paint,
                                              parent=self.paint_selector_frame))

        direct.gui.DirectGui.DirectLabel(text="Metallic",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              5 * (UI.MARGIN + UI.FONT_SIZE)),
                                         parent=self.paint_selector_frame)

        self.paint_metallic_slider = (
            direct.gui.DirectGui.DirectSlider(range=(0, 1),
                                              value=chassis_paint.metallic,
                                              pageSize=BodyShop.SLIDER_PAGE_SIZE,
                                              pos=(BodyShop.FRAME_X_SIZE / 2, 0,
                                                   BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                   5 * (UI.MARGIN + UI.FONT_SIZE) + 8),
                                              scale=BodyShop.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_paint,
                                              parent=self.paint_selector_frame))

        direct.gui.DirectGui.DirectLabel(text="Brilliance",
                                         text_fg=UI.WHITE,
                                         text_bg=UI.RED,
                                         text_font=self.main.font,
                                         text_scale=UI.FONT_SIZE,
                                         text_align=UI.TEXT_JUSTIFY_LEFT,
                                         pos=(UI.MARGIN, 0,
                                              BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                              6 * (UI.MARGIN + UI.FONT_SIZE)),
                                         parent=self.paint_selector_frame)

        self.paint_brilliance_slider = (
            direct.gui.DirectGui.DirectSlider(range=(0, 1),
                                              value=chassis_paint.brilliance,
                                              pageSize=BodyShop.SLIDER_PAGE_SIZE,
                                              pos=(BodyShop.FRAME_X_SIZE / 2, 0,
                                                   BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE -
                                                   6 * (UI.MARGIN + UI.FONT_SIZE) + 8),
                                              scale=BodyShop.SLIDER_SCALE,
                                              color=UI.WHITE,
                                              thumb_relief=direct.gui.DirectGui.DGG.FLAT,
                                              thumb_color=UI.WHITE,
                                              command=self.callback_update_paint,
                                              parent=self.paint_selector_frame))

        self.paint_preview = PaintPreview(font=self.main.font,
                                          position_x=BodyShop.FRAME_X_SIZE - 132,
                                          position_y=64,
                                          size_x=100,
                                          size_y=125,
                                          callback=self.callback_update_paint_sliders,
                                          parent=self.paint_selector_frame)

        self.paint_all_car_items_checkbutton = (
            CheckButton(text="Paint all car parts (except wheels)",
                        font=self.main.font,
                        position_x=UI.MARGIN + 2,
                        position_y=BodyShop.PAINT_SELECTOR_FRAME_Y_SIZE - UI.FONT_TITLE_SIZE - 7 * (
                                UI.MARGIN + UI.FONT_SIZE) - 10,
                        size_x=BodyShop.FRAME_X_SIZE - 4 * UI.MARGIN,
                        size_y=UI.BUTTON_Y_SIZE,
                        callback_b1press=self.callback_toggle_paint_all,
                        parent=self.paint_selector_frame))

    def callback_toggle_paint_all(self, active: bool) -> None:

        if active:
            self.selected_item_label["text"] = BodyShop.PAINT_ALL
            self.selected_tag_to_paint = None
        else:
            self.selected_item_label["text"] = BodyShop.PAINT_NONE

    def callback_load_car_item(self, tag: str, _) -> None:

        self.main.car.load_part(tag=tag)

        if self.paint_all_car_items_checkbutton.active:

            self.selected_item_label["text"] = BodyShop.PAINT_ALL
            self.selected_tag_to_paint = None
            current_paint = self.get_paint(item=self.main.car.items["chassis"])

        else:

            self.selected_tag_to_paint = tag

            if self.main.car.is_wheel(tag=tag):
                self.selected_item_label["text"] = self.main.car.get_first_wheel().name
                current_paint = self.get_paint(item=self.main.car.get_first_wheel())
            elif self.main.car.is_brake(tag=tag):
                self.selected_item_label["text"] = self.main.car.get_first_brake(tag=tag).name
                current_paint = self.get_paint(item=self.main.car.get_first_brake(tag=tag))
            else:
                self.selected_item_label["text"] = self.main.car.items[tag].name
                current_paint = self.get_paint(item=self.main.car.items[tag])

        self.callback_update_paint_sliders(paint=current_paint)
        self.paint_preview.update_paint(paint=current_paint)

        self.refresh_ui_car_items_buttons()

    def callback_update_paint(self) -> None:

        new_paint = Paint(color=(self.paint_red_slider["value"],
                                 self.paint_green_slider["value"],
                                 self.paint_blue_slider["value"], 1),
                          metallic=self.paint_metallic_slider["value"],
                          brilliance=self.paint_brilliance_slider["value"])

        self.paint_preview.update_paint(paint=new_paint)

        if self.paint_all_car_items_checkbutton.active:

            for tag in self.main.car.items:
                if not self.main.car.is_wheel(tag=tag) and not self.main.car.is_brake(tag=tag):
                    self.set_paint(item=self.main.car.items[tag], paint=new_paint)
        else:

            if self.selected_tag_to_paint:

                if self.main.car.is_wheel(tag=self.selected_tag_to_paint):
                    for axle in self.main.car.items["wheels"]:
                        for wheel in self.main.car.items["wheels"][axle]:
                            self.set_paint(item=wheel, paint=new_paint)
                elif self.main.car.is_brake(tag=self.selected_tag_to_paint):
                    for brake in self.main.car.items[self.selected_tag_to_paint]:
                        self.set_paint(item=brake, paint=new_paint)
                else:
                    self.set_paint(item=self.main.car.items[self.selected_tag_to_paint], paint=new_paint)

        self.refresh_ui_car_items_buttons()

    def refresh_ui_car_items_buttons(self) -> None:

        for i, tag in enumerate(self.main.car.items):

            if self.main.car.is_wheel(tag=tag):
                item = self.main.car.get_first_wheel()
            elif self.main.car.is_brake(tag=tag):
                item = self.main.car.get_first_brake(tag=tag)
            else:
                item = self.main.car.items[tag]

            self.car_items_buttons[i].update_item_status(item=item)

    def callback_update_paint_sliders(self, paint: Paint) -> None:

        if paint.color:
            self.paint_red_slider["value"] = paint.color[0]
            self.paint_green_slider["value"] = paint.color[1]
            self.paint_blue_slider["value"] = paint.color[2]
            self.paint_metallic_slider["value"] = paint.metallic
            self.paint_brilliance_slider["value"] = paint.brilliance

    def set_paint(self, item: car.Item, paint: Paint) -> None:

        if item:
            if item.model:
                paint_found = item.model.findMaterial(self.main.GLB_PAINT_NAME)
                if paint_found:
                    paint_found.setBaseColor(paint.color)
                    paint_found.setMetallic(paint.metallic)
                    paint_found.setRoughness(1 - paint.brilliance)

    def get_paint(self, item: car.Item) -> Paint:

        result = Paint(color=None, metallic=None, brilliance=None)

        if item:
            if item.model:
                paint = item.model.findMaterial(self.main.GLB_PAINT_NAME)
                if paint:
                    return Paint(color=tuple(paint.getBaseColor()),
                                 metallic=paint.getMetallic(),
                                 brilliance=1 - paint.getRoughness())

        return result


class SplashScreen:

    WAIT_IN_DURATION = 0.6
    FADE_IN_DURATION = 0.1
    DISPLAY_DURATION = 2
    FADE_OUT_DURATION = 0.2
    WAIT_OUT_DURATION = 1

    T1 = WAIT_IN_DURATION
    T2 = T1 + FADE_IN_DURATION
    T3 = T2 + DISPLAY_DURATION
    T4 = T3 + FADE_OUT_DURATION
    T5 = T4 + WAIT_OUT_DURATION

    BACKGROUND_SCALE = 2
    PROJECTNAER_LOGO_SCALE = 0.48
    PANDA3D_LOGO_SCALE = 0.3

    BACKGROUND_IMAGE = "content/images/ui/splashscreen/background.png"
    PROJECTNAER_LOGO = "content/images/ui/splashscreen/project_naer_logo.png"
    PANDA3D_LOGO = "content/images/ui/splashscreen/panda3d_logo.png"

    def __init__(self, main) -> None:

        self.main = main

        self.background = (
            direct.gui.OnscreenImage.OnscreenImage(image=SplashScreen.BACKGROUND_IMAGE,
                                                   pos=(0, 0, 0),
                                                   scale=(SplashScreen.BACKGROUND_SCALE, 1,
                                                          9 / 16 * SplashScreen.BACKGROUND_SCALE),
                                                   parent=self.main.aspect2d))

        self.projectnaer_logo = (
            direct.gui.OnscreenImage.OnscreenImage(image=SplashScreen.PROJECTNAER_LOGO,
                                                   pos=(0, 0, 0.3),
                                                   scale=(SplashScreen.PROJECTNAER_LOGO_SCALE, 1,
                                                          SplashScreen.PROJECTNAER_LOGO_SCALE),
                                                   parent=self.main.aspect2d))
        self.projectnaer_logo.setTransparency(panda3d.core.TransparencyAttrib.MAlpha)

        self.projectnaer_text = (
            direct.gui.OnscreenText.OnscreenText(text="LOADING...",
                                                 fg=UI.WHITE,
                                                 font=self.main.font,
                                                 pos=(0.05, -0.3),
                                                 scale=0.07))

        self.panda3d_text = (
            direct.gui.OnscreenText.OnscreenText(text="POWERED BY",
                                                 fg=UI.WHITE,
                                                 font=self.main.font,
                                                 pos=(0.04, -0.70),
                                                 scale=0.03))

        self.panda3d_logo = (
            direct.gui.OnscreenImage.OnscreenImage(image=SplashScreen.PANDA3D_LOGO,
                                                   pos=(0, 0, -0.77),
                                                   scale=(SplashScreen.PANDA3D_LOGO_SCALE, 1,
                                                          146 / 680 * SplashScreen.PANDA3D_LOGO_SCALE),
                                                   parent=self.main.aspect2d))
        self.panda3d_logo.setTransparency(panda3d.core.TransparencyAttrib.MAlpha)

        self.disclaimer_text = (
            direct.gui.OnscreenText.OnscreenText(text="ALL TRADEMARKS, LOGOS AND BRAND NAMES ARE THE PROPERTY "
                                                      "OF THEIR RESPECTIVE OWNERS.",
                                                 fg=UI.WHITE,
                                                 font=self.main.font,
                                                 pos=(0, -0.95),
                                                 scale=0.025))

        self.version_text = (
            direct.gui.OnscreenText.OnscreenText(text="v" + ".".join([str(i) for i in self.main.VERSION]),
                                                 fg=UI.GREY,
                                                 font=self.main.font,
                                                 pos=(1.7, -0.95),
                                                 scale=0.025))

        self.frame = direct.gui.DirectGui.DirectFrame(frameColor=UI.BLACK,
                                                      frameSize=(0, self.main.window_resolution[0], 0,
                                                                 -self.main.window_resolution[1]),
                                                      parent=self.main.pixel2d)

        self.main.taskMgr.add(self.task_splashscreen, self.main.TASK_SPLASH_SCREEN)

    def task_splashscreen(self, task) -> None:

        if SplashScreen.T1 < task.time < SplashScreen.T2:

            fadein_time = task.time - SplashScreen.T1
            self.frame["frameColor"] = (
                tuple([1 - (fadein_time / SplashScreen.FADE_IN_DURATION) if i == 3 else x
                       for i, x in enumerate(self.frame["frameColor"])]))

        elif SplashScreen.T3 < task.time < SplashScreen.T4:

            fadeout_time = task.time - SplashScreen.T3
            self.frame["frameColor"] = (
                tuple([fadeout_time / SplashScreen.FADE_OUT_DURATION if i == 3 else x
                       for i, x in enumerate(self.frame["frameColor"])]))

        elif SplashScreen.T4 < task.time < SplashScreen.T5:

            self.remove_elements()
            self.main.ui.main_menu.burger_menu.set_visible()

            waitout_time = task.time - SplashScreen.T4
            self.frame["frameColor"] = (
                tuple([1 - (waitout_time / SplashScreen.WAIT_OUT_DURATION) if i == 3 else x
                       for i, x in enumerate(self.frame["frameColor"])]))

        if task.time > SplashScreen.T5:

            self.remove_frame()
            MainMenu.inhibited = False
            return direct.task.Task.done

        else:

            return direct.task.Task.cont

    def remove_elements(self) -> None:

        self.background.destroy()
        self.projectnaer_text.destroy()
        self.projectnaer_logo.destroy()
        self.panda3d_text.destroy()
        self.panda3d_logo.destroy()
        self.disclaimer_text.destroy()
        self.version_text.destroy()

    def remove_frame(self) -> None:

        self.frame.destroy()


class UI:

    MARGIN = 16
    FONT_SIZE = 20
    FONT_TITLE_SIZE = 24
    BUTTON_Y_SIZE = 32
    BUTTON_BORDER_SIZE = 3
    BUTTON_TEXT_Y_OFFSET = 1
    BUTTON_MEDIUM_X_SIZE = 100

    BLACK = (0, 0, 0, 1)
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
