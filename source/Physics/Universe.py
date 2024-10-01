from pygame import Surface

# Classe Universe
class Universe:
    def __init__(self, surface: Surface) -> None:
        self.corpses: list = []
        self.surface: Surface = surface
        return
    
    # Ajouter un corps
    def addCorpse(self, corps) -> None:
        self.corpses.append(corps)
        return
    
    # Mettre à jour l'univers
    def update(self) -> None:
        for corpse in self.corpses:
            for target in self.corpses:
                if target == corpse:
                    continue
                corpse.attract(target)

    # Dessiner l'univers
    def draw(self):
        for corpse in self.corpses:
            corpse.draw(self.surface)