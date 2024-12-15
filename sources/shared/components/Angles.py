from proto import proto
from math import cos, sin, radians, pi

with proto("Angles") as Angles:
    @Angles
    def generate_unit_vector_angle(angle): # fonction qui retourne un vecteur unitaire correspondant à un angle donné en degrés. (une orientation) 90° --> vecteur 0,1
        return cos(radians(angle)), sin(radians(angle))
