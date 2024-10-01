from typing import Self

from .Enums import Real
from .Vector import Vector

#  Classe pour la Position
class Position:
    # Initialisation de la classe Position
    def __init__(self, x: int = 0, y: int = 0) -> None:
        # Les valeurs x et y sur l'écran
        self.x: int = x
        self.y: int = y
        return
    
    # Métaméthode pour l'égalité de Position
    def __eq__(self, value: Self) -> bool:
        return self.x == value.x and self.y == value.y
    
    def __add__(self, value: Vector) -> Self:
        self.x += value.x * value.size
        self.y += value.y * value.size
        return self
    
    def __sub__(self, value: Vector) -> Self:
        self.x -= value.x * value.size
        self.y -= value.y * value.size
        return self

    def __call__(self) -> tuple[int, int]:
        return (self.x, self.y)

    # Récupérer la distance d'une autre position avec Pythagore.
    def getDistance(self, position: Self) -> Real:
        return ((position.x - self.x) ** 2 + (position.y - self.y) ** 2) ** (1/2) 
