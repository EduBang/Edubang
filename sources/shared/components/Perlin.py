#Projet : EduBang
#Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

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
        self.final_matrix = final_matrix()

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

    @Perlin
    def final_matrix(self):
        perlin_matrix = generate_perlin(Perlin.surface_size, Perlin.stretching, Perlin.intensity)
        scaled_perlin = upscale(perlin_matrix, Perlin.zoom)
        return scaled_perlin
