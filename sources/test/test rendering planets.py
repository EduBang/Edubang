import pygame as pg
from math import *
from nsi25perlin import PerlinNoise as perlin 
import opensimplex

                
planet_pos = (500, 500) # Position du centre de la planète
radius = 100 # Rayon de la planète
Perlin_surface = perlin(radius * 2)
liste = []

def generer_perlin():
    for x in range(Perlin_surface.size):
        liste.append([])
        for y in range(Perlin_surface.size):
            value = Perlin_surface.noise(x / 100, y / 100)
            liste[x].append(value * 255)
    return liste

def draw_perlin(liste, screen, planet_pos, radius):
    start_pos = (planet_pos[0] - radius, planet_pos[1] - radius)

    for x, element in enumerate(liste):
        for y, value in enumerate(element):
            pixel_pos = (x + start_pos[0], y + start_pos[1])

            if sqrt((planet_pos[0] - pixel_pos[0]) ** 2 + (planet_pos[1] - pixel_pos[1]) ** 2) <= radius:
                screen.set_at((int(x + start_pos[0]), int(y + start_pos[1])),(abs(value), abs(value), abs(value)))




def main():
   
    screen = pg.display.set_mode((1000, 1000))  # Initialiser la fenêtre d'affichage
    pg.display.set_caption("Test Rendering Planets")
    clock = pg.time.Clock()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))

        generer_perlin()
        draw_perlin(liste, screen, planet_pos, radius)
        
        pg.display.flip()
        clock.tick(60)  

    pg.quit()

main()