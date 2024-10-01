import pygame as pg
import math

# Initialisation de Pygame
pg.init()

running = True
resolution = (1000, 800)
screen = pg.display.set_mode(resolution)
w, h = pg.display.get_window_size()
black = (0, 0, 0)

pg.display.set_caption('EduBang')
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)

class game:

    @staticmethod
    def draw_screen():
        pg.display.update()

    @staticmethod
    def quit_algo():
        pg.quit()
        quit()

    @staticmethod
    def vector(start_pos, end_pos, width=5):
        # Dessiner le vecteur vert
        pg.draw.line(screen, (0, 255, 0), start_pos, end_pos, width)

        # Calcul de la direction opposée pour le vecteur bleu
        # La direction opposée est obtenue en inversant les coordonnées
        opposite_pos = (end_pos[0] - 0.2 * (end_pos[0] - start_pos[0]), end_pos[1] - 0.2 * (end_pos[1] - start_pos[1]))

        # Dessiner le vecteur bleu dans la direction opposée
        pg.draw.line(screen, (0, 0, 255), end_pos, opposite_pos, width)


while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Remplir l'écran en noir
    screen.fill(black)

    # Dessiner un cercle rouge au centre de l'écran
    pg.draw.circle(screen, (255, 0, 0), (w / 2, h / 2), 30, 0)


    game.vector((200, 200), (400, 200), 5)


    game.draw_screen()

# Quitter proprement
game.quit_algo()
