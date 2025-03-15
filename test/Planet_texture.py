# Projet : EduBang
# Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

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
        return round(degrees(atan2(unit_vector_y, - unit_vector_x)))
    
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
        new_rect = rotated_image.get_rect(center = center)
        return rotated_image, new_rect


def pil_to_pygame(image):
    """Convertir une image PIL en surface Pygame."""
    mode = image.mode
    size = image.size
    data = image.tobytes()
    return pg.image.fromstring(data, size, mode)

def generate_texture(intensity, stretch_x, stretch_y):
    global perlin_instance 
    perlin_instance = Perlin(surface_size=radius * 2, center_pos=planet_pos, intensity=intensity, stretching=(stretch_x, stretch_y), zoom=1)
    global image_pg
    image_pg = perlin_instance.generate_img(perlin_instance.fm)
    return image_pg


def displayRotatedImage(surf: pg.Surface, image: pg.image, pos: tuple[int, int], angle: float):
    w, h = image.get_size()
    originPos = (w / 2, h / 2)
    imageRect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offsetCenterToPivot = pg.math.Vector2(pos) - imageRect.center
    
    rotatedOffset = offsetCenterToPivot.rotate(angle)

    rotatedImageCenter = (pos[0] - rotatedOffset.x, pos[1] - rotatedOffset.y)

    rotatedImage = pg.transform.rotate(image, angle)
    rotatedImageRect = rotatedImage.get_rect(center = rotatedImageCenter)

    surf.blit(rotatedImage, rotatedImageRect)
    return

# def get_pixels():



pg.init()
screen = pg.display.set_mode((1000, 1000))  # Initialiser la fenêtre d'affichage
pg.display.set_caption("Test Rendering Planets")
clock = pg.time.Clock()
pg.font.init()
font = pg.font.SysFont('Arial', 30)

image_shadow_planet = pg.image.load("data/images/planet_shadow.png")

planet_pos = (500, 500)  # Position du centre de la planète
radius = 300  # Rayon de la planète
running = True
intensity = 255

l_light = [(1000, 1000)]
size_image_shadow_planet = pg.transform.scale(image_shadow_planet, (radius * 2 + 10, radius * 2 + 10))

l_angles = []

for light_pos in l_light:

    unit_vector_light = Vectors.get_unit_vector(planet_pos, light_pos)
    angle = Angles.generate_angle_whith_unit_vector(unit_vector_light[0], unit_vector_light[1])
    size_image_shadow_planet = pg.transform.scale(image_shadow_planet, (radius * 2, radius * 2))
    l_angles.append(angle)

stretch_x = 300
stretch_y = 300
planet_surface = generate_texture(intensity, stretch_x, stretch_y)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                planet_surface = generate_texture(intensity, stretch_x, stretch_y)
            if event.key == pg.K_t:
                stretch_x += 10
                planet_surface = generate_texture(intensity, stretch_x, stretch_y)
            if event.key == pg.K_g:
                stretch_x -= 10
                planet_surface = generate_texture(intensity, stretch_x, stretch_y)
            if event.key == pg.K_y:
                stretch_y += 10
                planet_surface = generate_texture(intensity, stretch_x, stretch_y)
            if event.key == pg.K_h:
                stretch_y -= 10
                planet_surface = generate_texture(intensity, stretch_x, stretch_y)
            if event.key == pg.K_s:

                pg.image.save(image_pg, "Soleil_preset.png")

                with open("soleil.txt", "w") as file:
                    file.write("Stretching X: " + str(stretch_x) + "\n")
                    file.write("Stretching Y: " + str(stretch_y) + "\n\n")
                    file.write("Ladder:\n")
                    for item in perlin_instance.ladder:
                        file.write(str(item) + "\n")
                    file.write("\nFinal Matrix (fm):\n")
                    for row in perlin_instance.fm:
                        file.write(" ".join(map(str, row)) + "\n")
                


    screen.fill((0, 0, 0))
    # Afficher la planète :
    screen.blit(planet_surface, (planet_pos[0] - radius, planet_pos[1] - radius))

    # for angle in l_angles:
    #     displayRotatedImage(screen, size_image_shadow_planet, planet_pos, angle)


    for light_pos in l_light:
        pg.draw.circle(screen, (255, 0, 0), (light_pos), 100)

    # Dessiner le texte avec la valeur de l'intensité
    intensity_text = font.render(f'Intensité: {intensity}', True, (255, 255, 255))
    screen.blit(intensity_text, (10, 10))
    
    pg.display.flip()
    clock.tick(60)  # Cap the frame rate at 60 FPS

pg.quit()