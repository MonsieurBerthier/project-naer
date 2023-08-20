import direct.gui.DirectGui


class Menu:

    def __init__(self, main, ground, car) -> None:

        self._main = main
        self._ground = ground
        self._car = car
        self.font_menu = self._main.loader.loadFont(self._main.PATH_FONT_MENU)

        self.button_zenki = direct.gui.DirectGui.DirectButton(text="Zenki",
                                                              text_font=self.font_menu,
                                                              pos=(-0.2, 0, -0.9),
                                                              scale=.05,
                                                              text_fg=(1, 1, 1, 1),
                                                              text_bg=(1, 0, 0, 1),
                                                              relief=None,
                                                              borderWidth=(0.2, 0.2),
                                                              command=self._car.load_part,
                                                              extraArgs=["frontbumper_oemzenki"])
        self.button_zenki = direct.gui.DirectGui.DirectButton(text="Chuki",
                                                              text_font=self.font_menu,
                                                              pos=(0, 0, -0.9),
                                                              scale=.05,
                                                              text_fg=(1, 1, 1, 1),
                                                              text_bg=(1, 0, 0, 1),
                                                              relief=None,
                                                              command=self._car.load_part,
                                                              extraArgs=["frontbumper_oemchuki"])
        self.button_zenki = direct.gui.DirectGui.DirectButton(text="Kouki",
                                                              text_font=self.font_menu,
                                                              pos=(0.2, 0, -0.9),
                                                              scale=.05,
                                                              text_fg=(1, 1, 1, 1),
                                                              text_bg=(1, 0, 0, 1),
                                                              relief=None,
                                                              command=self._car.load_part,
                                                              extraArgs=["frontbumper_oemkouki"])
