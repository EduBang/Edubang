import pygame as pg
import math
from time import sleep

from physics.Corpse import Corpse
from physics.Gravitation import Gravitation
from physics.Position import Position
from physics.Universe import Universe
from physics.Vector import Vector # Ne fonctionne pas encore.

# Initialisation de Pygame
pg.init()

running = True
resolution = (1000, 800)
screen = pg.display.set_mode(resolution)
w, h = pg.display.get_window_size()
black = (0, 0, 0)
white = (255, 255, 255)
blue = (4, 6, 24)

pg.display.set_caption('EduBang')
icon = pg.image.load('source/Images/icon.png')
pg.display.set_icon(icon)

universe = Universe(screen)

terre = Corpse(10, (100, 100), 50, 0)
terre.color = (0, 0, 255)
terre.addForce(Vector(0, 0, 1))
terre.addForce(Vector(0, 0, 1))

mars = Corpse(5, (500, 500), 50, 0)
mars.color = (255, 50, 50)

universe.addCorpse(terre)
universe.addCorpse(mars)

class items:
    def vector(start_pos, end_pos, width=5):
        # Dessiner le vecteur vert
        pg.draw.line(screen, (0, 255, 0), start_pos, end_pos, width)
        opposite_pos = (end_pos[0] - 0.2 * (end_pos[0] - start_pos[0]), end_pos[1] - 0.2 * (end_pos[1] - start_pos[1]))
        pg.draw.line(screen, (0, 0, 255), end_pos, opposite_pos, width)
    
class game:
    def draw_screen():
        pg.display.update()

    def quit_algo():
        pg.quit()
        quit()



while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(blue)

    pg.draw.circle(screen, (255, 0, 0), (w / 2, h / 2), 30, 0)

    items.vector((200, 200), (400, 200), 5)

    universe.update()
    universe.draw()

    game.draw_screen()

    # sleep(1)

game.quit_algo()
