from types import MethodType
from random import randint
from math import pi

import pygame as pg

from main import Game, getFont
from proto import proto
from eventListen import Events
from shared.components.Vectors import Vectors
from shared.components.Physics import Physics, G

type EnergyInfos = tuple[int, tuple[int, int], tuple[int, int]]

# La constante d'EduBang
# valeur de calibrage, origine à déterminer
C_EDUBANG = 10750

exponentFont = getFont("Medium", 12)

# region Prototypes

FOCUS_COLOR: tuple[int, int, int] = (13, 178, 190)

UNICODES: dict[int, str] = {
    0x20: "espace",
    0x400000e2: "alt",
    0x400000e0: "ctrl"
}

UNICODES_DARWIN: dict[int, str] = {
    0x31: "espace",
    0x37: "alt",
    0x3b: "cmd"
}

Game.ctrl = pg.KMOD_LCTRL if Game.os == "Windows" else pg.KMOD_META
C_UNICODES = UNICODES if Game.os == "Windows" else UNICODES_DARWIN
fnKeys: tuple = (0x400000e2 if Game.os == "Windows" else 0x37, 0x400000e0 if Game.os == "Windows" else 0x3b)

SCROLL_SPEED: int = 20

with proto("Button") as Button:
    def drawButton(self) -> None:
        if not self.active: return 
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect(self.position, self.size), 0, 8)
        surface = Game.font.render(self.text, False, (0, 0, 0))
        width, height = Game.font.size(self.text)
        x = self.position[0] + (self.size[0] - width) / 2
        y = self.position[1] + (self.size[1] - height) / 2
        Game.screen.blit(surface, (x, y))
        return
    
    def mousemotionBTN(self, event) -> None:
        if not self.active: return
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownBTN(self, event) -> None:
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onPressed()
        return
    
    def mousebuttonupBTN(self, event) -> None:
        if not self.active: return
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onReleased()
        return

    def mousewheelBTN(self, event) -> None:
        if not self.active: return
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowBTN(self, w) -> None:
        Events.stopObserving(self)
        return

    def onHover() -> None:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        return

    @Button
    def new(self, position: tuple[int, int], size: tuple[int, int]) -> None:
        self.text = "Button"
        self.position = list(position)
        self.size = size
        self.draw = MethodType(drawButton, self)
        self.onPressed = lambda: None
        self.onReleased = lambda: None
        self.onHover = onHover
        self.scrollable = False
        self.offsetY = 0
        self.active = True
        Events.group(self, {
            "mousemotion": MethodType(mousemotionBTN, self),
            "mousebuttondown": MethodType(mousebuttondownBTN, self),
            "mousebuttonup": MethodType(mousebuttonupBTN, self),
            "mousewheel": MethodType(mousewheelBTN, self),
            "window": MethodType(windowBTN, self)
            })
        return

with proto("CheckBox") as CheckBox:
    def drawCheckBox(self) -> None:
        color = FOCUS_COLOR if self.checked else (255, 255, 255)
        pg.draw.rect(Game.screen, color, pg.Rect(self.position, self.size), 0, 4)
        if color == FOCUS_COLOR:
            pos1 = (self.position[0] + 5.25, self.position[1] + 15)
            pos2 = (self.position[0] + 12.75, self.position[1] + 22.5)
            pos3 = (self.position[0] + 24, self.position[1] + 7.5)
            pg.draw.line(Game.screen, (255, 255, 255), pos1, pos2, 4)
            pg.draw.line(Game.screen, (255, 255, 255), pos2, pos3, 4)
        return
    
    def mousemotionCB(self, event) -> None:
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownCB(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onPressed()
        return
    
    def mousebuttonupCB(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onReleased()
        return
    
    def mousewheelCB(self, event) -> None:
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowCB(self, w) -> None:
        Events.stopObserving(self)
        return

    def onHover() -> None:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        return

    @CheckBox
    def onPressed(self) -> None:
        self.checked = not self.checked
        return
    
    @CheckBox
    def new(self, position: tuple[int, int], checked: bool = False) -> None:
        self.checked = checked
        self.position = list(position)
        self.size  = [30, 30]
        self.draw = MethodType(drawCheckBox, self)
        self.onReleased = lambda: None
        self.onHover = onHover
        self.scrollable = False
        self.offsetY = 0
        Events.group(self, {
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
        if not self.active: return
        widthScreen, heightScreen = pg.display.get_surface().get_size()
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
        self.text = message
        self.active = False
        return

with proto("KeyBind") as KeyBind:
    def drawKeyBind(self):
        color = FOCUS_COLOR if self.focus else (255, 255, 255)
        pg.draw.rect(Game.screen, color, pg.Rect(self.position, self.size), 0, 4)
        surface = self.font.render(" + ".join(self.keyname), False, (0, 0, 0))
        x = self.position[0] + 10
        y = self.position[1] + 10
        Game.screen.blit(surface, (x, y))
        return
    
    def mousemotionKB(self, event) -> None:
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownKB(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onPressed()
        return
    
    def mousebuttonupKB(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onReleased()
        return
    
    def mousewheelKB(self, event) -> None:
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowKB(self, w) -> None:
        Events.stopObserving(self)
        return

    def keydownKB(self, event) -> None:
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
                self.keyname.append("espace" if event.key in C_UNICODES else event.unicode if event.key > 0x110000 else chr(event.key))
                self.keys.append(event.key)
                self.focus = False
        return

    def onHover() -> None:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        return

    @KeyBind
    def onPressed(self) -> None:
        self.focus = True
        return

    @KeyBind
    def new(self, keys: list[int], keyname: str, position: tuple[int, int]) -> None:
        self.focus = False
        self.keys = keys
        self.keyname = keyname
        self.position = list(position)
        self.font = Game.font
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
        surface = self.font.render(self.text, self.antialiasing, self.color)
        Game.screen.blit(surface, self.position)
        return

    def mousewheelT(self, event) -> None:
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    @Text
    def new(self, text: str, position: tuple[int, int], antialiasing: bool = False, color: tuple[int, int, int] = (0, 0, 0), font=Game.font) -> None:
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
        color = FOCUS_COLOR if self.focus and self.active else (255, 255, 255)
        pg.draw.rect(Game.screen, color, pg.Rect(self.position, self.size), 0, 4)
        surface = self.font.render(self.text, False, (0, 0, 0))
        dim = self.font.size(self.text)
        x = self.position[0] + 5
        y = self.position[1] + self.size[1] // 2 - dim[1] // 2
        Game.screen.blit(surface, (x, y))
        return
    
    def mousemotionI(self, event) -> None:
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownI(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if not self.active: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.focus = not self.focus
            if self.focus:
                self.onPressed()
                if self.resetOnClick: self.text = ""
        else:
            self.focus = False
        return
    
    def mousebuttonupI(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if not self.active: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.focus = not self.focus
            if self.focus: self.onReleased()
        else:
            self.focus = False
        return
    
    def mousewheelI(self, event) -> None:
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowI(self, w) -> None:
        Events.stopObserving(self)
        return

    def keydownI(self, event) -> None:
        if not self.active: return
        if self.focus:
            if event.key in [pg.K_RETURN, pg.K_ESCAPE, pg.K_TAB]:
                self.focus = False
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if self.numberOnly:
                    if not event.unicode.isdigit():
                        return
                self.text += event.unicode
        return

    def onHover() -> None:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        return

    @Input
    def onPressed(self) -> None:
        if not self.active: return
        self.focus = True
        return

    @Input
    def new(self, text: str, position: tuple[int, int], size: tuple[int, int]) -> None:
        self.active = True
        self.focus = False
        self.text = text
        self.position = position
        self.size  = size
        self.draw = MethodType(drawInput, self)
        self.onReleased = lambda: None
        self.afterInput = lambda: None
        self.onHover = onHover
        self.font = Game.font
        self.numberOnly = False
        self.scrollable = False
        self.resetOnClick = False
        self.offsetY = 0
        Events.group(self, {
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
        if self.active:
            pos = pg.mouse.get_pos()
            value = pos[0] - self.position[0]
            if value > self.size[0]:
                value = self.values[1]
            elif value < 0:
                value = self.values[0]
            self.value = value

        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect(self.position, self.size), 0, 8)
        pg.draw.rect(Game.screen, FOCUS_COLOR, pg.Rect(self.position, (self.value, 5)), 0, 8)
        pg.draw.circle(Game.screen, FOCUS_COLOR, (self.position[0] + self.value, self.position[1] + 2.5), 5)
        return
    
    def mousemotionSB(self, event) -> None:
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownSB(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onPressed()
        else:
            self.active = False
        return
    
    def mousebuttonupSB(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onReleased()
        else:
            self.active = False
        return
    
    def mousewheelSB(self, event) -> None:
        if not self.scrollable: return
        self.offsetY = SCROLL_SPEED * event.y
        self.position[1] += self.offsetY
        return

    def windowSB(self, w) -> None:
        Events.stopObserving(self)
        return

    def onHover() -> None:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        return

    @SlideBar
    def onPressed(self) -> None:
        self.active = True
        return

    @SlideBar
    def onReleased(self) -> None:
        self.active = False
        return

    @SlideBar
    def new(self, position: tuple[int, int]) -> None:
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

# prototype pour garder des variables
with proto("DataKeeper") as DataKeeper:
    @DataKeeper
    def new(self):
        return

with proto("Path") as Path:
    # dessiner trajectoire terre
    @Path
    def draw_corps_path(self, screen, path, color):
        for pos in path:
            x = float((pos[0] + Game.Camera.x / Game.Camera.zoom) * Game.Camera.zoom)
            y = float((pos[1] + Game.Camera.y / Game.Camera.zoom) * Game.Camera.zoom)
            pg.draw.circle(screen, color, (x, y), 1)

with proto("SizeViewer") as SizeViewer:
    def drawSizeViewer(self):
        width, text = getSize()
        x, y = self.position
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect((x, y), (width, 2)))
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect((x, y - 8), (2, 10)))
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect((x + 100, y - 8), (2, 10)))
        surface = Game.font.render(text, False, (255, 255, 255))
        Game.screen.blit(surface, (x, y + 10))
        w, h = Game.font.size(text)
        self.size = (w if w > 100 else 100, h + 60)
        return

    def getSize() -> tuple[int, str]:
        unit = "km"
        distance = round(100 / Game.Camera.zoom, 3)
        if Game.Camera.zoom < 0.1:
            unit = "x10³ km"
            distance = round(100 / Game.Camera.zoom / 1000, 3)
            if distance > 1000:
                unit = "x10⁶ km"
                distance = round(100 / Game.Camera.zoom / 1000000, 3)
        elif Game.Camera.zoom > 100:
            unit = "m"
            distance = round((100 / Game.Camera.zoom) * 1000, 3)

        return (100, f"{distance} {unit}")

    def mousemotionSV(self, event) -> None:
        x, y = event.pos
        if self.focus:
            self.position = [x - self.size[0] // 2, y]
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownSV(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.focus = True
            self.position = [x - self.size[0] // 2, y]
        return
    
    def mousebuttonupSV(self, event) -> None:
        button = event.button
        if button != 1: return
        self.focus = False
        return
    
    def windowSV(self, w) -> None:
        Events.stopObserving(self)
        return

    def onHover() -> None:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        return

    @SizeViewer
    def new(self, position: tuple[int, int]) -> None:
        self.position = list(position)
        self.draw = MethodType(drawSizeViewer, self)
        self.size = (0, 0)
        self.focus = False
        Events.group(self, {
            "mousemotion": MethodType(mousemotionSV, self),
            "mousebuttondown": MethodType(mousebuttondownSV, self),
            "mousebuttonup": MethodType(mousebuttonupSV, self),
            "window": MethodType(windowSV, self)
            })
        return

# endregion

# region Fonctions physiques

# Fonction permettant de mettre à jour la postion entre 2 corps.
def updateCorps(a, b) -> float:
    distance: float = Vectors.get_distance(a.pos, b.pos)
    attraction: float = Physics.get_attraction(a.mass, b.mass, distance)
    unitVectorA: tuple[float] = Vectors.get_unit_vector(a.pos, b.pos)
    unitVectorB: tuple[float] = (-unitVectorA[0], -unitVectorA[1])
    accA: tuple[float, float] = (unitVectorA[0] * attraction / a.mass, unitVectorA[1] * attraction / a.mass)
    accB: tuple[float, float] = (unitVectorB[0] * attraction / b.mass, unitVectorB[1] * attraction / b.mass)

    a.update_position(accA, Game.DT)
    b.update_position(accB, Game.DT)
    return distance

# Fonction permettant de mélanger les couleurs de 2 corps selon la surface
def mergeColor(a, b) -> tuple[int, int, int]:
    # C'est un calcul de moyenne pondérée
    surfaceA: float = pi * a.radius ** 2
    surfaceB: float = pi * b.radius ** 2
    red: float = (surfaceA * a.color[0] + surfaceB * b.color[0]) / (surfaceA + surfaceB)
    green: float = (surfaceA * a.color[1] + surfaceB * b.color[1]) / (surfaceA + surfaceB)
    blue: float = (surfaceA * a.color[2] + surfaceB * b.color[2]) / (surfaceA + surfaceB)
    return (red, green, blue)

# Fonction permettant de fusionner le nom de 2 astres selon leur masse
def mergeNames(d1: tuple[int, str], d2: tuple[int, str]) -> str:
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
    aName = getattr(a, "name", None)
    bName = getattr(b, "name", None)
    c.name = aName or bName
    if aName and bName:
        x1 = a if a.mass < b.mass else b
        x2 = b if x1 == a else a
        dominationIndex: float = x2.mass * 100 / x1.mass
        c.name = x1 if 10 < dominationIndex else mergeNames((x1.mass, x1.name), (x2.mass, x2.name))
        return

def mergeEnergy(d1: EnergyInfos, d2: EnergyInfos) -> tuple[float, float]:
    mass: int = d1[0] + d2[0]

    cineticEnergyCorps1: float = Physics.get_cinetic_energy(d1[0], Physics.get_velocity(d1[1], d1[2], Game.DT))
    cineticEnergyCorps2: float = Physics.get_cinetic_energy(d2[0], Physics.get_velocity(d2[1], d2[2], Game.DT))

    unitVectorMouvCorps1: float = Vectors.get_unit_vector_mouv(d1[1], d1[2])
    unitVectorMouvCorps2: float = Vectors.get_unit_vector_mouv(d2[1], d2[2])

    cineticEnergyVectorCorps1: float = cineticEnergyCorps1 * unitVectorMouvCorps1[0], cineticEnergyCorps1 * unitVectorMouvCorps1[1]
    cineticEnergyVectorCorps2: float = cineticEnergyCorps2 * unitVectorMouvCorps2[0], cineticEnergyCorps2 * unitVectorMouvCorps2[1]
    
    sumVectorCineticEnergyCorps1: float = (cineticEnergyVectorCorps1[0] / d1[0], cineticEnergyVectorCorps1[1] / d1[0])
    sumVectorCineticEnergyCorps2: float = (cineticEnergyVectorCorps2[0] / d2[0], cineticEnergyVectorCorps2[1] / d2[0])

    x: float = (sumVectorCineticEnergyCorps1[0] + sumVectorCineticEnergyCorps2[0]) / mass
    y: float = (sumVectorCineticEnergyCorps1[1] + sumVectorCineticEnergyCorps2[1]) / mass

    return (x, y)

def process_collide(corps1, corps2):
    x, y = mergeEnergy((corps1.mass, corps1.pos, corps1.path[-1]), (corps2.mass, corps2.pos, corps2.path[-1]))

    mass: int = corps1.mass + corps2.mass
    radius: float = (((pi * corps1.radius ** 2) + (pi * corps2.radius ** 2)) / pi) ** .5
    color: tuple[float, float, float] = mergeColor(corps1, corps2)

    corps = corps1
    hasChanged: bool = False
    if corps2.mass > corps1.mass:
        corps = corps2
        hasChanged = True
    corps.mass = mass
    corps.radius = radius
    corps.color = color
    corps.velocity = [x, y]
    corps.path = []
    processMergingNames(corps1, corps2, corps)
    if Game.Camera.focus in [corps1, corps2]:
        Game.Camera.focus = corps
    return corps1 if hasChanged else corps2

# endregion

# region Fond espace

def loadSpace(perlin) -> tuple[dict[tuple, tuple], int]:
    galaxy = {}

    # Code qui génère les amas de galaxies
    for x in range(perlin.size):
        for y in range(perlin.size):
            value = perlin.noise(x / 80, y / 80)

            # Si le "bruit" est fort, il va générer une galaxie.
            if value > 0.15:
                galaxy[(x, y)] = (int(70 * value), int(20 * value), int(70 * value * 0.8))

    return (galaxy, perlin.size)

def loadStars(n: int = 100, position: tuple[int, int] = (-1000, 1000)) -> list[tuple[int, int]]:
    stars = []
    for i in range(n):
        stars.append((randint(position[0], position[1]), randint(position[0], position[1])))
    return stars

# endregion

# region Vecteur
def draw_velocity_vector(screen, corps) -> None:
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
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)
    return

font = pg.font.Font(None, 24)

def draw_attraction_norm(screen) -> None:

    # Récupérer la position de la souris
    mouse_pos: tuple[int, int] = pg.mouse.get_pos()

    # Initialisation du vecteur résultant (au départ centré sur la souris)
    attraction_vector_sum: tuple[float, float] = (.0, .0)

    # Conversion de la position écran vers la position espace
    # x: float = (mouse_pos[0] - 1280 / 2) / Game.Camera.zoom + Game.Camera.x
    # y: float = (mouse_pos[1] - 720 / 2) / Game.Camera.zoom + Game.Camera.y
    mouseSpacePos: tuple[float, float] = screenPosToSpacePos(mouse_pos)

    # Calcul de l'attraction gravitationnelle pour chaque corps
    for corps in Game.space:
        attraction_norm: float = .0
        unit_vector: tuple[float, float] = Vectors.get_unit_vector(mouseSpacePos, corps.pos)
        distance = Vectors.get_distance(mouseSpacePos, corps.pos)

        if distance > 0:  # Éviter la division par zéro
            attraction_norm = G * (corps.mass / ((distance * 1000 / Game.Camera.zoom) ** 2))

        attraction_vector = (
            unit_vector[0] * attraction_norm,
            unit_vector[1] * attraction_norm
        )

        attraction_vector_sum = (
            attraction_vector_sum[0] + attraction_vector[0],
            attraction_vector_sum[1] + attraction_vector[1]
        )

    # Calcul des coordonnées de la fin du vecteur résultant (espace -> écran)
    # endX: float = (attraction_vector_sum[0] + Game.Camera.x / Game.Camera.zoom) * Game.Camera.zoom
    # endY: float = (attraction_vector_sum[1] + Game.Camera.y / Game.Camera.zoom) * Game.Camera.zoom

    pg.draw.line(screen, (255, 255, 255), mouse_pos, spacePosToScreenPos(attraction_vector_sum), 5)

    screen_width, screen_height = screen.get_size()

    # Coordonnées fixes pour le bas et au centre
    draw_text(screen, f"Pointeur écran : {mouse_pos}", (screen_width // 2 - 100, screen_height - 60), font)
    draw_text(screen, f"Position espace : ({mouseSpacePos[0]:.2f}, {mouseSpacePos[1]:.2f})", (screen_width // 2 - 150, screen_height - 40), font)
    draw_text(screen, 
              f"Vecteur de norme : ({attraction_vector_sum[0]:.2e}, {attraction_vector_sum[1]:.2e})", 
              (screen_width // 2 - 200, screen_height - 20), font)

# endregion

# region Converter

def screenPosToSpacePos(pos: tuple[float, float]) -> tuple[float, float]:
    x: float = (Game.Camera.x + pos[0]) / Game.Camera.zoom
    y: float = (Game.Camera.y + pos[1]) / Game.Camera.zoom
    return (x, y)

def spacePosToScreenPos(pos: tuple[float, float]) -> tuple[float, float]:
    x: float = (pos[0] + Game.Camera.x / Game.Camera.zoom) * Game.Camera.zoom
    y: float = (pos[1] + Game.Camera.y / Game.Camera.zoom) * Game.Camera.zoom
    return (x, y)

# endregion

# region Autre

def updateSpaceship(a, b) -> float:
    distance: float = Vectors.get_distance(a.pos, b.pos) # pixel
    attraction: float = Physics.get_attraction(a.mass, b.mass, distance)
    unitVectorA: tuple[float, float] = Vectors.get_unit_vector(a.pos, b.pos)
    unitVectorB: tuple[float, float] = (-unitVectorA[0], -unitVectorA[1])
    accA: tuple[float, float] = [(unitVectorA[0] * attraction / a.mass) + unitVectorA[1] * attraction / a.mass]
    accB: tuple[float, float] = [unitVectorB[0] * attraction / b.mass, unitVectorB[1] * attraction / b.mass]

    a.update_position(accA, Game.deltaTime * Game.timeScale)
    b.update_position(accB, Game.deltaTime * Game.timeScale)
    return distance

def scientificNotation(value, position, *, end: str | None = None) -> None:
    strMass: list[str, str] = value.__str__().split("e")
    mantisse: str = strMass[0]
    exponent: str = strMass[1][1:]

    renderedMantisse: str = "%s x 10" % mantisse

    text = Game.font.render(renderedMantisse, False, (255, 255, 255))
    w1, h1 = Game.font.size(renderedMantisse)
    Game.screen.blit(text, (position[0], position[1]))
    
    text = exponentFont.render(exponent, False, (255, 255, 255))
    w2, h2 = Game.font.size(exponent)
    Game.screen.blit(text, (position[0] + w1, position[1] - 3))

    if end:
        text = Game.font.render(end, False, (255, 255, 255))
        Game.screen.blit(text, (position[0] + w1 + w2, position[1]))
    return

# endregion