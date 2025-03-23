# Projet : EduBang
# Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

import pygame as pg
from math import sqrt, sin, cos, pi
from rePerlin import  Perlin

# Utilisation de chaînes brutes pour éviter les problèmes d'échappement
path_normal_map = r"data/images/assets/assets/normal_map.png"
normal_map = pg.image.load(path_normal_map)

planet_pos = (500, 500)  # Position du centre de la planète
radius = 100  # Rayon de la planète

def generate_texture():
    perlin_instance = Perlin(surface_size=radius * 2, center_pos=planet_pos, intensity=255, stretching=(7, 7), zoom=4, scale=2)
    
    perlin_matrix = perlin_instance.generate_perlin()
    scaled_perlin = perlin_instance.upscale(perlin_matrix)
    planet_texture = pg.Surface((radius * 2 * perlin_instance.zoom, radius * 2 * perlin_instance.zoom))
    
    for x in range(radius * 2 * perlin_instance.zoom):
        for y in range(radius * 2 * perlin_instance.zoom):
            value = scaled_perlin[x][y]
            color = (value, value, value)
            planet_texture.set_at((x, y), color)
    
    return planet_texture, perlin_instance

pg.init()
screen = pg.display.set_mode((1000, 1000))  # Initialiser la fenêtre d'affichage
pg.display.set_caption("Test Rendering Planets")
clock = pg.time.Clock()
running = True
planet_texture, a = generate_texture()
zoom = 1.0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                zoom *= 1.1
            elif event.button == 5:  # Scroll down
                zoom /= 1.1

    screen.fill((0, 0, 0))
    scaled_texture = pg.transform.scale(planet_texture, (int(radius * 2 * zoom), int(radius * 2 * zoom)))
    screen.blit(scaled_texture, (planet_pos[0] - radius * zoom, planet_pos[1] - radius * zoom))
    pg.display.flip()
    clock.tick(60)  # Cap the frame rate at 60 FPS

pg.quit()