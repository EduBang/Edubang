from proto import proto
import pygame as pg

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
    def draw(self, screen):
        pg.draw.circle(screen, self.color, (float(self.pos[0]), float(self.pos[1])), self.radius)
    
    @Corps
    def update_position(self, acc, dt):
        self.path.append(self.pos)
        # Mise à jour de la vitesse (conserve l'inertie)
        self.velocity[0] += acc[0] * dt
        self.velocity[1] += acc[1] * dt
        
        # Mise à jour de la position en fonction de la nouvelle vitesse (avec inertie)
        self.pos = (self.pos[0] + self.velocity[0] * dt, self.pos[1] + self.velocity[1] * dt)

