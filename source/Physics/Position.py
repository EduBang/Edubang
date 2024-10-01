from .Enums import Real

#  Classe pour la Position
class Position:
    # Initialisation de la classe Position
    def __init__(self, x: int = 0, y: int = 0) -> None:
        # Les valeurs x et y sur l'écran
        self.x: int = x
        self.y: int = y
        return
    
    # Métaméthode pour l'égalité de Position
    def __eq__(self, value: object) -> bool:
        return self.x == value.x and self.y == value.y

    def __call__(self) -> tuple[int, int]:
        return (self.x, self.y)

    # Récupérer la distance d'une autre position avec Pythagore.
    def getDistance(self, position: object) -> Real:
        return ((position.x - self.x) ** 2 + (position.y - self.y) ** 2) ** (1/2) 
