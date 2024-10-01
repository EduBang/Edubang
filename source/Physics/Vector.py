from .Enums import Real

# Classe pour le Vecteur
class Vector:
    # Initialisation de la classe Vector
    def __init__(self, x: Real = 0, y: Real = 0, size: Real = 0) -> None:
        self.x: Real = x
        self.y: Real = y
        self.size: Real = size
        return
    
    # Métaméthode pour l'égalité de Vecteur
    def __eq__(self, value: object) -> bool:
        return self.x == value.x and self.y == value.y

