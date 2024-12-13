from math import sqrt
import pygame as pg 
from proto import proto


with proto("Space_ship") as Space_ship:
    @Space_ship
    def new(self, pos, mass, orientation, v_initial_x, v_initial_y):
        self.pos = pos
        self.mass = mass
        self.path = []
        self.orientation = orientation
        self.velocity = [v_initial_x, v_initial_y]
        
    @Space_ship
    def draw_ship(self, screen, camera) -> None:
        x = float((self.pos[0] + camera.x / camera.zoom) * camera.zoom) #dessine une crois a l'emplacement du vaisseau
        y = float((self.pos[1] + camera.y / camera.zoom) * camera.zoom)
        pg.draw.line(screen, (255, 255, 255), (x - 8, y), (x + 8, y), 2)
        pg.draw.line(screen, (255, 255, 255), (x, y - 8), (x, y + 8), 2)
        return
    
    @Space_ship
    def update_position_ship(self, acc, dt) -> None:
        self.path.append(self.pos)
        if len(self.path) > 499:
            self.path.pop(0)
        # Mise à jour de la vitesse (conserve l'inertie)

        # selon prgm, acc en px/s
        self.velocity[0] += acc[0] * dt
        self.velocity[1] += acc[1] * dt
        
        x = self.pos[0] + self.velocity[0] * dt
        y = self.pos[1] + self.velocity[1] * dt

        # Mise à jour de la position en fonction de la nouvelle vitesse (avec inertie)
        self.pos = (x, y)
        return
    

