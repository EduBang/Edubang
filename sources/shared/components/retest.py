import pygame as pg
from math import sqrt, sin, cos, pi
from proto import proto
from rePerlin import Perlin
from PIL import Image

# Utilisation de chaînes brutes pour éviter les problèmes d'échappement
path_normal_map = r"sources/test/normal_map.png"
normal_map = pg.image.load(path_normal_map)

planet_pos = (500, 500)  # Position du centre de la planète
radius = 100  # Rayon de la planète

pg.init()
screen = pg.display.set_mode((1000, 1000))  # Initialiser la fenêtre d'affichage
pg.display.set_caption("Test Rendering Planets")
clock = pg.time.Clock()
running = True
intensity = 255

# Initialiser la police
pg.font.init()
font = pg.font.SysFont('Arial', 30)

def pil_to_pygame(image):
    """Convertir une image PIL en surface Pygame."""
    mode = image.mode
    size = image.size
    data = image.tobytes()
    return pg.image.fromstring(data, size, mode)

def generate_texture(intensity):
    perlin_instance = Perlin(surface_size=radius * 2, center_pos=planet_pos, intensity=intensity, stretching=(7, 7), zoom=4)
    pil_image = perlin_instance.generate_img()
    return pil_to_pygame(pil_image)

planet_surface = generate_texture(intensity)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                intensity += 1
                planet_surface = generate_texture(intensity)
            elif event.key == pg.K_e:
                intensity -= 1
                planet_surface = generate_texture(intensity)

    screen.fill((0, 0, 0))
    screen.blit(planet_surface, (planet_pos[0] - radius, planet_pos[1] - radius))
    
    # Dessiner le texte avec la valeur de l'intensité
    intensity_text = font.render(f'Intensité: {intensity}', True, (255, 255, 255))
    screen.blit(intensity_text, (10, 10))
    
    pg.display.flip()
    clock.tick(60)  # Cap the frame rate at 60 FPS

pg.quit()