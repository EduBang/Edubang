import pygame as pg
from math import sqrt
from nsi25perlin import PerlinNoise  # Assurez-vous que ce module est installé et accessible
from proto import proto

with proto("Perlin") as Perlin:
    """
    Génère une surface de bruit de Perlin avec les paramètres donnés

    Args:
        surface_size (int): Taille de la surface en largeur et hauteur
        center_pos (tuple[int, int]): Position centrale de la surface (position de la planète)
        intensity (int): Intensité du bruit (entre 1 et 255)
        stretching (tuple[int, int]): Étirement du bruit (x et y) > 1
        zoom (int): Zoom du bruit (pixelisation)
    """
    @Perlin
    def new(self, surface_size, center_pos, intensity, stretching, zoom):
        self.surface_size = surface_size
        self.center_pos = center_pos
        self.intensity = intensity
        self.stretching = stretching
        self.zoom = zoom
        self.noise = PerlinNoise()

    @Perlin
    def generate_perlin(self):
        return [[self.noise.noise(x / self.stretching[0], y / self.stretching[1]) * self.intensity for y in range(self.surface_size)] for x in range(self.surface_size)]

    @Perlin
    def upscale(self, matrix):
        return [[element for element in row for _ in range(self.zoom)] for row in matrix for _ in range(self.zoom)]

    @Perlin
    def draw_perlin(self, matrix, surface, radius):
        start_x, start_y = self.center_pos[0] - radius, self.center_pos[1] - radius
        for x, row in enumerate(matrix):
            for y, value in enumerate(row):
                pixel_pos = (x + start_x, y + start_y)
                if sqrt((self.center_pos[0] - pixel_pos[0]) ** 2 + (self.center_pos[1] - pixel_pos[1]) ** 2) <= radius:
                    # Convertir value en une couleur RGB
                    value = min(max(int(value), 0), 255)
                    color = (value, value, value)
                    surface.set_at((x, y), color)