from types import MethodType
from random import randint

import pygame as pg

from main import Game
from proto import proto
from eventListen import Events
from shared.components.Vectors import *
from shared.components.Corps import *
from shared.components.Physics import *
from shared.components.Captors import *

# region Prototypes

FOCUS_COLOR: tuple[int, int, int] = (13, 178, 190)

UNICODES: dict[int, str] = {
    0x20: "espace",
    0x400000e2: "alt",
    0x400000e0: "ctrl"
}

with proto("Button") as Button:
    def drawButton(self) -> None:
        pg.draw.rect(Game.screen, (255, 255, 255), pg.Rect(self.position, self.size), 0, 8)
        surface = Game.font.render(self.text, False, (0, 0, 0))
        width, height = Game.font.size(self.text)
        x = self.position[0] + (self.size[0] - width) / 2
        y = self.position[1] + (self.size[1] - height) / 2
        Game.screen.blit(surface, (x, y))
        return
    
    def mousemotionBTN(self, event) -> None:
        x, y = event.pos
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondownBTN(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onPressed()
        return
    
    def mousebuttonupBTN(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.onReleased()
        return

    def mousewheelBTN(self, event) -> None:
        if not self.scrollable: return
        self.offsetY = 10 * event.y
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
        self.offsetY = 10 * event.y
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
        surface = self.font.render(self.keyname, False, (0, 0, 0))
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
        self.offsetY = 10 * event.y
        self.position[1] += self.offsetY
        return

    def windowKB(self, w) -> None:
        Events.stopObserving(self)
        return

    def keydownKB(self, event) -> None:
        if self.focus:
            self.key = event.key
            self.keyname = UNICODES[event.key] if event.key in UNICODES else event.unicode 
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
    def new(self, key: int, keyname: str, position: tuple[int, int]) -> None:
        self.focus = False
        self.key = key
        self.keyname = keyname
        self.position = list(position)
        self.font = Game.font
        self.size  = [80, 40]
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
        self.offsetY = 10 * event.y
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
        color = FOCUS_COLOR if self.focus else (255, 255, 255)
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
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.focus = not self.focus
            if self.focus: self.onPressed()
        else:
            self.focus = False
        return
    
    def mousebuttonupI(self, event) -> None:
        button = event.button
        x, y = event.pos
        if button != 1: return
        if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[1] and y < self.position[1] + self.size[1]:
            self.focus = not self.focus
            if self.focus: self.onReleased()
        else:
            self.focus = False
        return
    
    def mousewheelI(self, event) -> None:
        if not self.scrollable: return
        self.offsetY = 10 * event.y
        self.position[1] += self.offsetY
        return

    def windowI(self, w) -> None:
        Events.stopObserving(self)
        return

    def keydownI(self, event) -> None:
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
        self.focus = True
        return

    @Input
    def new(self, text: str, position: tuple[int, int], size: tuple[int, int]) -> None:
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
        self.offsetY = 10 * event.y
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
        self.position = position
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
            self.position = (x - self.size[0] // 2, y)
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
            self.position = (x - self.size[0] // 2, y)
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
    distance = Vectors.get_distance(a, b) # pixel
    attraction = Physics.get_attraction(a.mass, b.mass, distance) # N
    unitVectorA = Vectors.get_unit_vector(a.pos, b.pos)
    unitVectorB = Vectors.get_unit_vector(b.pos, a.pos)
    accA = [unitVectorA[0] * attraction / a.mass, unitVectorA[1] * attraction / a.mass]
    accB = [unitVectorB[0] * attraction / b.mass, unitVectorB[1] * attraction / b.mass]

    # faut que acc en px/s

    a.update_position(accA, Game.deltaTime * Game.timeScale)
    b.update_position(accB, Game.deltaTime * Game.timeScale)
    return distance

# Fonction permettant de mélanger les couleurs de 2 corps selon la surface
def mergeColor(a, b) -> tuple[int, int, int]:
    # C'est un calcul de moyenne pondérée
    surfaceA = pi * a.radius ** 2
    surfaceB = pi * b.radius ** 2
    red = (surfaceA * a.color[0] + surfaceB * b.color[0]) / (surfaceA + surfaceB)
    green = (surfaceA * a.color[1] + surfaceB * b.color[1]) / (surfaceA + surfaceB)
    blue = (surfaceA * a.color[2] + surfaceB * b.color[2]) / (surfaceA + surfaceB)
    return (red, green, blue)


def process_collide(corps1, corps2):
    cinetic_energy_corps1 = Physics.get_cinetic_energy(corps1.mass, Physics.get_velocity(corps1.path[-2], corps1.path[-1], Game.deltaTime * Game.timeScale))
    cinetic_energy_corps2 = Physics.get_cinetic_energy(corps2.mass, Physics.get_velocity(corps2.path[-2], corps2.path[-1], Game.deltaTime * Game.timeScale))
    unit_vector_mouv_corps1 = Vectors.get_unit_vector_mouv(corps1.path[-2], corps1.path[-1])
    unit_vector_mouv_corps2 = Vectors.get_unit_vector_mouv(corps2.path[-2], corps2.path[-1])
    
    cinetic_energy_vector_corps1 = cinetic_energy_corps1 * unit_vector_mouv_corps1[0], cinetic_energy_corps1 * unit_vector_mouv_corps1[1]
    cinetic_energy_vector_corps2 = cinetic_energy_corps2 * unit_vector_mouv_corps2[0], cinetic_energy_corps2 * unit_vector_mouv_corps2[1]
    
    sum_vector_cinetic_energy_corps1 = (cinetic_energy_vector_corps1[0] / corps1.mass, cinetic_energy_vector_corps1[1] / corps1.mass)
    sum_vector_cinetic_energy_corps2 = (cinetic_energy_vector_corps2[0] / corps2.mass, cinetic_energy_vector_corps2[1] / corps2.mass)

    mass = corps1.mass + corps2.mass
    radius = sqrt(((pi * corps1.radius ** 2) + (pi * corps2.radius ** 2)) / pi)
    color = mergeColor(corps1, corps2)
    vInitialX = (sum_vector_cinetic_energy_corps1[0] + sum_vector_cinetic_energy_corps2[0]) / mass
    vInitialY = (sum_vector_cinetic_energy_corps1[1] + sum_vector_cinetic_energy_corps2[1]) / mass

    corps = corps1
    hasChanged = False
    if corps2.radius > corps1.radius:
        corps = corps2
        hasChanged = True
    corps.mass = mass
    corps.radius = radius
    corps.color = color
    corps.velocity = [vInitialX, vInitialY]
    corps.path = []
    if Game.Camera.focus in [corps1, corps2]:
        Game.Camera.focus = corps
    return corps1 if hasChanged else corps2

# endregion

# region Fond espace

def loadSpace(perlin) -> tuple[dict[tuple, tuple], int]:
    noise_matrix = [[perlin.noise(x / 80, y / 80) for y in range(perlin.size)] for x in range(perlin.size)]

    galaxy = {}

    # Code qui génère les amas de galaxies
    for x in range(perlin.size):
        for y in range(perlin.size):
            noise_x = int(x)
            noise_y = int(y)
            noise_val = noise_matrix[noise_x][noise_y]

            # Si le "bruit" est fort, il va générer une galaxie.
            if noise_val > 0.15:
                color = (int(70 * noise_val), int(20 * noise_val), int(70 * noise_val * 0.8))
                galaxy[(x, y)] = color

    return (galaxy, perlin.size)

def loadStars(n: int = 100, position: tuple[int, int] = (-1000, 1000)) -> list[tuple[int, int]]:
    stars = {}
    for i in range(n):
        stars[(randint(position[0], position[1]), randint(position[0], position[1]))] = (255, 255, 255)
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

def draw_attraction_norm(screen, ) -> None: #  chanp gravitation = G*(mass_obj_select / d2)
    list_attraction_norm = []
    mouse_pos = pg.mouse.get_pos()
    
    for corps in Game.space: # fonction retournant une liste avec tout les vecteurs de norme d'attraction pour chaque astre
        unit_vector = get_unit_vector(mouse_pos, corps.pos)
        attraction_norm = Physics.gravitation_constant * (corps.mass / Physics.get_distance(mouse_pos, corps) ** 2)
        attraction_vector = (unit_vector[0] * attraction_norm, unit_vector[1] * attraction_norm)
        list_attraction_norm.append(attraction_vector) # la liste en question
        
        attraction_vector_sum = (0, 0)
        
        for element in list_attraction_norm:
            attraction_vector_sum = (attraction_vector_sum[0] + element[0], attraction_vector_sum[1] + element[1])
        
    endX = mouse_pos[0] + attraction_vector_sum[0] * 100
    endY = mouse_pos[1] + attraction_vector_sum[1] * 100
        
    pg.draw.line(screen, (255, 255, 255), (mouse_pos[0], mouse_pos[1]), (endX, endY), 5)
    

   
# endregion x = float((self.pos[0] + camera.x / camera.zoom) * camera.zoom)