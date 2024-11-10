from types import MethodType

import pygame as pg

from main import Game
from proto import proto
from eventListen import Events
from shared.components.Vectors import *
from shared.components.Corps import *
from shared.components.Physics import *
from shared.components.Captors import *

with proto("Button") as Button:
    def drawButton(self, screen):
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(self.position, self.size), 0, 8)
        surface = Game.font.render(self.text, False, (0, 0, 0))
        width, height = Game.font.size(self.text)
        x = self.position[0] + (self.size[0] - width) / 2
        y = self.position[1] + (self.size[1] - height) / 2
        screen.blit(surface, (x, y))
        return
    
    def mousemotion(self, position: tuple[int, int]) -> None:
        if position[0] > self.position[0] and position[1] < self.position[0] + self.size[0] and position[1] > self.position[1] and position[1] < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondown(self, position: tuple[int, int], button: int) -> None:
        if button != 1: return
        if position[0] > self.position[0] and position[0] < self.position[0] + self.size[0] and position[1] > self.position[1] and position[1] < self.position[1] + self.size[1]:
            self.onPressed()
        return
    
    def mousebuttonup(self, position: tuple[int, int], button: int) -> None:
        if button != 1: return
        if position[0] > self.position[0] and position[0] < self.position[0] + self.size[0] and position[1] > self.position[1] and position[1] < self.position[1] + self.size[1]:
            self.onReleased()
        return

    def window(self, w):
        Events.stopObserving(self)

    def onHover():
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

    @Button
    def new(self, position: tuple[int, int], size: tuple[int, int]):
        self.text = "Button"
        self.position = position
        self.size = size
        self.draw = MethodType(drawButton, self)
        self.onPressed = lambda: None
        self.onReleased = lambda: None
        self.onHover = onHover
        Events.group(self, [MethodType(mousemotion, self), MethodType(mousebuttondown, self), MethodType(mousebuttonup, self), MethodType(window, self)])
        return

with proto("CheckBox") as CheckBox:
    def drawCheckBox(self, screen):
        color = (0, 0, 255) if self.checked else (255, 255, 255)
        pg.draw.rect(screen, color, pg.Rect(self.position, self.size), 0, 4)
        if color == (0, 0, 255):
            pg.draw.line(screen, (0, 0, 0), (self.position[0] + 7, self.position[1] + 20), (self.position[0] + 17, self.position[1] + 30), 5)
            pg.draw.line(screen, (0, 0, 0), (self.position[0] + 17, self.position[1] + 30), (self.position[0] + 32, self.position[1] + 10), 5)
        return
    
    def mousemotion(self, position: tuple[int, int]) -> None:
        if position[0] > self.position[0] and position[0] < self.position[0] + self.size[0] and position[1] > self.position[1] and position[1] < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondown(self, position: tuple[int, int], button: int) -> None:
        if button != 1: return
        if position[0] > self.position[0] and position[0] < self.position[0] + self.size[0] and position[1] > self.position[1] and position[1] < self.position[1] + self.size[1]:
            self.onPressed()
        return
    
    def mousebuttonup(self, position: tuple[int, int], button: int) -> None:
        if button != 1: return
        if position[0] > self.position[0] and position[0] < self.position[0] + self.size[0] and position[1] > self.position[1] and position[1] < self.position[1] + self.size[1]:
            self.onReleased()
        return

    def window(self, w):
        Events.stopObserving(self)

    def onHover():
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

    @CheckBox
    def onPressed(self):
        self.checked = not self.checked
    
    @CheckBox
    def new(self, position: tuple[int, int], checked: bool = False):
        self.checked = checked
        self.position = position
        self.size  = [40, 40]
        self.draw = MethodType(drawCheckBox, self)
        self.onReleased = lambda: None
        self.onHover = onHover
        Events.group(self, [MethodType(mousemotion, self), MethodType(mousebuttondown, self), MethodType(mousebuttonup, self), MethodType(window, self)])

with proto("MessageBox") as MessageBox:
    @MessageBox
    def draw(self, screen):
        if not self.active: return
        widthScreen, heightScreen = pg.display.get_surface().get_size()
        surface = Game.font.render(self.text, False, (0, 0, 0))
        width, height = Game.font.size(self.text)
        x = widthScreen // 2
        y = heightScreen // 2
        xRect = x - (width + 20) // 2
        yRect = y - (height + 20) // 2
        pg.draw.rect(screen, (255, 255, 255), pg.Rect((xRect , yRect), (width + 20, height + 20)))
        screen.blit(surface, (xRect + 10, yRect + height // 2))
        return
    
    @MessageBox
    def new(self, message: str):
        self.text = message
        self.active = False

with proto("KeyBind") as KeyBind:
    def drawKeyBind(self, screen):
        color = (0, 0, 255) if self.focus else (255, 255, 255)
        pg.draw.rect(screen, color, pg.Rect(self.position, self.size), 0, 4)
        surface = Game.font.render(chr(self.key), False, (0, 0, 0))
        width, height = Game.font.size(chr(self.key))
        x = self.position[0] + width // 2
        y = self.position[1] + height // 2
        screen.blit(surface, (x, y))
        return
    
    def mousemotion(self, position: tuple[int, int]) -> None:
        if position[0] > self.position[0] and position[0] < self.position[0] + self.size[0] and position[1] > self.position[1] and position[1] < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondown(self, position: tuple[int, int], button: int) -> None:
        if button != 1: return
        if position[0] > self.position[0] and position[0] < self.position[0] + self.size[0] and position[1] > self.position[1] and position[1] < self.position[1] + self.size[1]:
            self.onPressed()
        return
    
    def mousebuttonup(self, position: tuple[int, int], button: int) -> None:
        if button != 1: return
        if position[0] > self.position[0] and position[0] < self.position[0] + self.size[0] and position[1] > self.position[1] and position[1] < self.position[1] + self.size[1]:
            self.onReleased()
        else:
            self.focus = False
        return

    def window(self, w):
        Events.stopObserving(self)

    def keydown(self, key: int) -> None:
        if self.focus:
            if 0 < key < 1114112:
                self.key = key
            self.focus = False
        return

    def onHover():
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

    @KeyBind
    def onPressed(self) -> None:
        self.focus = True
        return

    @KeyBind
    def new(self, key: int, position: tuple[int, int]) -> None:
        self.focus = False
        self.key = key
        self.position = position
        self.size  = [40, 40]
        self.draw = MethodType(drawKeyBind, self)
        self.onReleased = lambda: None
        self.onHover = onHover
        Events.group(self, [MethodType(mousemotion, self), MethodType(mousebuttondown, self), MethodType(mousebuttonup, self), MethodType(window, self), MethodType(keydown, self)])

with proto("Text") as Text:
    @Text
    def draw(self, screen) -> None:
        surface = Game.font.render(self.text, self.antialiasing, self.color)
        screen.blit(surface, self.position)

    @Text
    def new(self, text: str, position: tuple[int, int], antialiasing: bool = False, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        self.text = text
        self.position = position
        self.antialiasing = antialiasing
        self.color = color
        self.size = Game.font.size(self.text)


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
    
# Fonction permettant de mettre à jour la postion entre 2 corps.
def updateCorps(a, b) -> float:
    distance = Vectors.get_distance(a, b)
    attraction = Physics.get_attraction(a.mass, b.mass, distance)
    unitVectorA = Vectors.get_unit_vector(a.pos, b.pos)
    unitVectorB = Vectors.get_unit_vector(b.pos, a.pos)
    accA = [unitVectorA[0] * attraction / a.mass, unitVectorA[1] * attraction / a.mass]
    accB = [unitVectorB[0] * attraction / b.mass, unitVectorB[1] * attraction / b.mass]

    a.update_position(accA, Game.dt)
    b.update_position(accB, Game.dt)
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
    cinetic_energy_corps1 = Physics.get_cinetic_energy(corps1.mass, Physics.get_velocity(corps1.path[-2], corps1.path[-1], Game.dt))
    cinetic_energy_corps2 = Physics.get_cinetic_energy(corps2.mass, Physics.get_velocity(corps2.path[-2], corps2.path[-1], Game.dt))
    unit_vector_mouv_corps1 = Vectors.get_unit_vector_mouv(corps1.path[-2], corps1.path[-1])
    unit_vector_mouv_corps2 = Vectors.get_unit_vector_mouv(corps2.path[-2], corps2.path[-1])
    
    cinetic_energy_vector_corps1 = cinetic_energy_corps1 * unit_vector_mouv_corps1[0], cinetic_energy_corps1 * unit_vector_mouv_corps1[1]
    cinetic_energy_vector_corps2 = cinetic_energy_corps2 * unit_vector_mouv_corps2[0], cinetic_energy_corps2 * unit_vector_mouv_corps2[1]
    
    sum_vector_cinetic_energy_corps1 = (cinetic_energy_vector_corps1[0] / corps1.mass, cinetic_energy_vector_corps1[1] / corps1.mass)
    sum_vector_cinetic_energy_corps2 = (cinetic_energy_vector_corps2[0] / corps2.mass, cinetic_energy_vector_corps2[1] / corps2.mass)

    mass = corps1.mass + corps2.mass
    radius = sqrt(((pi * corps1.radius ** 2) + (pi * corps2.radius ** 2)) / pi)
    color = mergeColor(corps1,corps2)
    vInitialX = (corps1.mass * sum_vector_cinetic_energy_corps1[0] + corps2.mass * sum_vector_cinetic_energy_corps2[0]) / mass
    vInitialY = (corps1.mass * sum_vector_cinetic_energy_corps1[1] + corps2.mass * sum_vector_cinetic_energy_corps2[1]) / mass

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


def draw_velocity_vector(self, corps):
    corps_velocity = Physics.get_velocity(corps.path[-2], corps.path[-1], Game.dt)
    unit_vector_mouv = Vectors.get_unit_vector_mouv(corps.path[-2], corps.path[-1])
    velocity_vector = unit_vector_mouv[0] * corps_velocity, unit_vector_mouv[1] * corps_velocity
    return velocity_vector
    
def draw_cinetic_energy_vector(self, corps):
    unit_vector_mouv = Vectors.get_unit_vector_mouv(corps.path[-2], corps.path[-1])
    cinetic_energy = Physics.get_cinetic_energy(corps.mass, Physics.get_velocity(corps.path[-2], corps.path[-1], Game.dt))
    cinetic_energy_vector = unit_vector_mouv * cinetic_energy
    return cinetic_energy_vector
    
