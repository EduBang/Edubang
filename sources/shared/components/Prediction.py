from copy import deepcopy

from proto import proto
import pygame as pg

from ..utils.utils import spacePosToScreenPos, screenPosToSpacePos
from .Vectors import Vectors
from .Physics import Physics

with proto("Prediction") as Prediction:

    @Prediction
    def predict(self, game, n: int = 0, k: int = 100) -> None:
        space = [{"pos": i.pos, "velocity": i.velocity, "mass": i.mass} for i in deepcopy(game.space)]

        dt = 5e-2

        for i in range(n):
            for a in space:
                velocity = a["velocity"]
                pos = a["pos"]
                mass = a["mass"]
                x, y = pos
                for b in space:
                    if a == b: continue
                    
                    distance = Vectors.get_distance(pos, b["pos"]) # km
                    attraction = Physics.get_attraction(mass, b["mass"], distance) # N
                    unitVector = Vectors.get_unit_vector(pos, b["pos"])
                    accA = (unitVector[0] * attraction / mass, unitVector[1] * attraction / mass)

                    velocity[0] += accA[0] * dt * k
                    velocity[1] += accA[1] * dt * k
                    
                    x += velocity[0] * dt * k
                    y += velocity[1] * dt * k

                startX, startY = spacePosToScreenPos(pos)
                endX, endY = spacePosToScreenPos((x, y))
                pg.draw.line(game.screen, (155, 155, 155), (startX, startY), (endX, endY), 2)

                a["pos"] = (x, y)

        return
