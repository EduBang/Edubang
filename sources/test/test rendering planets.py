import pygame as pg
from math import *
from nsi25perlin import PerlinNoise as perlin 

Perlin_surface = perlin(200)
liste = []

def generer_perlin():
    for x in range(Perlin_surface.size):
        liste.append([])
        for y in range(Perlin_surface.size):
            value = Perlin_surface.noise(x / 2000, y / 2000)
            liste[x].append(value * 255)
    return liste




def draw_perlin(liste, screen, center, radius = 100):
    pos = (
        center[0] - radius,
        center[1] - radius
    )

    center = (center[0] + radius, center[1] + radius)

    for x, element in enumerate(liste):
        for y, value in enumerate(element):
            
            dx, dy = (pos[0] + x), (pos[1] + y)

            
            if sqrt((center[0] - dx )**2 + (center[1] - dy )**2) <= radius:
                screen.set_at((int(x + pos[0]), int(y + pos[1])),(abs(value), abs(value), abs(value)))

 

    










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
        draw_perlin(liste, screen, (630, 300))

        
        pg.display.flip()
        clock.tick(60)  

    pg.quit()

main()