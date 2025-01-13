import pygame as pg
from math import sqrt, sin, cos, pi
from Perlin import Perlin

# Utilisation de chaînes brutes pour éviter les problèmes d'échappement
path_normal_map = r"sources/test/normal_map.png"
normal_map = pg.image.load(path_normal_map)

planet_pos = (500, 500)  # Position du centre de la planète
radius = 100  # Rayon de la planète

def generate_texture():
    perlin_instance = Perlin(surface_size=radius * 2, center_pos=planet_pos, intensity=255, stretching=(7, 7), zoom=2)
    
    perlin_matrix = perlin_instance.generate_perlin()
    scaled_perlin = perlin_instance.upscale(perlin_matrix)
    planet_texture = pg.Surface((radius * 2, radius * 2))
    perlin_instance.draw_perlin(scaled_perlin, planet_texture, radius)
    return planet_texture


pg.init()
screen = pg.display.set_mode((1000, 1000))  # Initialiser la fenêtre d'affichage
pg.display.set_caption("Test Rendering Planets")
clock = pg.time.Clock()
running = True
planet_texture = generate_texture()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill((0, 0, 0))
    # Afficher la texture de la planète
    screen.blit(planet_texture, (planet_pos[0] - radius, planet_pos[1] - radius))

    pg.display.flip()
    clock.tick(60)  # Cap the frame rate at 60 FPS

pg.quit()
