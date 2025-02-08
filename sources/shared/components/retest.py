# Projet : EduBang
# Auteurs : Anaël Chevillard, Sacha Fréguin, Néji Lim

import pygame as pg
from math import sqrt, sin, cos, pi, radians, acos, degrees, atan2
from proto import proto
from rePerlin import Perlin
from PIL import Image
import numpy as np

with proto("Vectors") as Vectors:
    @Vectors
    def get_distance(self, pos1, pos2) -> float:
        return sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))
    
    @Vectors
    def get_unit_vector(self, pos1, pos2) -> tuple[float, float]:
        x_v_unit = y_v_unit = .0
        dif_x: float = pos2[0] - pos1[0]
        dif_y: float = pos2[1] - pos1[1]
        distance: float = sqrt(dif_x ** 2 + dif_y ** 2)
        
        if distance != 0:
            x_v_unit = dif_x / distance
            y_v_unit = dif_y / distance
        
        return (x_v_unit, y_v_unit)

    @Vectors
    def get_unit_vector_mouv(self, pos_init, pos_final) -> tuple[float | int, float | int]:
        unit_vector_mouv: tuple[float, float] = (.0, .0)
        dX, dY = pos_final[0] - pos_init[0], pos_final[1] - pos_init[1]
        if dX != 0 or dY != 0:
            mouv_vector: tuple[float, float] = (dX, dY)
            norm_mouv_vector: float = sqrt(mouv_vector[0] ** 2 + mouv_vector[1] ** 2)
            unit_vector_mouv = (mouv_vector[0] / norm_mouv_vector, mouv_vector[1] / norm_mouv_vector)
        return unit_vector_mouv

with proto("Angles") as Angles:
    @Angles
    def generate_unit_vector_angle(self, angle: float):
        """
        Fonction qui trouve le vecteur unitaire selon l'angle donné en degrés
        
        Arguments:
            angle (float): Angle en degrés
            
        Retourne:
            tuple[float, float]: Le vecteur unitaire
        """
        return (cos(radians(angle)), sin(radians(angle)))
    
    @Angles
    def generate_angle_whith_unit_vector(self, unit_vector_x: float, unit_vector_y: float):
        """
        Fonction qui trouve l'angle en degrés selon un vecteur unitaire
        
        Arguments:
            unit_vector (tuple[float, float]): Vecteur unitaire
            
        Retourne:
            float: L'angle en degrés
        """
        return round(degrees(atan2(unit_vector_y, unit_vector_x)))
    
    @Angles
    def rotate_image(self, image, angle, center):
        """
        Fait tourner une image autour de son centre.

        :param image: Surface pygame à faire tourner
        :param angle: Angle de rotation en degrés (sens anti-horaire)
        :param center: Coordonnées (x, y) du centre de rotation
        :return: Nouvelle surface tournée et son rectangle positionné correctement
        """
        rotated_image = pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=center)
        return rotated_image, new_rect


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



# def fusion_shadows_planets(l_matrix):



#     for matrix in l_matrix:

#         rgb = np.minimum(matrix[..., :3] + matrix[..., :3], 255)

#         alpha = np.minimum(matrix[..., 3] + matrix[..., 3], 255)

#         fused_arr = np.dstack((rgb, alpha)).astype(np.uint8)
#         fusion_image = Image.fromarray(fused_arr, 'RGBA')

#         return fusion_image
#     # print(l_matrix)
#     # width = len(l_matrix[0])  # Nombre de colonnes (largeur)
#     # height = len(l_matrix[0][0])  # Nombre de lignes (hauteur)

    # # Créer une nouvelle image PIL en mode RGBA
    # fusion_image = Image.new('RGBA', (width, height))

    # new_matrix = []
    # inc = 0

    # for matrix in l_matrix:
    #     for x in range(width):
    #         for y in range(height):
    #             r, g, b, a = matrix[x][y]
    #             new_matrix.append((r, g, b, min(a + inc, 255)))  # Alpha ne dépasse pas 255
    #             inc += a  # Incrémentation progressive de la transparence

    # # Créer une image PIL sans utiliser NumPy
    # fusion_image.putdata(new_matrix)
    
    # fusion_data = np.zeros((height, width, 4), dtype=np.uint8)
    
    # for matrix in l_matrix:
    #     alpha = matrix[..., 3]
    #     fusion_data[..., 3] += alpha
    #     fusion_data[..., 3] = np.clip(fusion_data[..., 3], 0, 255)
    
    # fusion_image = Image.fromarray(fusion_data, 'RGBA')

pg.init()
screen = pg.display.set_mode((1000, 1000))  # Initialiser la fenêtre d'affichage
pg.display.set_caption("Test Rendering Planets")
clock = pg.time.Clock()
pg.font.init()
font = pg.font.SysFont('Arial', 30)

image_shadow_planet = pg.image.load("data/images/planet_shadow.png")
planet_pos = (500, 500)  # Position du centre de la planète
radius = 150  # Rayon de la planète
running = True
intensity = 255

l_light = [(750 ,0)]
# l_matrix = []
l_image = []


for light_pos in l_light:
    unit_vector_light = Vectors.get_unit_vector(light_pos, planet_pos)
    
    print(f"Unit vector : {unit_vector_light}")
    angle = Angles.generate_angle_whith_unit_vector(unit_vector_light[0], unit_vector_light[1])
    print(f"Angle trouvé : {angle}°")

    size_image_shadow_planet = pg.transform.scale(image_shadow_planet, (radius * 2 + 10, radius * 2 + 10))
    rotated_image_shadow_planet, new_rect = Angles.rotate_image(size_image_shadow_planet, angle, planet_pos)
    print(type(rotated_image_shadow_planet))

    l_image.append(rotated_image_shadow_planet)
    # Convertir la surface Pygame en tableau numpy
    # rotated_image_shadow_planet_array = pg.surfarray.array3d(rotated_image_shadow_planet)
    
    # matrix = []
    # for x in range(rotated_image_shadow_planet_array.shape[0]):
    #     row = []
    #     for y in range(rotated_image_shadow_planet_array.shape[1]):
    #         pixel = rotated_image_shadow_planet_array[x, y]
    #         row.append(pixel)
    #     matrix.append(row)
    # width, height = rotated_image_shadow_planet.get_size()  # Récupérer dimensions correctes
    # pixels = list(pg.PixelArray(rotated_image_shadow_planet))  # Extraire pixels
    # matrix = [pixels[i * width:(i + 1) * width] for i in range(height)]
    # matrix = np.array(rotated_image_shadow_planet, dtype=np.uint16)

    # l_matrix.append(matrix)

# fusioned_image_shadow = fusion_shadows_planets(l_matrix)

# unit_vector_light = Vectors.get_unit_vector(planet_pos, light_pos)
# print(f"Unit vector : {unit_vector_light}")
# angle = Angles.generate_angle_whith_unit_vector(unit_vector_light[0], unit_vector_light[1])
# # angle = -90
# print(f"Angle trouvé : {angle}°")

planet_surface = generate_texture(intensity)

# size_image_shadow_planet = pg.transform.scale(image_shadow_planet, (radius*2 + 10, radius*2 + 10))
# rotated_image_shadow_planet, new_rect = Angles.rotate_image(size_image_shadow_planet, angle, planet_pos)

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
    #afficher planette :
    screen.blit(planet_surface, (planet_pos[0] - radius, planet_pos[1] - radius))
    for image in l_image:
        screen.blit(image, new_rect.topleft)
    pg.draw.circle(screen, (255, 0, 0), (light_pos), 100)
    # afficher ombre :
    # screen.blit(rotated_image, (500, 500))
    
    # Dessiner le texte avec la valeur de l'intensité
    intensity_text = font.render(f'Intensité: {intensity}', True, (255, 255, 255))
    screen.blit(intensity_text, (10, 10))
    
    pg.display.flip()
    clock.tick(60)  # Cap the frame rate at 60 FPS

pg.quit()