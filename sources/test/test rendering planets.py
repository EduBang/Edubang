import pygame as pg
from math import *
from nsi25perlin import PerlinNoise as perlin 
from perlin_noise import PerlinNoise
import opensimplex

                
planet_pos = (500, 500) # Position du centre de la planète
radius = 100 # Rayon de la planète
Perlin_surface = perlin(radius * 2)
liste = []
block_size = 10

def generer_perlin():
    for x in range(Perlin_surface.size):
        liste.append([])
        for y in range(Perlin_surface.size):
            value = Perlin_surface.noise(x / 40, y / 40)
            liste[x].append(value * 255)

            Perlin_surface.octaves = -100000
    return liste

def draw_perlin(liste, screen, planet_pos, radius):
    start_pos = (planet_pos[0] - radius, planet_pos[1] - radius)

    for x, element in enumerate(liste):
        for y, value in enumerate(element):
            pixel_pos = (x + start_pos[0], y + start_pos[1])

            if sqrt((planet_pos[0] - pixel_pos[0]) ** 2 + (planet_pos[1] - pixel_pos[1]) ** 2) <= radius:
                if value <= 0:
                    screen.set_at((int(x + start_pos[0]), int(y + start_pos[1])),(0, 0, 255))

                if value > 0 and value <= 35:
                    screen.set_at((int(x + start_pos[0]), int(y + start_pos[1])),(255, 218, 51))
                if value > 35:
                    screen.set_at((int(x + start_pos[0]), int(y + start_pos[1])),(75, 161, 68))
                
""""""


"""def generate_open_simplex_noise():"""








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