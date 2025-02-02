# Projet : EduBang
# Auteurs : Anaël Chevillard, Sacha Fréguin, Néji Lim

from proto import proto
from math import cos, sin, radians, acos, degrees, atan2

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
    def generate_angle_whith_unit_vector(self, unit_vector_x: float, unit_vector_y: float = 0):
        """
        Fonction qui trouve l'angle en degrés selon un vecteur unitaire
        
        Arguments:
            unit_vector (tuple[float, float]): Vecteur unitaire
            
        Retourne:
            float: L'angle en degrés
        """
        return degrees(atan2(unit_vector_y, unit_vector_x))


for i in range(0, 600, 10):
    print(i, Angles.generate_angle_whith_unit_vector(Angles.generate_unit_vector_angle(i)[0]))