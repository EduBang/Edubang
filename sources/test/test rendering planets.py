import pygame as pg
from math import *
from nsi25perlin import PerlinNoise as perlin 
from perlin_noise import PerlinNoise
import opensimplex

                
planet_pos = (500, 500) # Position du centre de la planète
radius = 100 # Rayon de la planète
Perlin_surface = perlin(radius) #sous dimentionner pour pixeliser
liste = []

def generer_perlin():
    for x in range(Perlin_surface.size):
        liste.append([])
        for y in range(Perlin_surface.size):
            value = Perlin_surface.noise(x / 7, y / 7)
            liste[x].append(value * 255)
    return liste

def upscale(matrix, factor):
    new_matrix = []
    for row in matrix:
        new_row = []
        for element in row:
            new_row.extend([element] * factor)
        for _ in range(factor):
            new_matrix.append(new_row)
    return new_matrix


def draw_perlin(new_liste, screen, planet_pos, radius):
    start_pos = (planet_pos[0] - radius // 2, planet_pos[1] - radius // 2)

    for x, element in enumerate(new_liste):
        for y, value in enumerate(element):
            pixel_pos = (x + start_pos[0], y + start_pos[1])

            if sqrt((planet_pos[0] - pixel_pos[0]) ** 2 + (planet_pos[1] - pixel_pos[1]) ** 2) <= radius:

                if value <= 0:
                    screen.set_at((int(x + start_pos[0]), int(y + start_pos[1])),(11, 89, 134)) #eau profonde
                if value <= 5 and value > 0:
                    screen.set_at((int(x + start_pos[0]), int(y + start_pos[1])),(19, 128, 191)) #eau peu profonde
                if value > 5 and value <= 35:
                    screen.set_at((int(x + start_pos[0]), int(y + start_pos[1])),(228, 197, 23)) #sable
                if value > 35 and value <= 100:
                    screen.set_at((int(x + start_pos[0]), int(y + start_pos[1])),(75, 161, 68))  #herbe
                if value > 100 and value <= 150:
                    screen.set_at((int(x + start_pos[0]), int(y + start_pos[1])),(148, 141, 132)) #montagne
                if value > 150:
                    screen.set_at((int(x + start_pos[0]), int(y + start_pos[1])),(82, 82, 82)) #montagne haute





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
        draw_perlin(upscale(liste, 4), screen, planet_pos, radius)
        
        pg.display.flip()
        clock.tick(60)  

    pg.quit()

main()