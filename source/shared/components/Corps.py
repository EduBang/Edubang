from proto import proto
import pygame as pg
from math import pi

from main import Game

with proto("Corps") as Corps:
    @Corps
    def new(self, mass, radius, pos, color, v_initial_x, v_initial_y):
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.color = color
        self.velocity = [v_initial_x, v_initial_y]  # Vitesse initiale
        self.path = []
    
    @Corps
    def draw(self, screen, camera):
        x = float((self.pos[0] + camera.x / camera.zoom) * camera.zoom)
        y = float((self.pos[1] + camera.y / camera.zoom) * camera.zoom)
        if pi * (self.radius * camera.zoom) ** 2 < 10: # Si le corps est trop petit sur l'écran, alors il va l'afficher avec une croix
            pg.draw.line(screen, (255, 255, 255), (x - 8, y), (x + 8, y), 2)
            pg.draw.line(screen, (255, 255, 255), (x, y - 8), (x, y + 8), 2)
            if hasattr(self, "name"): # s'il a l'attribut "name", alors il va l'afficher
                pg.draw.line(screen, (255, 255, 255), (x + 4, y - 4), (x + 16, y - 16), 1)
                surface = Game.font.render(self.name, False, (255, 255, 255))
                screen.blit(surface, (x + 18, y - 30))
        else:
            pg.draw.circle(screen, self.color, (x, y), self.radius * camera.zoom)
    
    @Corps
    def update_position(self, acc, dt):
        self.path.append(self.pos) # Laisser ce code ira consommer environ 4Mo de RAM par seconde pour 10 corps.
        if len(self.path) > 499: # On limite alors la liste du chemin à 100. C'est ajustable.
            self.path.pop(0)
        # Mise à jour de la vitesse (conserve l'inertie)
        self.velocity[0] += acc[0] * dt
        self.velocity[1] += acc[1] * dt
        
        # Mise à jour de la position en fonction de la nouvelle vitesse (avec inertie)
        self.pos = (self.pos[0] + self.velocity[0] * dt, self.pos[1] + self.velocity[1] * dt)

