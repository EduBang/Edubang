import pygame as pg
import math

from Physics.Corpse import Corpse
from Physics.Gravitation import Gravitation
from Physics.Position import Position
from Physics.Universe import Universe
from Physics.Vector import Vector # Ne fonctionne pas encore.

# Initialisation de Pygame
pg.init()

running = True
resolution = (1000, 800)
screen = pg.display.set_mode(resolution)
w, h = pg.display.get_window_size()
black = (0, 0, 0)

pg.display.set_caption('EduBang')
icon = pg.image.load('source/Images/icon.png')
pg.display.set_icon(icon)

universe = Universe(screen)

# La gravitation se calculera automatiquement plus tard.
tGravitation = Gravitation(10)
tPosition = Position(100, 100)
terre = Corpse(10, tPosition, 50, tGravitation, 0)

mGravitation = Gravitation(5)
mPosition = Position(500, 500)
mars = Corpse(5, mPosition, 50, mGravitation, 0)

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

    screen.fill(black)

    pg.draw.circle(screen, (255, 0, 0), (w / 2, h / 2), 30, 0)

    items.vector((200, 200), (400, 200), 5)

    universe.update()
    universe.draw()

    game.draw_screen()


game.quit_algo()
