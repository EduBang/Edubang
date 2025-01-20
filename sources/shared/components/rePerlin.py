import pygame as pg
from math import sqrt, sin, cos
from nsi25perlin import PerlinNoise as perlin
from proto import proto

with proto("Perlin") as Perlin:

    @Perlin 
    def new(self, surface_size: int, center_pos: tuple[int, int], intensity: int, stretching: tuple[int, int], zoom: int):
        self.surface_size = surface_size
        self.center_pos = center_pos
        self.intensity = intensity
        self.stretching = stretching
        self.zoom = zoom
        self.perlin = perlin()
        self.surface = pg.Surface((surface_size * zoom, surface_size * zoom))
        self.fm = self.final_matrix()

    @Perlin
    def generate_perlin(self):
        return [[self.perlin.noise(x / self.stretching[0], y / self.stretching[1]) * self.intensity for y in range(self.surface_size)] for x in range(self.surface_size)]

    @Perlin
    def upscale(self, matrix):
        return [[element for element in row for _ in range(self.zoom)] for row in matrix for _ in range(self.zoom)]
    
    @Perlin
    def draw_perlin(self, matrix, surface, center_pos, radius):
        start_x, start_y = center_pos[0] - radius, center_pos[1] - radius
        for x, row in enumerate(matrix):
            for y, value in enumerate(row):
                pixel_pos = (x + start_x, y + start_y)
                if sqrt((center_pos[0] - pixel_pos[0]) ** 2 + (center_pos[1] - pixel_pos[1]) ** 2) <= radius:
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

    @Perlin
    def final_matrix(self):
        perlin_matrix = self.generate_perlin()
        scaled_perlin = self.upscale(perlin_matrix)
        return scaled_perlin