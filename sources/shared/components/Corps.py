from math import pi

from proto import proto
import pygame as pg

from ..utils.utils import spacePosToScreenPos
from .Relative import lorentzFactor

with proto("Corps") as Corps:
    @Corps
    def new(self, mass: int | float, radius: int, pos: tuple[int, int], color: tuple[int, int, int], v_initial: tuple[float, float]) -> None:
        self.mass = mass # kilogramme
        self.radius = radius # kilomètre
        self.pos = pos
        self.color = color
        self.velocity = list(v_initial)  # Vitesse initiale
        self.path = []
        return
    
    @Corps
    def draw(self, screen, camera) -> None:
        x, y = spacePosToScreenPos(self.pos)
        if pi * (self.radius * camera.zoom) ** 2 < 10: # Si le corps est trop petit sur l'écran, alors il va l'afficher avec une croix
            pg.draw.line(screen, (255, 255, 255), (x - 8, y), (x + 8, y), 2)
            pg.draw.line(screen, (255, 255, 255), (x, y - 8), (x, y + 8), 2)
        else:
            pg.draw.circle(screen, self.color, (x, y), self.radius * camera.zoom)
        return
    
    @Corps
    def update_position(self, acc, dt) -> None:
        self.path.append(self.pos) # Laisser ce code ira consommer environ 4Mo de RAM par seconde pour 10 corps.
        if len(self.path) > 499: # On limite alors la liste du chemin à 500. C'est ajustable.
            self.path.pop(0)
        # Mise à jour de la vitesse (conserve l'inertie)

        gamma: float = lorentzFactor((self.velocity[0] ** 2 + self.velocity[1] ** 2) ** .5)

        # selon prgm, acc en km/s
        self.velocity[0] += acc[0] * dt / gamma
        self.velocity[1] += acc[1] * dt / gamma

        # Mise à jour de la position en fonction de la nouvelle vitesse (avec inertie)
        self.pos = (
            self.pos[0] + self.velocity[0] * dt,
            self.pos[1] + self.velocity[1] * dt
        )
        return
