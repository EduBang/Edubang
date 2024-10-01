from typing import Self

from .Enums import Real

# Classe pour le Vecteur
class Vector:
    # Initialisation de la classe Vector
    def __init__(self, x: Real = 0, y: Real = 0, size: Real = 0) -> None:
        self.x: Real = 0 if x == 0 else x / abs(x)
        self.y: Real = 0 if x == 0 else y / abs(x)
        self.size: Real = size
        return
    
    def __add__(self, value: Self) -> Self:
        self.x += value.x
        self.y += value.y
        self.size += value.size
        return self
    
    # Métaméthode pour l'égalité de Vecteur (v1 == v2)
    def __eq__(self, value: Self) -> bool:
        return self.x == value.x and self.y == value.y and self.size == value.size
