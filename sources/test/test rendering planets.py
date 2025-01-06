import pygame as pg
from math import *
from nsi25perlin import PerlinNoise as perlin 

Perlin_surface = perlin(200)
liste = []

def generer_perlin():
    for x in range(Perlin_surface.size):
        liste.append([])
        for y in range(Perlin_surface.size):
            value = Perlin_surface.noise(x / 20, y / 20)
            liste[x].append(value * 255)
    return liste

def draw_perlin(liste, screen, pos_x = 640, pos_y = 300, radius = 100):

    for x, element in enumerate(liste):

        for y, value in enumerate(element):

            if sqrt((x + radius / 2) ** 2 + (y + radius / 2) ** 2) <= radius:
                screen.set_at((int(x + pos_x + radius / 2), int(y + pos_y + radius / 2)),(abs(value), abs(value), abs(value)))

def main():
   
    screen = pg.display.set_mode((1280, 720))  # Initialiser la fenêtre d'affichage
    pg.display.set_caption("Test Rendering Planets")
    clock = pg.time.Clock()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))

        generer_perlin()
        draw_perlin(liste, screen)

        
        pg.display.flip()
        clock.tick(60)  

    pg.quit()

main()