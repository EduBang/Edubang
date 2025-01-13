import pygame as pg
from math import sqrt, sin, cos
from nsi25perlin import PerlinNoise as perlin
from proto import proto


with proto("Perlin") as Perlin:

    @Perlin 
    def new(self, surface, surface_size: int, center_pos: tuple[int, int], intensity: int, stretching: tuple[int, int], zoom: int):
        self.surface = surface
        self.surface_size = surface_size
        self.center_pos = center_pos
        self.intensity = intensity
        self.stretching = stretching
        self.zoom = zoom

    """
    Génère une surface de bruit de Perlin avec les paramètres donnés

    Args:
        surface (PerlinNoise): écran
        surface_size (int): Taille de la surface en largeur et hauteur
        center_pos (tuple[int, int]): Position centrale de la surface (position de la planète)
        intensity (int): Intensité du bruit (entre 1 et 255)
        stretching (tuple[int, int]): Étirement du bruit (x et y) > 1
        zoom (int): Zoom du bruit (pixelisation)
    """

    @Perlin
    def generate_perlin(self, surface, stretching, intensity):
        return [[surface.noise(x / stretching[0], y / stretching[1]) * intensity for y in range(self.surface_size)] for x in range(self.surface_size)]

    @Perlin
    def upscale(matrix, zoom):
        return [[element for element in row for _ in range(zoom)] for row in matrix for _ in range(zoom)]
    
    @Perlin
    def draw_perlin(self, matrix, surface, center_pos, radius):
        start_x, start_y = center_pos[0] - radius, center_pos[1] - radius
        for x, row in enumerate(matrix):
            for y, value in enumerate(row):
                pixel_pos = (x + start_x, y + start_y)
                if sqrt((center_pos[0] - pixel_pos[0]) ** 2 + (center_pos[1] - pixel_pos[1]) ** 2) <= radius:
                    surface.set_at((x, y), value)

    perlin_matrix = generate_perlin(Perlin.surface_size, Perlin.stretching, Perlin.intensity)

    scaled_perlin = upscale(perlin_matrix, Perlin.zoom)

    perlin_texture = pg.Surface(Perlin.surface_size, Perlin.surface_size)

    draw_perlin(scaled_perlin, perlin_texture, Perlin.center_pos, Perlin.surface_size // 2)



