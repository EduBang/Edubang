from proto import proto
import pygame as pg

from main import Game
from .Physics import Physics
from .Vectors import Vectors

with proto("Prediction") as Prediction:
    @Prediction
    def new(self, space) -> None:
        self.space = space
        return

    @Prediction
    def predict(self, n: int = 0) -> None:
        # n est le nombre l'itération à la prédiction
        for i in range(n):
            for a in self.space:
                for b in self.space:
                    if a == b: continue
                    
                    velocity = [*a.velocity]
                    pos = [*a.pos]

                    distance = Vectors.get_distance(a, b) # pixel
                    attraction = Physics.get_attraction(a.mass, b.mass, distance) # N
                    unitVectorA = Vectors.get_unit_vector(a.pos, b.pos)
                    accA = [unitVectorA[0] * attraction / a.mass, unitVectorA[1] * attraction / a.mass]

                    k = 1000

                    velocity[0] += accA[0] * Game.deltaTime * Game.timeScale * k
                    velocity[1] += accA[1] * Game.deltaTime * Game.timeScale * k
                    
                    x = pos[0] + velocity[0] * Game.deltaTime * Game.timeScale * k
                    y = pos[1] + velocity[1] * Game.deltaTime * Game.timeScale * k

                    pg.draw.circle(Game.screen, (255, 255, 255), (x, y), 500)
        return