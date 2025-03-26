#Projet : EduBang
#Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

from math import sqrt
from nsi25perlin import PerlinNoise as perlin
from proto import proto
from PIL import Image
import pygame as pg

with proto("Perlin") as Perlin:

    @Perlin 
    def new(self, surface_size: int, center_pos: tuple[int, int], intensity: int, stretching: tuple[int, int], zoom: int):
        self.surface_size = surface_size
        self.center_pos = center_pos
        self.intensity = intensity
        self.stretching = stretching
        self.zoom = zoom
        self.perlin = perlin()
        self.ladder = self.color_ladder()
        self.fm = self.final_matrix()
        

    @Perlin
    def generate_perlin(self):
        return [[self.perlin.noise(x / self.stretching[0], y / self.stretching[1]) * self.intensity for y in range(self.surface_size)] for x in range(self.surface_size)]

    @Perlin
    def upscale(self, zoom, matrix):
        return [[element for element in row for _ in range(zoom)] for row in matrix for _ in range(zoom)]
    
    @Perlin
    def final_matrix(self):
        perlin_matrix = self.generate_perlin()
        scaled_perlin = self.upscale(self.zoom, perlin_matrix)           
        scaled_c_matrix = self.color_matrix(scaled_perlin, self.ladder)

        # print(perlin_matrix)
        # # scaled_perlin_colored = self.upscale(c_matrix)
        return scaled_c_matrix

    @Perlin
    def color_ladder(self):
        ladder =  [((0, 40), (230, 230, 180)),  # Jaune très pâle  
                 ((40, 50), (240, 240, 200)),  # Jaune blanchâtre  
                 ((50, 55), (250, 250, 220)),  # Presque blanc avec une touche de jaune  
                 ((55, 70), (255, 255, 230)),  # Blanc chaud légèrement teinté  
                 ((70, 80), (255, 255, 240)),  # Blanc solaire éclatant  
                 ((80, 95), (255, 255, 250)),  # Blanc pur  
                 ((95, 100), (255, 255, 255)), # Blanc aveuglant  
                 ((100, 105), (255, 255, 255)) # Blanc absolu, lumière maximale  
                ]



            
        return ladder
        

    @Perlin 
    def color_matrix(self, matrix, ladder):
        center_pos = self.center_pos
        color_matrix = []
        for row in matrix:
            color_row = []
            for element in row:
                element = normalize(element, -255, 255)
                inc = 0
                for item in ladder:
                    if item[inc][inc] <= element < item[inc][inc + 1]:
                        color_row.append(item[inc + 1])
                        
                        inc += 1
                    
            color_matrix.append(color_row)
        # print(color_matrix)
        return color_matrix

    @Perlin
    def generate_img(self, final_matrix):
        # Créer une nouvelle image avec PIL
        # new_image = Image.new('RGB', (self.surface_size * self.zoom, self.surface_size * self.zoom))
        new_image = pg.Surface((self.surface_size * self.zoom, self.surface_size * self.zoom), pg.SRCALPHA )
        
        # Obtenir la matrice de couleurs
        fm = final_matrix

        start_x = self.center_pos[0] - self.surface_size // 2
        start_y = self.center_pos[1] - self.surface_size // 2

        
        # Parcourir la matrice de couleurs et définir les pixels dans l'image
        for x, row in enumerate(fm):
            for y, color in enumerate(row):
                if sqrt((x - (self.surface_size * self.zoom) // 2) ** 2 + (y - (self.surface_size * self.zoom) // 2) ** 2) > (self.surface_size * self.zoom) // 2 :
                    continue
                new_image.set_at((x, y), (*color, 255))
        
        return new_image
    

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) * 100