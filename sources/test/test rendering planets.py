import pygame as pg
from math import sqrt, sin, cos
from nsi25perlin import PerlinNoise as perlin

# Utilisation de chaînes brutes pour éviter les problèmes d'échappement
path_normal_map = r"sources/test/normal_map.png"
normal_map = pg.image.load(path_normal_map)

planet_pos = (500, 500)  # Position du centre de la planète
radius = 100  # Rayon de la planète
Perlin_surface = perlin(radius)  # sous-dimensionner pour pixeliser

def generate_texture_with_lighting():
    def generer_perlin(surface):
        size = surface.size
        return [[surface.noise(x / 7, y / 7) * 255 for y in range(size)] for x in range(size)]

    def upscale(matrix, factor):
        return [[element for element in row for _ in range(factor)] for row in matrix for _ in range(factor)]

    def draw_perlin(matrix, surface, planet_pos, radius):
        start_x, start_y = planet_pos[0] - radius, planet_pos[1] - radius
        for x, row in enumerate(matrix):
            for y, value in enumerate(row):
                pixel_pos = (x + start_x, y + start_y)
                if sqrt((planet_pos[0] - pixel_pos[0]) ** 2 + (planet_pos[1] - pixel_pos[1]) ** 2) <= radius:
                    color = get_color(value)
                    surface.set_at((x, y), color)

    def get_color(value):
        if value <= 0:
            return (11, 89, 134)  # eau profonde
        elif value <= 5:
            return (19, 128, 191)  # eau peu profonde
        elif value <= 35:
            return (228, 197, 23)  # sable
        elif value <= 100:
            return (75, 161, 68)  # herbe
        elif value <= 150:
            return (148, 141, 132)  # montagne
        else:
            return (82, 82, 82)  # montagne haute

    def apply_lighting(texture, light_direction):
        width, height = texture.get_size()
        lighting_surface = pg.Surface((width, height), pg.SRCALPHA)
        for x in range(width):
            for y in range(height):
                dx, dy = x - width / 2, y - height / 2
                distance = sqrt(dx ** 2 + dy ** 2)
                if distance == 0:
                    continue
                normal = [dx / distance, dy / distance]
                intensity = max(0, min(1, normal[0] * light_direction[0] + normal[1] * light_direction[1]))
                r, g, b, a = texture.get_at((x, y))
                lighting_surface.set_at((x, y), (int(r * intensity), int(g * intensity), int(b * intensity), a))
        return lighting_surface

    perlin_matrix = generer_perlin(Perlin_surface)
    scaled_perlin = upscale(perlin_matrix, 4)
    planet_texture = pg.Surface((radius * 2, radius * 2))
    draw_perlin(scaled_perlin, planet_texture, planet_pos, radius)
    return planet_texture, apply_lighting

def main():
    pg.init()
    screen = pg.display.set_mode((1000, 1000))  # Initialiser la fenêtre d'affichage
    pg.display.set_caption("Test Rendering Planets")
    clock = pg.time.Clock()
    running = True

    planet_texture, apply_lighting = generate_texture_with_lighting()
    time = 0  # Variable de temps pour faire tourner la lumière

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Calculer la direction de la lumière en fonction du temps pour qu'elle pointe vers l'extérieur
        light_direction = (cos(time), sin(time))
        norm = sqrt(light_direction[0] ** 2 + light_direction[1] ** 2)
        light_direction = (light_direction[0] / norm, light_direction[1] / norm)  # Normalisation de la direction de la lumière
        lighting_texture = apply_lighting(planet_texture, light_direction)
        # Afficher l'image éclairée
        screen.blit(lighting_texture, (planet_pos[0] - radius, planet_pos[1] - radius))

        pg.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

        time += 0.01  # Incrémenter le temps pour faire tourner la lumière

    pg.quit()

main()