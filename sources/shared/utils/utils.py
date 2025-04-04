#Projet : EduBang
#Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

from json import load as loadJson
from os import listdir, path
from types import MethodType
from typing import Generator
from random import randint
from math import pi, sqrt, atan2, sin, cos, log10, floor
from copy import deepcopy
from datetime import datetime

import pygame as pg

from main import Game, getFont, l, p
from proto import proto
from eventListen import Events
from shared.components.Vectors import Vectors
from shared.components.Physics import Physics, G
from shared.components.Corps import Corps

# La constante d'EduBang
# valeur de calibrage, origine à déterminer
C_EDUBANG: int = 10750

squareAlpha = pg.image.load(p("data/images/assets/squareAlpha.png"))
colorPalette = pg.image.load(p("data/images/assets/colorPalette.png"))

exponentFont = getFont("Medium", 12)
titleFont = getFont("Regular", 20)
descriptionFont = getFont("Regular", 14)
descriptionFontInventory = getFont("Regular", 12)
footerFont = getFont("Regular", 10)
cardFont = getFont("Regular", 12)
languageFont = getFont("Regular", 20)
inter = getFont("SemiBold", 16, header="Inter")
keybindFont = getFont("SemiBold", 16)

FOCUS_COLOR: tuple[int, int, int] = (128, 24, 99)

UNICODES: dict[int, str] = {
    0x9: "tab",
    0x20: "espace",
    0x7F: "del",
    0x4000003A: "F1",
    0x4000003B: "F2",
    0x4000003C: "F3",
    0x4000003D: "F4",
    0x4000003E: "F5",
    0x4000003F: "F6",
    0x40000040: "F7",
    0x40000041: "F8",
    0x40000042: "F9",
    0x40000043: "F10",
    0x40000044: "F11",
    0x40000045: "F12",
    0x400000E2: "alt",
    0x400000E0: "ctrl",
    0x40000052: "↑",
    0x40000050: "←",
    0x40000051: "↓",
    0x4000004F: "→"
}

UNICODES_DARWIN: dict[int, str] = {
    0x30: "tab",
    0x31: "espace",
    0x400000E2: "alt",
    0x400000E3: "cmd",
    0x40000052: "↑",
    0x40000050: "←",
    0x40000051: "↓",
    0x4000004F: "→"
}

Game.ctrl = pg.KMOD_LCTRL if Game.os == "Windows" else pg.KMOD_META
C_UNICODES = UNICODES if Game.os == "Windows" else UNICODES_DARWIN
fnKeys: tuple = (0x400000E2, 0x400000E0 if Game.os == "Windows" else 0x400000E3)

SCROLL_SPEED: int = 20

RAD: float = 2 * pi / 3

# region Prototypes

with proto("Enums", {
    "Violet": (128, 24, 99),
    "DarkViolet": (97, 22, 76),
    "Background": (10, 9, 9)
}) as Enums:
    pass

def onHover() -> None:
    """
    Fonction qui change le curseur en main
    
    Arguments:
        None
        
    Retourne:
        None
    """
    pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
    return

with proto("Button") as Button:
    def drawButton(self) -> None:
        """
        Fonction de base qui dessine un bouton
        
        Arguments:
            None
            
        Retourne:
            None
        """
        if not self.active: return 
        offset: int = 0
        pg.draw.rect(Game.screen, self.color, pg.Rect(self.position, self.size), 0, 8)
        if self.icon:
            Game.screen.blit(self.icon, (
                self.position[0] + 10,
                self.position[1] + 5
            ))
            offset = self.icon.get_size()[0]
        surface = self.font.render(self.text, False, self.textColor)
        width, height = self.font.size(self.text)
        x = self.position[0] + (self.size[0] - width) / 2
        y = self.position[1] + (self.size[1] - height) / 2
        Game.screen.blit(surface, (x + offset / 2, y))
        return
    
    def hideHUDBTN(self, hide: bool) -> None:
        """
        Fonction qui gère l'événement "hideHUD" pour le bouton
        
        Arguments:
            hide (bool): Masquer ou afficher le bouton
            
        Retourne:
            None
        """
        self.visible = not hide
        return

    def mousemotionBTN(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour le bouton
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
            
        Retourne:
            None
        """
        if not self.visible: return
        if not self.active: return
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownBTN(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttondown" pour le bouton
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
            
        Retourne:
            None
        """ 
        if not self.visible: return
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onPressed()
        return
    
    def mousebuttonupBTN(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour le bouton
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.visible: return
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onReleased()
            pg.mixer.music.load(p("data/sound/click.wav"))
            pg.mixer.music.set_volume(1)
            pg.mixer.music.play()
            pg.mixer.music.set_volume(Game.settings["volume"] / 100)
        return

    def mousewheelBTN(self, event) -> None:
        """
        Fonction qui gère l'événement "mousewheel" pour le bouton
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.visible: return
        if not self.active: return
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowBTN(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour le bouton
        
        Arguments:
            w (str): Le nom de la page
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return

    @Button
    def new(self, position: tuple[int, int], size: tuple[int, int], *, color: tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        L'initateur du bouton
        
        Arguments:
            position (tuple[int, int]): Position du bouton
            size (tuple[int, int]): Dimensions du bouton
            color: (tuple[int, int, int]): Couleur du bouton
            
        Retourne:
            None
        """
        self.text = "Button"
        self.position = list(position)
        self.size = size
        self.color = color
        self.font = Game.font
        self.textColor = (0, 0, 0)
        self.icon = None
        self.draw = MethodType(drawButton, self)
        self.onPressed = lambda: None
        self.onReleased = lambda: None
        self.onHover = onHover
        self.scrollable = False
        self.offsetY = 0
        self.active = True
        self.visible = True
        Events.group(self, {
            "hideHUD": MethodType(hideHUDBTN, self),
            "mousemotion": MethodType(mousemotionBTN, self),
            "mousebuttondown": MethodType(mousebuttondownBTN, self),
            "mousebuttonup": MethodType(mousebuttonupBTN, self),
            "mousewheel": MethodType(mousewheelBTN, self),
            "window": MethodType(windowBTN, self)
        })
        return

with proto("CheckBox") as CheckBox:
    def drawCheckBox(self) -> None:
        """
        Fonction de base qui dessine une case à cocher
        """
        if not self.active: return
        color = FOCUS_COLOR if self.checked else (255, 255, 255)
        pg.draw.rect(Game.screen, color, pg.Rect(self.position, self.size), 0, 4)
        if color == FOCUS_COLOR:
            pos1 = (self.position[0] + 5.25, self.position[1] + 15)
            pos2 = (self.position[0] + 12.75, self.position[1] + 22.5)
            pos3 = (self.position[0] + 24, self.position[1] + 7.5)
            pg.draw.line(Game.screen, (255, 255, 255), pos1, pos2, 4)
            pg.draw.line(Game.screen, (255, 255, 255), pos2, pos3, 4)
        return
    
    def hideHUDCB(self, hide: bool) -> None:
        """
        Fonction qui gère l'événement "hideHUD" pour la case à cocher

        Arguments:
            hide (bool): Masquer ou afficher la case à cocher

        Retourne:
            None
        """
        self.active = not hide
        return
    
    def mousemotionCB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour la case à cocher
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownCB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttondown" pour la case à cocher
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.checked = not self.checked
        return
    
    def mousebuttonupCB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour la case à cocher
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onReleased()
        return
    
    def mousewheelCB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousewheel" pour la case à cocher
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowCB(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour la case à cocher
        
        Arguments:
            w (str): Le nom de la page
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return
    
    @CheckBox
    def new(self, position: tuple[int, int], checked: bool = False) -> None:
        """
        L'initateur de la case à cocher
        
        Arguments:
            position (tuple[int, int]): Position de la case à cocher
            checked (bool): Défini son état
            
        Retourne:
            None
        """
        self.checked = checked
        self.position = list(position)
        self.size  = [30, 30]
        self.draw = MethodType(drawCheckBox, self)
        self.onReleased = lambda: None
        self.onHover = onHover
        self.scrollable = False
        self.offsetY = 0
        self.active = True
        Events.group(self, {
            "hideHUD": MethodType(hideHUDCB, self),
            "mousemotion": MethodType(mousemotionCB, self),
            "mousebuttondown": MethodType(mousebuttondownCB, self),
            "mousebuttonup": MethodType(mousebuttonupCB, self),
            "mousewheel": MethodType(mousewheelCB, self),
            "window": MethodType(windowCB, self)
        })
        return

with proto("MessageBox") as MessageBox:
    @MessageBox
    def draw(self) -> None:
        """
        Fonction de base qui dessine la boite de message
        
        Arguments:
            None
            
        Retourne:
            None
        """
        if not self.active: return
        widthScreen, heightScreen = Game.screenSize
        surface = Game.font.render(self.text, False, (0, 0, 0))
        width, height = Game.font.size(self.text)
        x = widthScreen // 2
        y = heightScreen // 2
        xRect = x - (width + 20) // 2
        yRect = y - (height + 20) // 2
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect((xRect , yRect), (width + 20, height + 20)))
        Game.screen.blit(surface, (xRect + 10, yRect + height // 2))
        return
    
    @MessageBox
    def new(self, message: str) -> None:
        """
        L'initateur de la boite de message
        
        Arguments:
            message (str): Le message à transmettre
            
        Retourne:
            None
        """
        self.text = message
        self.active = False
        return

with proto("KeyBind") as KeyBind:
    def drawKeyBind(self):
        """
        Fonction de base qui dessine le keybind
        
        Arguments:
            None
            
        Retourne:
            None
        """
        font = keybindFont
        if any([i in "↑←↓→" for i in self.keyname]):
            font = inter
        color: tuple[int, int, int] = FOCUS_COLOR if self.focus else (255, 255, 255)
        pg.draw.rect(Game.screen, color, pg.Rect(self.position, self.size), 0, 4)
        surface = font.render(" + ".join(self.keyname), False, (0, 0, 0))
        Game.screen.blit(surface, (self.position[0] + 10, self.position[1] + 10))
        return
    
    def mousemotionKB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour le keybind
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownKB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttondown" pour le keybind
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onPressed()
        else:
            self.focus = False
        return
    
    def mousebuttonupKB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour le keybind
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onReleased()
        else:
            self.focus = False
        return
    
    def mousewheelKB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousewheel" pour le keybind
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowKB(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour le keybind
        
        Arguments:
            w (str): Le nom de la page
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return

    def keydownKB(self, event) -> None:
        """
        Fonction qui gère l'événement "keydown" pour le keybind
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if self.focus:
            self.keys = []
            self.keyname = []
            mods = pg.key.get_mods()
            if mods & Game.ctrl:
                self.keyname.append("ctrl" if Game.os == "Windows" else "cmd")
                self.keys.append(fnKeys[1])
            if mods & pg.KMOD_LALT:
                self.keyname.append("alt")
                self.keys.append(fnKeys[0])
            if event.key not in fnKeys:
                self.keyname.append(C_UNICODES[event.key] if event.key in C_UNICODES else event.unicode if event.key > 0x110000 else chr(event.key))
                self.keys.append(event.key)
                self.focus = False
        return

    @KeyBind
    def onPressed(self) -> None:
        """
        Fonction de base qui gère l'événement "onPressed" pour le keybind
        
        Arguments:
            None
        
        Retourne:
            None
        """
        self.focus = not self.focus
        return

    @KeyBind
    def new(self, keys: list[int], keyname: str, position: tuple[int, int]) -> None:
        """
        L'initateur du keybind
        
        Arguments:
            keys (list[int]): Les codes des touches
            keyname (str): Le nom de la liaison de touches
            position (tuple[int, int]): La position du keybind
        
        Retourne:
            None
        """
        self.focus = False
        self.keys = keys
        self.keyname = keyname
        self.position = list(position)
        self.size  = [120, 40]
        self.draw = MethodType(drawKeyBind, self)
        self.onReleased = lambda: None
        self.onHover = onHover
        self.scrollable = False
        self.offsetY = 0
        Events.group(self, {
            "mousemotion": MethodType(mousemotionKB, self),
            "mousebuttondown": MethodType(mousebuttondownKB, self),
            "mousebuttonup": MethodType(mousebuttonupKB, self),
            "mousewheel": MethodType(mousewheelKB, self),
            "window": MethodType(windowKB, self),
            "keydown": MethodType(keydownKB, self)
        })
        return

with proto("Text") as Text:
    @Text
    def draw(self) -> None:
        """
        Fonction de base qui affiche le texte sur l'écran
        
        Arguments:
            None
            
        Retourne:
            None
        """
        surface = self.font.render(self.text, self.antialiasing, self.color)
        Game.screen.blit(surface, self.position)
        return

    def mousewheelT(self, event) -> None:
        """
        Fonction qui gère l'événement "mousewheel" pour le Texte
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    @Text
    def new(self, text: str, position: tuple[int, int], antialiasing: bool = False, color: tuple[int, int, int] = (0, 0, 0), font=Game.font) -> None:
        """
        L'initateur du Texte
        
        Arguments:
            text (str): Le texte à afficher
            position (tuple[int, int]): La position du Texte
            antialiasing (bool): Activer l'anticrénelage
            color (tuple[int, int, int]): La couleur du Texte
            font (pg.Font): La police de texte
        
        Retourne:
            None
        """
        self.text = text
        self.position = list(position)
        self.antialiasing = antialiasing
        self.color = color
        self.font = font
        self.size = Game.font.size(self.text)
        self.scrollable = False
        self.offsetY = 0
        Events.group(self, {"mousewheel": MethodType(mousewheelT, self)})
        return

with proto("Input") as Input:
    def drawInput(self) -> None:
        """
        Fonction de base qui dessine l'entrée de texte
        
        Arguments:
            None
        
        Retourne:
            None
        """
        if not self.visible: return
        if not self.active: return
        color: tuple[int, int, int] = FOCUS_COLOR if self.focus and self.active else (255, 255, 255)
        fontColor: tuple[int, int, int] = (150, 150, 150) if self.placeholder and not self.text else (0, 0, 0)
        pg.draw.rect(Game.screen, color, pg.Rect(self.position, self.size), 0, 4)
        text: str = self.placeholder if self.placeholder and not self.text else self.text
        surface = self.font.render(text, False, fontColor)
        dim = self.font.size(text)
        x = self.position[0] + 5
        y = self.position[1] + self.size[1] // 2 - dim[1] // 2
        Game.screen.blit(surface, (x, y))
        return
    
    def hideHUDI(self, hide: bool) -> None:
        """
        Fonction qui gère l'événement "hideHUD" pour l'entrée de texte

        Arguments:
            hide (bool): Masquer ou afficher l'entrée de texte

        Retourne:
            None 
        """
        self.active = not hide
        return

    def mousemotionI(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour l'entrée de texte
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownI(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttondown" pour l'entrée de texte
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.focus = not self.focus
            if self.focus:
                self.onPressed()
                if self.resetOnClick: self.text = ""
        else:
            self.focus = False
            self.afterInput(self)
        return
    
    def mousebuttonupI(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour l'entrée de texte
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.focus = not self.focus
            if self.focus: self.onReleased()
        else:
            self.focus = False
            self.afterInput(self)
        return
    
    def mousewheelI(self, event) -> None:
        """
        Fonction qui gère l'événement "mousewheel" pour l'entrée de texte
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowI(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour l'entrée de texte
        
        Arguments:
            w (str): Le nom de la page
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return

    def keydownI(self, event) -> None:
        """
        Fonction qui gère l'événement "keydown" pour l'entrée de texte
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        if self.focus:
            if event.key in [pg.K_RETURN, pg.K_ESCAPE, pg.K_TAB]:
                self.focus = False
                self.afterInput(self)
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if self.numberOnly:
                    if not event.unicode.isdigit():
                        return
                self.text += event.unicode
        return

    @Input
    def new(self, text: str, position: tuple[int, int], size: tuple[int, int]) -> None:
        """
        L'initiateur de l'entrée de texte
        
        Arguments:
            text (str): Le texte déjà présent dans la boite
            position (tuple[int, int]): La position de l'entrée de texte
            size: (tuple[int, int]): La taille de l'entrée de texte
            
        Retourne:
            None
        """
        self.active = True
        self.visible = True
        self.focus = False
        self.text = text
        self.placeholder = None
        self.position = position
        self.size  = size
        self.draw = MethodType(drawInput, self)
        self.onPressed = lambda: None
        self.onReleased = lambda: None
        self.afterInput = lambda x: None
        self.onHover = onHover
        self.font = Game.font
        self.numberOnly = False
        self.scrollable = False
        self.resetOnClick = False
        self.offsetY = 0
        Events.group(self, {
            "hideHUD": MethodType(hideHUDI, self),
            "mousemotion": MethodType(mousemotionI, self),
            "mousebuttondown": MethodType(mousebuttondownI, self),
            "mouseubuttonup": MethodType(mousebuttonupI, self),
            "mousewheel": MethodType(mousewheelI, self),
            "window": MethodType(windowI, self),
            "keydown": MethodType(keydownI, self)
        })
        return

with proto("SlideBar") as SlideBar:
    def drawSlideBar(self) -> None:
        """
        Fonction de base qui dessine une barre coulissante
        
        Arguments:
            None
        
        Retourne:
            None
        """
        if self.active:
            pos = pg.mouse.get_pos()
            value = pos[0] - self.position[0]
            self.value = max(self.values[0], min(self.values[1], value))

        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect(self.position, self.size), 0, 8)
        pg.draw.rect(Game.screen, FOCUS_COLOR, pg.Rect(self.position, (self.value, 5)), 0, 8)
        pg.draw.circle(Game.screen, FOCUS_COLOR, (self.position[0] + self.value, self.position[1] + 2.5), 5)
        return
    
    def mousemotionSB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour la barre coulissante
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownSB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttondown" pour la barre coulissante
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onPressed()
        else:
            self.active = False
        return
    
    def mousebuttonupSB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour la barre coulissante
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onReleased()
        else:
            self.active = False
        return
    
    def mousewheelSB(self, event) -> None:
        """
        Fonction qui gère l'événement "mousewheel" pour la barre coulissante
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        x, y = pg.mouse.get_pos()
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.value += event.y
            self.value = max(0, min(100, self.value))
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowSB(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour la barre coulissante
        
        Arguments:
            w (str): Le nom de la page
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return

    @SlideBar
    def onPressed(self) -> None:
        """
        Fonction de base qui gère l'événement "onPressed" pour la barre coulissante
        
        Arguments:
            None
        
        Retourne:
            None
        """
        self.active = True
        return

    @SlideBar
    def onReleased(self) -> None:
        """
        Fonction de base qui gère l'événement "onReleased" pour la barre coulissante
        
        Arguments:
            None
        
        Retourne:
            None
        """
        self.active = False
        return

    @SlideBar
    def new(self, position: tuple[int, int]) -> None:
        """
        L'initiateur de la barre coulissante
        
        Arguments:
            position (tuple[int, int]): La position de la barre coulissante
            
        Retourne:
            None
        """
        self.active = False
        self.values = [0, 100]
        self.value = self.values[0]
        self.position = list(position)
        self.size = (100, 5)
        self.draw = MethodType(drawSlideBar, self)
        self.onHover = onHover
        self.scrollable = False
        self.offsetY = 0
        Events.group(self, {
            "mousemotion": MethodType(mousemotionSB, self),
            "mousebuttondown": MethodType(mousebuttondownSB, self),
            "mousebuttonup": MethodType(mousebuttonupSB, self),
            "mousewheel": MethodType(mousewheelSB, self),
            "window": MethodType(windowSB, self)
        })
        return

with proto("System") as System:
    def drawSystem(self) -> None:
        """
        Fonction de base qui dessine la boite d'un système
        
        Arguments:
            None
            
        Retourne:
            None
        """
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect(self.position, self.size), 1, 8)
        surface = titleFont.render(self.system["title"], False, (255, 255, 255))
        Game.screen.blit(surface, (self.position[0] + 10, self.position[1] + 10))
        surface = descriptionFont.render(self.system["description"], False, (255, 255, 255))
        Game.screen.blit(surface, (self.position[0] + 10, self.position[1] + 40))
        dateSplit: list[str, str] = str(datetime.fromtimestamp(self.system["meta"]["lastModified"])).split(" ")
        dateRSplit: list[str, str, str] = dateSplit[0].split("-")
        dateRSplit.reverse()
        date: str = "%s @ %s" % ("/".join(dateRSplit), dateSplit[1])
        surface = footerFont.render("%s, %s" % (date, self.system["meta"]["user"]), False, (255, 255, 255))
        Game.screen.blit(surface, (self.position[0] + 10, self.position[1] + self.size[1] - 20))
        return
    
    def mousemotionS(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour la boite d'un système
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return
    
    def mousebuttonupS(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour la boite d'un système
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            for corps in self.system["space"]:
                c = Corps(corps["mass"], corps["radius"], corps["position"], corps["color"], corps["velocity"])
                for meta in corps["meta"]:
                    setattr(c, meta, corps["meta"][meta])
                Game.space.append(c)
            Game.originSpace = deepcopy(Game.space)
            Game.select("sandbox")
        return

    def mousewheelS(self, event) -> None:
        """
        Fonction qui gère l'événement "mousewheel" pour la boite d'un système
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowS(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour la boite d'un système
        
        Arguments:
            None
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return

    @System
    def destroy(self) -> None:
        """
        Fonction qui détruit le système

        Arguments:
            None

        Retourne:
            None
        """
        self.system = None
        self.position = [0, 0]
        self.size = [0, 0]
        self.draw = lambda: None
        self.onHover = lambda: None
        self.scrollable = False
        self.offsetY = None
        Events.stopObserving(self)
        return

    @System
    def new(self, system: dict, index: int) -> None:
        """
        L'initiateur de la boite d'un système
        
        Arguments:
            system (dict): Les données d'un système
            index (int): L'ordre du système sur l'écran
        
        Retourne:
            None
        """
        self.system = system
        self.position = [400, 100 + 120 * index]
        self.size = (500, 100)
        self.draw = MethodType(drawSystem, self)
        self.onHover = onHover
        self.scrollable = False
        self.offsetY = 0
        Events.group(self, {
            "mousemotion": MethodType(mousemotionS, self),
            "mousebuttonup": MethodType(mousebuttonupS, self),
            "mousewheel": MethodType(mousewheelS, self),
            "window": MethodType(windowS, self)
        })

with proto("Inventory") as Inventory:
    def drawInventory(self):
        """
        Fonction de base qui dessine l'inventaire
        
        Arguments:
            None
            
        Retourne:
            None
        """
        if not self.active: return
        bodies = self.bodies.copy()
        width, height = Game.screenSize
        x = width / 100
        y = height / 100
        pg.draw.rect(Game.screen, (10, 9, 9), pg.Rect((10 * x, 10 * y), (80 * x, 80 * y)), 0, 8)
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect((10 * x, 10 * y), (80 * x, 80 * y)), 1, 8)
        w, h = 180, 100
        r: bool = True
        k: int = floor((80 * x) / (w + 12))
        i: int = 0
        dy = (10 * y + 10)
        while r and k > 0:
            dx = (10 * x + 10)
            for j in range(k):
                body = bodies[i]
                pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect((dx, dy), (w, h)), 1, 8)
                surface = Game.font.render(body["meta"]["name"], False, (255, 255, 255))
                Game.screen.blit(surface, (dx + 10, dy + 10))
                displayMultilineText(body["meta"]["description"], descriptionFontInventory, (dx + 10, dy + 35), 100, stop=3)
                pg.draw.circle(Game.screen, body["color"], (dx + 130, dy + 50), 10)
                self.clickableZones[body["file"]] = ((dx, dy), (dx + 180, dy + 100))
                dx += 190
                i += 1
                if len(bodies) <= i:
                    r = False
                    break
            dy += 110
        return
    
    def mousemotionIn(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour l'inventaire
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        x, y = event.pos
        for cz in self.clickableZones.values():
            if x > cz[0][0] and x < cz[1][0] and y > cz[0][1] and y < cz[1][1]:
                self.onHover()
                Events.trigger("hovering", self)
                break
        else:
            Events.trigger("unhovering", self)
        return
    
    def mousebuttonupIn(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour l'inventaire
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        for file, cz in self.clickableZones.items():
            if x > cz[0][0] and x < cz[1][0] and y > cz[0][1] and y < cz[1][1]:
                for body in self.bodies:
                    if body["file"] != file:
                        continue
                    Events.trigger("inventory", body)
                    Events.trigger("unhovering", self)
                    self.active = False
                    return

    def windowIn(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour l'inventaire
        
        Arguments:
            w (str): Le nom de la page
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return
    
    @Inventory
    def update(self) -> None:
        """
        Fonction qui met à jour l'inventaire
        
        Arguments:
            None
        
        Retourne:
            None
        """
        self.bodies = []
        bodyFiles = [path.join(p("data/bodies"), f) for f in listdir(p("data/bodies")) if path.isfile(path.join(p("data/bodies"), f))]
        for i, bodyFile in enumerate(bodyFiles):
            body = {}
            with open(bodyFile, "r", encoding="utf-8") as f:
                body = loadJson(f)
                body["file"] = bodyFile
                f.close()
            self.bodies.append(body)

    @Inventory
    def new(self):
        """
        L'initiateur de l'inventaire
        
        Arguments:
            None
            
        Retourne:
            None
        """
        self.active = False
        self.clickableZones = {}
        self.update()
        self.draw = MethodType(drawInventory, self)
        self.onHover = onHover
        Events.group(self, {
            "mousemotion": MethodType(mousemotionIn, self),
            "mousebuttonup": MethodType(mousebuttonupIn, self),
            "window": MethodType(windowIn, self)
        })
        return

with proto("DataKeeper") as DataKeeper:
    @DataKeeper
    def new(self):
        """
        L'initiateur du DataKeeper, de la sauvegarde des variables
        
        Arguments:
            None
            
        Retourne:
            None
        """
        return

with proto("Path") as Path:
    # dessiner trajectoire terre
    @Path
    def draw_corps_path(self, screen, path, color):
        """
        Dessine une trajectoire
        
        Arguments:
            None
        
        Retourne:
            None
        """
        for pos in path:
            pg.draw.circle(screen, color, spacePosToScreenPos(pos), 1)
        return

with proto("SizeViewer") as SizeViewer:
    def drawSizeViewer(self):
        """
        Fonction de base pour dessiner une règle de mesure
        
        Arguments:
            None
            
        Retourne:
            None
        """
        if not self.active: return
        width, distance, unit = getSize()
        text: str = "%s %s" % (distance, unit)
        x, y = self.position
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect((x, y), (width, 2)))
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect((x, y - 8), (2, 10)))
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect((x + width, y - 8), (2, 10)))
        surface = Game.font.render(text, False, (255, 255, 255))
        Game.screen.blit(surface, (x, y + 10))
        w, h = Game.font.size(text)
        self.size = (w if w > 100 else 100, h + 60)
        return

    def hideHUDSV(self, hide: bool) -> None:
        """
        Fonction qui gère l'événement "hideHUD" pour la règle de mesure

        Arguments:
            hide (bool): Masquer ou afficher la règle de mesure

        Retourne:
            None
        """
        self.active = not hide

    def mousemotionSV(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour la règle de mesure
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        x, y = event.pos
        if self.focus:
            self.position = [x - self.size[0] // 2, y]
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownSV(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttondown" pour la règle de mesure
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.focus = True
            self.position = [x - self.size[0] // 2, y]
        return
    
    def mousebuttonupSV(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour la règle de mesure
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        button = event.button
        if button != 1: return
        self.focus = False
        return

    def windowSV(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour la règle de mesure
        
        Arguments:
            w (str): Le nom de la page
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return

    @SizeViewer
    def new(self, position: tuple[int, int]) -> None:
        """
        L'initiateur de la règle de mesure
        
        Arguments:
            position (tuple[int, int]): La position de la règle sur l'écran
            
        Retourne:
            None
        """
        self.position = list(position)
        self.draw = MethodType(drawSizeViewer, self)
        self.size = (0, 0)
        self.onHover = onHover
        self.focus = False
        self.active = True
        Events.group(self, {
            "hideHUD": MethodType(hideHUDSV, self),
            "mousemotion": MethodType(mousemotionSV, self),
            "mousebuttondown": MethodType(mousebuttondownSV, self),
            "mousebuttonup": MethodType(mousebuttonupSV, self),
            "window": MethodType(windowSV, self)
        })
        return

with proto("ColorPicker") as ColorPicker:
    def drawColorPickerSquare(self) -> None:
        """
        Fonction de base qui dessine le carré de sélection de la couleur
        
        Arguments:
            None
            
        Retourne:
            None
        """
        if not self.visible: return
        if not self.active: return
        pos = (self.position[0] - 285, self.position[1] + 20)
        pg.draw.rect(Game.screen, self.color, (pos, (255, 255)))
        Game.screen.blit(squareAlpha, pos)
        pos = (-self.aim[0] + self.position[0] + 19, self.aim[1] + self.position[1] + 20)
        pg.draw.circle(Game.screen, Game.screen.get_at(pos), pos, 15)
        pg.draw.circle(Game.screen, (255, 255, 255), pos, 15, 1)
    
    def drawColorPickerBar(self) -> None:
        """
        Fonction de base qui dessine la barre de sélection de la couleur
        
        Arguments:
            None
            
        Retourne:
            None
        """
        if not self.visible: return
        if not self.active: return
        Game.screen.blit(colorPalette, (0, self.position[1] + 310))
        color = pg.Color(0)
        color.hsla = (3.6 * self.value, 100, 50, 100)
        pg.draw.rect(Game.screen, color, (self.position[0] + self.value * 5 + 20, self.position[1] + 305, 10, 20))
        pg.draw.rect(Game.screen, (255, 255, 255), (self.position[0] + self.value * 5 + 20, self.position[1] + 305, 10, 20), 1)
        return
    
    def drawColorPicker(self) -> None:
        """
        Fonction de base qui dessine le sélecteur de couleur
        
        Arguments:
            None
        
        Retourne:
            None
        """
        if not self.visible: return
        if not self.active: return
        if not self.focus:
            pg.draw.rect(Game.screen, self.target, (self.position, (60, 60)), 0, 8)
        else:
            pg.draw.rect(Game.screen, (1, 0, 0), (self.position, (-560, 340)), 0, 8)
            pg.draw.rect(Game.screen, self.target, ((self.position[0] - 200, self.position[1] + 20), (255, 255)))
            drawColorPickerBar(self)
            drawColorPickerSquare(self)
        return

    def mousemotionCP(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour le sélecteur de couleur
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        x, y = event.pos
        if not self.focus:
            if x > self.position[0] and x < self.position[0] + 60 and y > self.position[1] and y < self.position[1] + 60:
                self.onHover()
                Events.trigger("hovering", self)
            else:
                Events.trigger("unhovering", self)
        else:
            square = x > self.position[0] + 285 and x < self.position[0] + 540 and y > self.position[1] + 20 and y < self.position[1] + 275
            bar = x > self.position[0] + 20 and x < self.position[0] + 520 and y > self.position[1] + 305 and y < self.position[1] + 325
            if square or bar:
                self.onHover()
                Events.trigger("hovering", self)
            else:
                Events.trigger("unhovering", self)
            if self.mouse:
                if square:
                    self.target = Game.screen.get_at((x, y))
                    self.aim = (
                        x - (self.position[0] + 20),
                        y - (self.position[1] + 20)
                    )
                if bar:
                    self.value = (x - (self.position[0] + 20)) / 5
                    color = pg.Color(0)
                    color.hsla = (3.6 * self.value, 100, 50, 100)
                    self.color = (color.r, color.g, color.b)
                    pos = (
                        -self.aim[0] + self.position[0] + 20,
                        self.aim[1] + self.position[1] + 20
                    )
                    self.target = Game.screen.get_at(pos)[:-1]
        return

    def mousebuttondownCP(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttondown" pour le sélecteur de couleur
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        button = event.button
        if button != 1: return
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + 60 and y > self.position[1] and y < self.position[1] + 60:
            self.focus = True
        if self.focus:
            square = x > self.position[0] + 285 and x < self.position[0] + 540 and y > self.position[1] + 20 and y < self.position[1] + 275
            bar = x > self.position[0] + 20 and x < self.position[0] + 520 and y > self.position[1] + 305 and y < self.position[1] + 325
            self.mouse = square or bar
            if square:
                self.target = Game.screen.get_at((x, y))
                self.aim = (
                    x - (self.position[0] + 20),
                    y - (self.position[1] + 20)
                )
            if bar:
                self.value = (x - (self.position[0] + 20)) / 5
                color = pg.Color(0)
                color.hsla = (3.6 * self.value, 100, 50, 100)
                self.color = (color.r, color.g, color.b)
                pos = (
                    -self.aim[0] + self.position[0] + 20,
                    self.aim[1] + self.position[1] + 20
                )
                self.target = Game.screen.get_at(pos)[:-1]
        return
    
    def mousebuttonupCP(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour le sélecteur de couleur
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        button = event.button
        if button != 1: return
        x, y = event.pos
        if not (x > self.position[0] and x < self.position[0] + 560 and y > self.position[1] and y < self.position[1] + 340):
            self.focus = False
        if self.focus:
            self.mouse = False
        return
    
    def mousewheelCP(self, event) -> None:
        """
        Fonction qui gère l'événement "mousewheel" pour le sélecteur de couleur
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        x, y = pg.mouse.get_pos()
        if x > self.position[0] + 20 and x < self.position[0] + 520 and y > self.position[1] + 305 and y < self.position[1] + 325:
            self.value += event.y
            if self.value <= 1 or self.value >= 99:
                self.value = 0 if self.value >= 99 else 100
            color = pg.Color(0)
            color.hsla = (3.6 * self.value, 100, 50, 100)
            self.color = (color.r, color.g, color.b)
            pos = (
                self.aim[0] + self.position[0] + 20,
                self.aim[1] + self.position[1] + 20
            )
            self.target = Game.screen.get_at(pos)[:-1]
        return

    def windowCP(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour le sélecteur de couleur
        
        Arguments:
            w (str): Le nom de la page
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return

    @ColorPicker
    def new(self, position: tuple[int, int]) -> None:
        """
        L'initiateur du sélecteur de couleur
        
        Arguments:
            position (tuple[int, int]): La position du sélecteur de couleur
            
        Retourne:
            None
        """
        self.active = True
        self.visible = True
        self.position = position
        self.color = (255, 0, 0)
        self.target = (255, 0, 0)
        self.aim = (520, 0)
        self.values = (0, 100)
        self.value = 0
        self.focus = False
        self.mouse = False
        self.draw = MethodType(drawColorPicker, self)
        self.onHover = onHover
        Events.group(self, {
            "mousemotion": MethodType(mousemotionCP, self),
            "mousebuttonup": MethodType(mousebuttonupCP, self),
            "mousebuttondown": MethodType(mousebuttondownCP, self),
            "mousewheel": MethodType(mousewheelCP, self),
            "window": MethodType(windowCP, self)
        })
        return

with proto("Card") as Card:
    def drawCard(self) -> None:
        """
        Fonction de base qui dessine une carte
        
        Arguments:
            None
            
        Retourne:
            None
        """
        if not self.active: return 
        pg.draw.rect(Game.screen, (33, 33, 33), pg.Rect(self.position, self.size), 0, 8)
        pg.draw.circle(Game.screen, self.body["color"], (self.position[0] + 40, self.position[1] + 40), 30)
        surface = self.font.render(self.body["meta"]["name"], False, (255, 255, 255))
        w, h = self.font.size(self.body["meta"]["name"])
        x = self.position[0] + 40 - w // 2
        y = self.position[1] + 75
        Game.screen.blit(surface, (x, y))
        return
    
    def hideHUDC(self, hide: bool) -> None:
        self.active = not hide
        return

    def mousemotionC(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour la carte
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
            
        Retourne:
            None
        """
        if not self.active: return
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return
    
    def mousebuttonupC(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour la carte
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            Events.trigger("inventory", self.body)
        return

    def mousewheelC(self, event) -> None:
        """
        Fonction qui gère l'événement "mousewheel" pour la carte
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        if not self.active: return
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowC(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour la carte
        
        Arguments:
            w (str): Le nom de la page
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return

    @Card
    def new(self, body, position: tuple[int, int]) -> None:
        """
        L'initateur de la carte
        
        Arguments:
            icon (pg.Image): L'image de la carte
            text (str): Texte de la carte
            position: (tuple[int, int]): Position de la carte
            
        Retourne:
            None
        """
        self.body = body
        self.text = body["meta"]["name"]
        self.position = list(position)
        self.size = (80, 100)
        self.font = cardFont
        # self.icon = icon
        self.draw = MethodType(drawCard, self)
        self.onHover = onHover
        self.scrollable = False
        self.offsetY = 0
        self.active = True
        Events.group(self, {
            "hideHUD": MethodType(hideHUDC, self),
            "mousemotion": MethodType(mousemotionC, self),
            "mousebuttonup": MethodType(mousebuttonupC, self),
            "mousewheel": MethodType(mousewheelC, self),
            "window": MethodType(windowC, self)
        })
        return

with proto("Language") as Language:
    def drawLanguage(self) -> None:
        pg.draw.rect(Game.screen, (33, 33, 33), pg.Rect(self.position, self.size))
        Game.screen.blit(self.icon, (self.position[0] + 5, self.position[1] + 5))
        surface = languageFont.render(l(self.lang), False, (255, 255, 255))
        x = self.position[0] + 80
        y = self.position[1] + 10
        Game.screen.blit(surface, (x, y))
        if Game.language == self.lang:
            pg.draw.rect(Game.screen, (100, 255, 100), pg.Rect(self.position, self.size), 2)
        return

    def mousemotionL(self, event) -> None:
        """
        Fonction qui gère l'événement "mousemotion" pour le bouton
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
            
        Retourne:
            None
        """
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttonupL(self, event) -> None:
        """
        Fonction qui gère l'événement "mousebuttonup" pour le bouton
        
        Arguments:
            event (pg.event.Event): L'événement PyGame
        
        Retourne:
            None
        """
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            Game.language = self.lang
            Events.trigger("lang", self.lang)
        return

    def windowL(self, w) -> None:
        """
        Fonction qui gère l'événement "window" pour le bouton
        
        Arguments:
            w (str): Le nom de la page
        
        Retourne:
            None
        """
        Events.stopObserving(self)
        return

    @Language
    def new(self, lang: str, position: tuple[int, int]) -> None:
        self.lang = lang[14:-5]
        self.icon = pg.transform.scale(pg.image.load(p("data/images/flags/%s.png" % self.lang)), (60, 40))
        self.position = position
        self.size = (230, 50)
        self.draw = MethodType(drawLanguage, self)
        self.onHover = onHover
        Events.group(self, {
            "mousemotion": MethodType(mousemotionL, self),
            "mousebuttonup": MethodType(mousebuttonupL, self),
            "window": MethodType(windowL, self)
        })
        return

# endregion

# region Fonctions physiques

def updateCorps(a, b) -> float:
    """
    Met à jour la position de 2 corps en fonction de leur masse et de leur distance.

    Arguments : 
        a (Corps): Premier corps
        b (Corps): Deuxième corps
    
    Retourne :
        float : Distance entre les 2 corps
    """
    distance: float = Vectors.get_distance(a.pos, b.pos)
    attraction: float = Physics.get_attraction(a.mass, b.mass, distance, a.velocity, b.velocity)
    unitVector: tuple[float] = Vectors.get_unit_vector(a.pos, b.pos)
    accA: tuple[float, float] = (unitVector[0] * attraction / a.mass, unitVector[1] * attraction / a.mass)
    accB: tuple[float, float] = (-unitVector[0] * attraction / b.mass, -unitVector[1] * attraction / b.mass)

    a.update_position(accA, Game.DT)
    b.update_position(accB, Game.DT)
    return distance

def mergeColor(a, b) -> tuple[int, int, int]:
    """
    Fusionne la couleur de 2 corps en fonction de leur surface.

    Arguments : 
        a (Corps): Premier corps
        b (Corps): Deuxième corps
    
    Retourne :
        tuple[int, int, int] : Couleur résultant de la fusion
    """
    # C'est un calcul de moyenne pondérée
    surfaceA: float = pi * a.radius ** 2
    surfaceB: float = pi * b.radius ** 2
    red: float = (surfaceA * a.color[0] + surfaceB * b.color[0]) / (surfaceA + surfaceB)
    green: float = (surfaceA * a.color[1] + surfaceB * b.color[1]) / (surfaceA + surfaceB)
    blue: float = (surfaceA * a.color[2] + surfaceB * b.color[2]) / (surfaceA + surfaceB)
    return (red, green, blue)

def mergeNames(d1: tuple[int, str], d2: tuple[int, str]) -> str:
    """
    Fusionne le nom de 2 corps en fonction de leur masse.

    Arguments : 
        d1 (tuple[int, str]): Métadonnée du premier corps
        d2 (tuple[int, str]): Métadonnée du deuxième corps
    
    Retourne :
        str : Nom résultant de la fusion
    """
    m1, n1 = d1
    m2, n2 = d2
    mass: int = m1 + m2
    p1: float = round(m1 * 100 / mass, -1)
    p2: float = 100 - p1
    i1: int = int(p1 / 100 * len(n1))
    i2: int = int(p2 / 100 * len(n2))
    if len(n2) > i2 + 1:
        nr2: str = n2[(i2 + 2):] if i2 != 0 else n2[i2 + 1] + n2[(i2 + 2):]
    else:
        nr2: str = n2[i2:]
    result: str = n1[:i1] + nr2
    return result

def processMergingNames(a, b, c) -> None:
    """
    Procède la fusion des noms

    Arguments : 
        a (Corps): Premier corps
        b (Corps): Deuxième corps
        c (Corps): Corps résultant
    
    Retourne :
        None
    """
    aName = getattr(a, "name", None)
    bName = getattr(b, "name", None)
    c.name = aName or bName
    if aName and bName:
        x1 = a if a.mass < b.mass else b
        x2 = b if x1 == a else a
        dominationIndex: float = x2.mass * 100 / x1.mass
        c.name = x2.name if 10 < dominationIndex else mergeNames((x1.mass, x1.name), (x2.mass, x2.name))
    return

def mergeEnergy(d1: tuple[int, tuple[int, int], tuple[int, int]], d2: tuple[int, tuple[int, int], tuple[int, int]]) -> list[float, float]:
    """
    Fusionne les énergies cinétiques de 2 corps.

    Arguments : 
        d1 (EnergyInfos): Informations énergétiques du premier corps
        d2 (EnergyInfos): Informations énergétiques du deuxième corps
    
    Retourne :
        tuple[float, float] : Energie cinétique résultante
    """
    mass: int = d1[0] + d2[0]
    cineticEnergyCorps1: float = Physics.get_cinetic_energy(d1[0], Physics.get_velocity(d1[1], d1[2], Game.DT))
    cineticEnergyCorps2: float = Physics.get_cinetic_energy(d2[0], Physics.get_velocity(d2[1], d2[2], Game.DT))


    unitVectorMouvCorps1: tuple[float, float] = Vectors.get_unit_vector_mouv(d1[1], d1[2])
    unitVectorMouvCorps2: tuple[float, float] = Vectors.get_unit_vector_mouv(d2[1], d2[2])

    cineticEnergyVectorCorps1: tuple[float, float] = (cineticEnergyCorps1 * unitVectorMouvCorps1[0], cineticEnergyCorps1 * unitVectorMouvCorps1[1])
    cineticEnergyVectorCorps2: tuple[float, float] = (cineticEnergyCorps2 * unitVectorMouvCorps2[0], cineticEnergyCorps2 * unitVectorMouvCorps2[1])


    sumVectorCineticEnergyCorps1: tuple[float, float] = (cineticEnergyVectorCorps1[0] / d1[0], cineticEnergyVectorCorps1[1] / d1[0])
    sumVectorCineticEnergyCorps2: tuple[float, float] = (cineticEnergyVectorCorps2[0] / d2[0], cineticEnergyVectorCorps2[1] / d2[0])


    x: float = -(sumVectorCineticEnergyCorps1[0] + sumVectorCineticEnergyCorps2[0]) / C_EDUBANG
    y: float = -(sumVectorCineticEnergyCorps1[1] + sumVectorCineticEnergyCorps2[1]) / C_EDUBANG

    return [x, y]

def process_collide(corps1, corps2):
    """
    Procède la fusion de 2 corps

    Arguments : 
        corps1 (Corps): Premier corps
        corps2 (Corps): Deuxième corps
    
    Retourne :
        Corps : Corps à supprimer de la simulation
    """
    mass: int = corps1.mass + corps2.mass
    radius: float = sqrt(((pi * corps1.radius ** 2) + (pi * corps2.radius ** 2)) / pi)
    color: tuple[float, float, float] = mergeColor(corps1, corps2)

    corps = corps1
    hasChanged: bool = False
    if corps2.mass > corps1.mass:
        corps = corps2
        hasChanged = True
    corps.mass = mass
    corps.radius = radius
    corps.color = color
    try:


        corps.velocity = mergeEnergy((corps1.mass, corps1.pos, corps1.path[-2]), (corps2.mass, corps2.pos, corps2.path[-2]))
    except IndexError:
        print("index_error")
        corps.velocity = [0, 0]

    corps.path = []
    processMergingNames(corps1, corps2, corps)
    if Game.Camera.focus in [corps1, corps2]:
        Game.Camera.focus = corps
    return corps1 if hasChanged else corps2

# endregion

# region Fond espace

def loadSpace(perlin) -> tuple[dict[tuple, tuple], int]:
    """
    Fonction qui charge un espace selon un bruit de Perlin

    Arguments : 
        perlin (Perlin): Bruit de Perlin
    
    Retourne :
        tuple[dict[tuple, tuple], int] : Espace généré
    """
    galaxy = {}

    for x in range(perlin.size):
        for y in range(perlin.size):
            value = perlin.noise(x / 80, y / 80)

            if value > 0.15:
                galaxy[(x, y)] = (int(70 * value), int(20 * value), int(70 * value * 0.8))

    return (galaxy, perlin.size)

def loadSpaceIterated(perlin) -> Generator[int, None, tuple[dict[tuple, tuple], int]]:
    """
    Générateur qui charge un espace selon un bruit de Perlin et qui rend compte de son avancement

    Arguments: 
        perlin (Perlin): Bruit de Perlin

    Retourne:
        tuple[dict[tuple, tuple], int] : Espace généré
    """
    galaxy = {}

    # Code qui génère les amas de galaxies
    for x in range(perlin.size):
        yield x + 1
        for y in range(perlin.size):
            value = perlin.noise(x / 80, y / 80)

            if value > 0.15:
                galaxy[(x, y)] = (int(70 * value), int(20 * value), int(70 * value * 0.8))

    yield (galaxy, perlin.size)

def loadStars(n: int = 100, position: tuple[int, int] = (-1000, 1000)) -> list[tuple[int, int]]:
    """
    Charge les étoiles de l'espace.

    Arguments: 
        n (int): Nombre d'étoiles
        position (tuple[int, int]): Plage de position possible de génération
    
    Retourne:
        list[tuple[int, int]] : Etoiles générées
    """
    stars = []
    for i in range(n):
        stars.append((randint(position[0], position[1]), randint(position[0], position[1])))
    return stars

# endregion

# region Vecteur
def draw_velocity_vector(screen, corps) -> None:
    """
    Dessine une ligne représentant le vecteur de la vélocité d'un astre
    
    Arguments:
        screen (pg.Surface): L'écran PyGame
        corps (Corps): Astre étudié
        
    Retourne:
        None
    """
    if len(corps.path) > 1:
        corps_velocity = Physics.get_velocity(corps.path[-2], corps.path[-1], Game.dt)
        unit_vector_mouv = Vectors.get_unit_vector_mouv(corps.path[-2], corps.path[-1])
        velocity_vector = unit_vector_mouv[0] * corps_velocity, unit_vector_mouv[1] * corps_velocity

        k = 50

        startX = corps.pos[0] * Game.Camera.zoom + Game.Camera.x
        startY = corps.pos[1] * Game.Camera.zoom + Game.Camera.y

        endX = startX + velocity_vector[0] * k
        endY = startY + velocity_vector[1] * k

        pg.draw.line(screen, (0, 255, 0), (startX, startY), (endX, endY), 5)
    return
    
def draw_cinetic_energy_vector(screen, corps) -> None:
    """
    Dessine une ligne représentant le vecteur de l'énergie cinétique
    
    Arguments:
        screen (pg.Surface): L'écran PyGame
        corps: (Corps): Astre étudié
        
    Retourne:
        None
    """
    if len(corps.path) > 1:
        unit_vector_mouv = Vectors.get_unit_vector_mouv(corps.path[-2], corps.path[-1])
        cinetic_energy = Game.normalizeCinetic(corps)
        cinetic_energy_vector = unit_vector_mouv[0] * cinetic_energy, unit_vector_mouv[1] * cinetic_energy

        k = 1

        startX = corps.pos[0] * Game.Camera.zoom + Game.Camera.x
        startY = corps.pos[1] * Game.Camera.zoom + Game.Camera.y

        endX = startX + cinetic_energy_vector[0] * k
        endY = startY + cinetic_energy_vector[1] * k

        pg.draw.line(screen, (255, 0, 0), (startX, startY), (endX, endY), 5)
    return

def draw_text(screen, text, position, font, color=(255, 255, 255)):
    """
    Affiche du texte sur l'écran PyGame
    
    Arguments:
        screen (pg.Surface): L'écran PyGame
        text (str): Texte à afficher
        position (tuple[int, int]): Position du texte
        font (pg.Font): Police de texte
        color: (tuple[int, int, int]): Couleur du texte
        
    Retourne:
        None
    """
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)
    return

def draw_attraction_norm(screen) -> None:
    """
    Dessine une flèche représentant le vecteur de la norme attractionnelle
    
    Arguments:
        screen (pg.Surface): L'écran PyGame
        
    Retourne:
        None
    """
    attractionVectorSum = mouseSpacePos = AVS = screenPosToSpacePos(pg.mouse.get_pos())

    for corps in Game.space:
        attraction_norm: float = .0
        unit_vector: tuple[float, float] = Vectors.get_unit_vector(mouseSpacePos, corps.pos)
        distance: float = Vectors.get_distance(mouseSpacePos, corps.pos)

        if distance > 0:
            attraction_norm: float = (G * corps.mass) / ((distance * 1e3) ** 2)

        attraction_vector: tuple[float, float] = (
            unit_vector[0] * attraction_norm,
            unit_vector[1] * attraction_norm
        )

        attractionVectorSum: tuple[float, float] = (
            attractionVectorSum[0] + attraction_vector[0] * 1e3,
            attractionVectorSum[1] + attraction_vector[1] * 1e3
        )

        AVS: tuple[float, float] = (
            AVS[0] + attraction_vector[0],
            AVS[1] + attraction_vector[1]
        )

    MSP: tuple[float, float] = spacePosToScreenPos(mouseSpacePos)

    drawArrow(MSP, spacePosToScreenPos(attractionVectorSum), l = 5)

    valeur: float = round(sqrt((AVS[0] - mouseSpacePos[0]) ** 2 + (AVS[1] - mouseSpacePos[1]) ** 2), 2)

    x, y = MSP
    pg.draw.line(screen, (255, 255, 255), (x + 4, y - 4), (x + 16, y - 16), 1)
    surface = Game.font.render(str(valeur), False, (255, 255, 255))
    w, h = Game.font.size(str(valeur))
    screen.blit(surface, (x + 18, y - 30))
    u, e = l("attractionNormUnit").split(" ")
    unit(u, e, (w + x + 20, y - 30))
    return



# endregion

# region Converter

def screenPosToSpacePos(pos: tuple[float, float]) -> tuple[float, float]:
    """
    Convertit une position écran en position espace.

    Arguments : 
        pos (tuple[float, float]): Position à convetir
    
    Retourne :
        tuple[float, float] : Position convertie
    """
    x: float = (pos[0] - Game.Camera.x) / Game.Camera.zoom
    y: float = (pos[1] - Game.Camera.y) / Game.Camera.zoom
    return (x, y)

def spacePosToScreenPos(pos: tuple[float, float]) -> tuple[float, float]:
    """
    Convertit une position espace en position écran.

    Arguments : 
        pos (tuple[float, float]): Position à convetir
    
    Retourne :
        tuple[float, float] : Position convertie
    """
    x: float = (pos[0] * Game.Camera.zoom) + Game.Camera.x
    y: float = (pos[1] * Game.Camera.zoom) + Game.Camera.y
    return (x, y)

# endregion

# region Autre


def scientificNotation(value: float | int, position: tuple[int, int], *, end: str | None = None) -> None:
    """
    Affiche une valeur en notation scientifique.

    Arguments: 
        value (float | int): Valeur à afficher en notation scientifique.
        position (tuple[int, int]): Position de l'affichage.
        end (str | None): Texte à afficher à la fin de la notation scientifique.
    
    Retourne:
        None
    """
    strValue: list[str, str] = str(value).split("e")
    mantisse: str = strValue[0][:7]
    e: str = strValue[1] if len(strValue) > 1 else "+0"
    exponent: str = e[1:] if e[0] == "+" else e

    renderedMantisse: str = "%s x 10" % mantisse

    text = Game.font.render(renderedMantisse, False, (255, 255, 255))
    w1, h1 = Game.font.size(renderedMantisse)
    Game.screen.blit(text, (position[0], position[1]))
    
    text = exponentFont.render(exponent, False, (255, 255, 255))
    Game.screen.blit(text, (position[0] + w1, position[1] - 3))

    if end:
        text = Game.font.render(end, False, (255, 255, 255))
        w2, h2 = Game.font.size(exponent)
        Game.screen.blit(text, (position[0] + w1 + w2, position[1]))
    return

def orbitalPeriod(mass: float | int, semimajorAxe: float | int) -> float:
    """
    Calcule la période orbitale d'un corps autour d'un autre.
    Formule selon la troisième loi de Kepler.

    Arguments: 
        mass (float | int): Masse du corps principal en kg.
        semimajorAxe (float | int): Demi-grand axe de l'orbite en km.
    
    Retourne:
        float : La période orbitale en jours.
    """
    return (2 * pi * sqrt((semimajorAxe * 1e3) ** 3 / (G * mass))) / 86400

def barycentre(space: list) -> tuple[int, int]:
    """
    Calcule les coordonnées du barycentre d'un système

    Arguments:
        space (list): Liste des astres du système
    
    Retourne:
        tuple[int, int]: Coordonnées du barycentre
    """
    mX, mY, mass = 0, 0, 0
    for corps in space:
        m: float | int = corps.mass
        x, y = corps.pos
        mX += m * x
        mY += m * y
        mass += m
    if mass == 0:
        return (0, 0)
    return (mX / mass, mY / mass)

def drawArrow(startPos: tuple[int, int], endPos: tuple[int, int], *, color: tuple[int, int, int] = (255, 255, 255), l: int = 2, c: int = 8) -> None:
    """
    Dessine une flèche

    Arguments:
        startPos (tuple[int, int]): Position de départ
        endPos (tuple[int, int]): Position de fin
        color (tuple[int, int, int]): Couleur de la flèche
        l (int): Largeur de la ligne
        c (int): Longueur des cotés du triangle

    Retourne:
        None
    """
    orientation: float = (atan2(startPos[1] - endPos[1], endPos[0] - startPos[0])) + pi/2
    if not (-1e2 < startPos[0] < 1e4 and -1e2 < startPos[1] < 1e4):
        startPos: tuple = (
            endPos[0] - 2000 * sin(orientation),
            endPos[1] - 2000 * cos(orientation)
        )
    if not (-1e2 < endPos[0] < 1e4 and -1e2 < endPos[1] < 1e4):
        endPos: tuple = (
            startPos[0] - 2000 * sin(orientation - pi),
            startPos[1] - 2000 * cos(orientation - pi)
        )
    pg.draw.line(Game.screen, color, startPos, endPos, l)
    pg.draw.polygon(Game.screen, color, (
        (endPos[0] + c * sin(orientation), endPos[1] + c * cos(orientation)),
        (endPos[0] + c * sin(orientation - RAD), endPos[1] + c * cos(orientation - RAD)),
        (endPos[0] + c * sin(orientation + RAD), endPos[1] + c * cos(orientation + RAD)),
    ))
    return

def getAttractor(corps):
    """
    Récupère l'astre qui attire le plus un astre

    Arguments:
        corps (Corps): Astre cible

    Retourne:
        Corps | None: Astre attracteur ou rien
    """
    attractors: dict = {}
    for c in Game.space:
        if c == corps: continue
        distance: float = Vectors.get_distance(c.pos, corps.pos)
        attraction: float = Physics.get_attraction(c.mass, corps.mass, distance, c.velocity, corps.velocity)
        attractors[attraction] = c
    return attractors[max(attractors)] if len(attractors) > 0 else None

def closeTo(n: float | int) -> int:
    """
    Donne le numbre le plus de n entre 1 * k, 2 * k, 5 * k et 10 * k, k étant la puissante de 10 de n

    Arguments:
        n (float | int): Nombre cible

    Retourne:
        int: Le nombre le plus proche de n
    """
    k: int = 10 ** floor(log10(n))
    closest: list = sorted((k, 2 * k, 5 * k, 10 * k), key=lambda x: (abs(n - x), x))
    return closest[0]

def getSize() -> tuple[int, int, str]:
    """
    Récupère la distance entre deux points d'une certaine distance en mètre selon le zoom de la caméra
    
    Arguments:
        None
        
    Retourne:
        tuple[int, int, str]: Respectivement: distance entre les points en px, distance "réelle", unité
    """
    d: float = round(100 * 1e3 / Game.Camera.zoom, 3)
    unit: str = l("m")
    if d > 1e3:
        unit = l("km")
        d = round(100 / Game.Camera.zoom, 3)
    if d > 1e3:
        unit = "x10³ %s" % l("km")
        d = round(100 / Game.Camera.zoom / 1e3, 3)
    if d > 1e3:
        unit = "x10⁶ %s" % l("km")
        d = round(100 / Game.Camera.zoom / 1e6, 3)
    if d > 1e3:
        unit = "x10⁹ %s" % l("km")
        d = round(100 / Game.Camera.zoom / 1e9, 3)
    distance = closeTo(d)
    width: float = distance * 100 / d
    return (width, distance, unit)

def toDate(secondsSinceStarting: float) -> tuple[int, int, int, int, int]:
    """
    Convertit des secondes en date

    Arguments:
        secondsSinceStarting (float): Secondes écoulées depuis le début

    Retourne:
        tuple[int, int, int, int, int]: Date formatée (années, mois, semaines, jours, heures)
    """
    years: int = floor(secondsSinceStarting // 365)
    months: int = floor((secondsSinceStarting - years * 365) // 30)
    weeks: int = floor((secondsSinceStarting - years * 365 - months * 30) // 7)
    days: int = floor(secondsSinceStarting - years * 365 - months * 30 - weeks * 7)
    hours: int = floor((secondsSinceStarting - years * 365 - months * 30 - weeks * 7 - days) * 24)
    return (years, months, weeks, days, hours)

def displayMultilineText(text: str, font, position: tuple[int, int], width: int, *, stop: int = -1, end: str = "...") -> int:
    """
    Affiche un texte sur plusieurs lignes

    Arguments:
        text (str): Texte à afficher
        font (pg.Font): Police utilisée pour écrite le texte
        position (tuple[int, int]): Position du texte
        width (int): Largeur maximale que peut atteindre le texte
        stop (int): Le nombre de lignes maximale
        end (str): Texte à afficher à la fin de la dernière ligne si le nombre de ligne dépasse la limitation

    Retourne:
        int: Hauteur du texte
    """
    text: list = text.split(" ")
    lines: list = []
    h: int = font.size(" ")[1]

    while len(text) > 0:
        line: str = ""
        while len(text) > 0 and font.size(line + text[0])[0] < width:
            line += text.pop(0) + " "
        lines.append(line)
    
    for i, line in enumerate(lines):
        if i + 1 == stop and len(lines) > i + 1:
            surface = font.render(line[:-1] + end, False, (255, 255, 255))
            Game.screen.blit(surface, (position[0], position[1] + h * i))
            break
        else:
            surface = font.render(line, False, (255, 255, 255))
            Game.screen.blit(surface, (position[0], position[1] + h * i))

    return h * len(lines)

def delimiter(position: tuple[int, int], dimension: tuple[int, int], *, padding: int = 10) -> pg.Rect:
    """
    Fonction qui va créer une bordure sur l'écran

    Arguments:
        position (tuple[int, int]): La position du sujet
        dimension (tuple[int, int]): Les dimensions du suejt
        padding (int): L'espace auteur du sujet et de la bordure, en pixels
    
    Retourne:
        pg.Rect: Le rectangle PyGame qui symbolise la bordure
    """
    x, y = position
    w, h = dimension
    return pg.Rect(x - padding, y - padding, w + 2 * padding, h + 2 * padding)

def setHelpMessage(
        surface: pg.Surface,
        startPosition: tuple[int, int],
        startDimension: tuple[int, int],
        border: int, 
        endPosition: tuple[int, int],
        endDimension: tuple[int, int],
        text: str,
        /,
        font: pg.font = descriptionFont
    ) -> None:
    """
    Fonction permettant de créer un message d'aide lorsque le menu d'aide est activé

    Arguments:
        surface (pg.Surface): Surface semi-transparente
        startPosition (tuple[int, int]): Position de départ
        startDimension (tuple[int, int]): Dimension de départ
        border (int): bordure où commence la ligne (1, 2, 3, 4 pour haut, gauche, bas, droite ou ZQSD)
        endPosition (tuple[int, int]): Position de la boîte d'aide
        endDimension (tuple[int, int]): Dimension de la boîte d'aide
        text (str): Texte à afficher dans la boîte d'aide
    
    Retourne:
        None
    """
    pg.draw.rect(surface, (0, 0, 0, 0), delimiter(startPosition, startDimension))
    pg.draw.rect(surface, (255, 255, 255, 255), delimiter(startPosition, startDimension), 1)
    positions: dict[int, tuple[int, int]] = {
        1: (
            ((startPosition[0] + startDimension[0] + 10) - (startDimension[0] + 2 * 10) // 2, startPosition[1] - 10),
            ((endPosition[0] + endDimension[0] + 10) - (endDimension[0] + 2 * 10) // 2, endPosition[1] + endDimension[1])
            ),
        2: (
            (startPosition[0] - 10, (startPosition[1] + startDimension[1] + 10) - (startDimension[1] + 2 * 10) // 2),
            (endPosition[0] + endDimension[0], (endPosition[1] + endDimension[1] + 10) - (endDimension[1] + 2 * 10) // 2)
            ),
        3: (
            ((startPosition[0] + startDimension[0] + 10) - (startDimension[0] + 2 * 10) // 2, startPosition[1] + startDimension[1] + 10),
            ((endPosition[0] + endDimension[0] + 10) - (endDimension[0] + 2 * 10) // 2, endPosition[1])
            ),
        4: (
            (startPosition[0] + startDimension[0] + 10, (startPosition[1] + startDimension[1] + 10) - (startDimension[1] + 2 * 10) // 2),
            (endPosition[0], (endPosition[1] + endDimension[1] + 10) - (endDimension[1] + 2 * 10) // 2)
            )
    }
    startLinePosition, endLinePosition = positions[border]
    pg.draw.line(Game.screen, (255, 255, 255), startLinePosition, endLinePosition)
    pg.draw.rect(surface, (0, 0, 0, 0), (*endPosition, *endDimension))
    pg.draw.rect(surface, (255, 255, 255, 255), (*endPosition, *endDimension), 1)
    displayMultilineText(text, font, (endPosition[0] + 10, endPosition[1] + 10), endDimension[0] - 20)
    return

def displayRotatedImage(surf: pg.Surface, image: pg.image, pos: tuple[int, int], angle: float):
    """
    Fonction permettant d'afficher une image selon une orientation

    Arguments:
        surf (pg.Surface): Surface où doit être affichée l'image
        image (pg.image): Image
        pos (tuple[int, int]): Position de l'image sur la surface
        angle (float): Angle, en degré, de l'orientation de l'image

    Retourne:
        None
    """
    w, h = image.get_size()
    originPos = (w / 2, h / 2)
    imageRect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offsetCenterToPivot = pg.math.Vector2(pos) - imageRect.center
    
    rotatedOffset = offsetCenterToPivot.rotate(-angle)

    rotatedImageCenter = (pos[0] - rotatedOffset.x, pos[1] - rotatedOffset.y)

    rotatedImage = pg.transform.rotate(image, angle)
    rotatedImageRect = rotatedImage.get_rect(center = rotatedImageCenter)

    surf.blit(rotatedImage, rotatedImageRect)
    return

def unit(unit: str, exponent: str, position: tuple[int, int], *, color: tuple[int, int, int] = (255, 255, 255)) -> None:
    """
    Affiche unité avec la notation unité^exposant

    Arguments: 
        unit (str): Unité
        exponent (str): Exposant
        position (tuple[int, int]): Position de l'affichage.
        color (tuple[int, int, int]): Couleur de l'unité
    
    Retourne:
        None
    """
    text = Game.font.render(unit, False, color)
    w1, _ = Game.font.size(unit)
    Game.screen.blit(text, (position[0], position[1]))
    
    text = exponentFont.render(exponent, False, color)
    Game.screen.blit(text, (position[0] + w1, position[1] - 3))
    return

def getNE(n: float) -> tuple[int, int]:
    if "inf" in str(n):
        return (10, 999)
    _n = str(n).split("e")[0]
    e = int(str(n).split("e")[1])
    if not "." in str(n):
        return (int(_n), e)
    d = len(_n.split(".")[1])
    n = int(float(_n) * 10 ** d)
    return (n, e - d)
# endregion