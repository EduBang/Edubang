# Projet : EduBang
# Auteurs : Anaël Chevillard, Sacha Fréguin, Néji Lim

from math import sqrt
from nsi25perlin import PerlinNoise as perlin
from proto import proto
from PIL import Image

with proto("Perlin") as Perlin:

    @Perlin 
    def new(self, surface_size: int, center_pos: tuple[int, int], intensity: int, stretching: tuple[int, int], zoom: int):
        self.surface_size = surface_size
        self.center_pos = center_pos
        self.intensity = intensity
        self.stretching = stretching
        self.zoom = zoom
        self.perlin = perlin()
        self.fm = self.final_matrix()

    @Perlin
    def generate_perlin(self):
        return [[self.perlin.noise(x / self.stretching[0], y / self.stretching[1]) * self.intensity for y in range(self.surface_size)] for x in range(self.surface_size)]

    @Perlin
    def upscale(self, matrix):
        return [[element for element in row for _ in range(self.zoom)] for row in matrix for _ in range(self.zoom)]
    
    @Perlin
    def final_matrix(self):
        perlin_matrix = self.generate_perlin()
        c_matrix = color_matrix(self, perlin_matrix)
        scaled_perlin_colored = self.upscale(c_matrix)
        return scaled_perlin_colored
    



    @Perlin 
    def color_matrix(self, matrix):
        # fm = self.fm
        center_pos = self.center_pos
        color_matrix = []
        for row in matrix:
            color_row = []
            for element in row:
                element = normalize(element, -140, 140)




                if element >= 0 and element < 40:
                    color_row.append((11, 89, 134))  # eau profonde
                if element >= 40 and element < 50:
                    color_row.append((19, 128, 191))  # eau peu profonde
                if element >= 50 and element < 55:
                    color_row.append((228, 197, 23))  # plage
                if element >= 55 and element < 80:
                    color_row.append((75, 161, 68))  # herbe
                if element >= 80 and element < 95:
                    color_row.append((148, 141, 132))  # montagne
                else:
                    color_row.append((82, 82, 82))  # montagne haute
            color_matrix.append(color_row)
        return color_matrix

    @Perlin
    def generate_img(self, final_matrix):
        # Créer une nouvelle image avec PIL
        new_image = Image.new('RGBA', (self.surface_size * self.zoom, self.surface_size * self.zoom))
        
        # Obtenir la matrice de couleurs
        color_matrix = final_matrix

        start_x = self.center_pos[0] - self.surface_size // 2
        start_y = self.center_pos[1] - self.surface_size // 2

        
        # Parcourir la matrice de couleurs et définir les pixels dans l'image
        for x, row in enumerate(color_matrix):
            for y, color in enumerate(row):
                if sqrt((x - self.surface_size // 2) ** 2 + (y - self.surface_size // 2) ** 2) > self.surface_size // 2 :
                    continue
                new_image.putpixel((y, x), color)
        
        return new_image
    

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) * 100