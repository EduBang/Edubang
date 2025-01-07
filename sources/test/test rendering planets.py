import pygame as pg
from math import sqrt, sin, cos, pi
from nsi25perlin import PerlinNoise as perlin
import numpy as np

# Utilisation de chaînes brutes pour éviter les problèmes d'échappement
path_normal_map = r"C:\Users\sacha\OneDrive\Documents\GitHub\Edubang\sources\test\normal_map.png"
normal_map = pg.image.load(path_normal_map)

planet_pos = (500, 500)  # Position du centre de la planète
radius = 100  # Rayon de la planète
Perlin_surface = perlin(radius)  # sous-dimensionner pour pixeliser
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

def draw_perlin(new_liste, surface, planet_pos, radius):
    start_pos = (planet_pos[0] - radius, planet_pos[1] - radius)

    for x, element in enumerate(new_liste):
        for y, value in enumerate(element):
            pixel_pos = (x + start_pos[0], y + start_pos[1])

            if sqrt((planet_pos[0] - pixel_pos[0]) ** 2 + (planet_pos[1] - pixel_pos[1]) ** 2) <= radius:
                if value <= 0:
                    surface.set_at((x, y), (11, 89, 134))  # eau profonde
                elif value <= 5:
                    surface.set_at((x, y), (19, 128, 191))  # eau peu profonde
                elif value <= 35:
                    surface.set_at((x, y), (228, 197, 23))  # sable
                elif value <= 100:
                    surface.set_at((x, y), (75, 161, 68))  # herbe
                elif value <= 150:
                    surface.set_at((x, y), (148, 141, 132))  # montagne
                else:
                    surface.set_at((x, y), (82, 82, 82))  # montagne haute

def apply_lighting(texture, light_direction, planet_pos, radius):
    width, height = texture.get_size()
    lighting_surface = pg.Surface((width, height), pg.SRCALPHA)

    for x in range(width):
        for y in range(height):
            dx = x - width / 2
            dy = y - height / 2
            distance = np.sqrt(dx ** 2 + dy ** 2)

            if distance == 0:
                continue

            normal = np.array([dx / distance, dy / distance])
            intensity = np.dot(normal, light_direction)
            intensity = np.clip(intensity, 0, 1)

            r, g, b, a = texture.get_at((x, y))
            r = int(r * intensity)
            g = int(g * intensity)
            b = int(b * intensity)

            lighting_surface.set_at((x, y), (r, g, b, a))

    return lighting_surface

def main():
    pg.init()
    screen = pg.display.set_mode((1000, 1000))  # Initialiser la fenêtre d'affichage
    pg.display.set_caption("Test Rendering Planets")
    clock = pg.time.Clock()
    running = True

    generer_perlin()
    scaled_perlin = upscale(liste, 4)
    planet_texture = pg.Surface((radius * 2, radius * 2))

    time = 0  # Variable de temps pour faire tourner la lumière

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Calculer la direction de la lumière en fonction du temps
        light_direction = np.array([cos(time), sin(time)])
        light_direction = light_direction / np.linalg.norm(light_direction)  # Normalisation de la direction de la lumière

        draw_perlin(scaled_perlin, planet_texture, planet_pos, radius)
        lighting_texture = apply_lighting(planet_texture, light_direction, planet_pos, radius)

        # Afficher l'image éclairée
        screen.blit(lighting_texture, (planet_pos[0] - radius, planet_pos[1] - radius))

        pg.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

        time += 0.01  # Incrémenter le temps pour faire tourner la lumière

    pg.quit()

main()