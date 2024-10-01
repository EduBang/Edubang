from .Enums import Real

# Classe pour la champ gravitationnel
class Gravitation:
    def __init__(self, space: int = 0) -> None:
        self.space: int = space
        self.spaces: dict = {}
        x = 0
        for i in range(-10, 0):
            self.spaces[(x, x + self.space)] = (-i * 10)
            x += self.space
        return

    def __str__(self) -> None:
        return str(self.spaces)

    def __eq__(self, value: object) -> bool:
        return self.space == value.space

    # Récupérer le "taux" de la forme selon une distance
    def getAt(self, distance: Real) -> int:
        for i in self.spaces.keys():
            if i[0] < distance < i[1]:
                return self.spaces[(i[0], i[1])]
        return 0
