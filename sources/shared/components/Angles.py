from proto import proto
from math import cos, sin, radians

with proto("Angles") as Angles:
    @Angles
    def generate_unit_vector_angle(angle: float):
        """
        Fonction qui trouve le vecteur unitaire selon l'angle donné en degrés
        
        Arguments:
            angle (float): Angle en degrés
            
        Retourne:
            tuple[float, float]: Le vecteur unitaire
        """
        return (cos(radians(angle)), sin(radians(angle)))
