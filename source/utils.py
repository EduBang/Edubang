from types import MethodType

import pygame as pg

from proto import proto
from eventListen import Events

pg.font.init()
font = pg.font.SysFont("Comic Sans MS", 12)

with proto("Button") as Button:
    def drawButton(self, screen):
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(self.position, self.size))
        surface = font.render(self.text, False, (0, 0, 0))
        width, height = font.size(self.text)
        x = self.position[0] + (self.size[0] - width) / 2
        y = self.position[1] + (self.size[1] - height) / 2
        screen.blit(surface, (x, y))
        return
    
    def mousemotion(self, position: tuple[int, int]) -> None:
        mouseX, mouseY = pg.mouse.get_pos()
        if mouseX > self.position[0] and mouseX < self.position[0] + self.size[0] and mouseY > self.position[1] and mouseY < self.position[1] + self.size[1]:
            self.onHover()
            Events.trigger("hovering", self)
        else:
            Events.trigger("unhovering", self)
        return

    def mousebuttondown(self, position: tuple[int, int], button: int) -> None:
        mouseX, mouseY = pg.mouse.get_pos()
        if mouseX > self.position[0] and mouseX < self.position[0] + self.size[0] and mouseY > self.position[1] and mouseY < self.position[1] + self.size[1]:
            self.onPressed()
        return
    
    def mousebuttonup(self, position: tuple[int, int], button: int) -> None:
        mouseX, mouseY = pg.mouse.get_pos()
        if mouseX > self.position[0] and mouseX < self.position[0] + self.size[0] and mouseY > self.position[1] and mouseY < self.position[1] + self.size[1]:
            self.onReleased()
        return

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
        Events.group(self, [MethodType(mousemotion, self), MethodType(mousebuttondown, self), MethodType(mousebuttonup, self)])
        return