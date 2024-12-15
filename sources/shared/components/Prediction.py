from copy import deepcopy
from math import pi

from proto import proto
import pygame as pg

from ..utils.utils import spacePosToScreenPos, mergeEnergy
from .Vectors import Vectors
from .Physics import Physics
from .Captors import Captors
from .Corps import Corps

with proto("Prediction") as Prediction:

    @Prediction
    def predict(self, game, n: int = 0, k: int = 100) -> None:
        if game.timeScale == 0: return

        space = [{"pos": tuple(i.pos), "velocity": list(i.velocity), "mass": int(i.mass), "corps": i} for i in game.space]

        k *= (5e-2 if game.timeScale > 0 else -5e-2)

        poses: dict = {}
        futureCollided: list = []

        for i in space:
            poses[i["corps"]] = []

        for i in range(n):
            cache = []
            for a in space:
                if a["corps"] in futureCollided: continue
                velocity = a["velocity"]
                x, y = pos = a["pos"]
                mass = a["mass"]
                for b in space:
                    if b["corps"] in futureCollided or a == b: continue
 
                    distance: float = Vectors.get_distance(pos, b["pos"])
                    attraction: float = Physics.get_attraction(mass, b["mass"], distance)
                    unitVector: tuple[float, float] = Vectors.get_unit_vector(pos, b["pos"])
                    acc: tuple[float, float] = (unitVector[0] * attraction / mass, unitVector[1] * attraction / mass)

                    velocity[0] += acc[0] * k
                    velocity[1] += acc[1] * k
                    
                    x += velocity[0] * k
                    y += velocity[1] * k

                poses[a["corps"]].append((x, y))

                pg.draw.line(game.screen, (155, 155, 155), spacePosToScreenPos(pos), spacePosToScreenPos((x, y)), 2)

                a["pos"] = (x, y)

            for i in poses:
                if i in futureCollided: continue
                lastPosI: tuple[float, float] = poses[i][-1]
                for j in poses:
                    if j in futureCollided or i == j: continue
                    lastPosJ: tuple[float, float] = poses[j][-1]
                    d: float = Vectors.get_distance(lastPosI, lastPosJ)
                    if Captors.collide(i, j, d):
                        x, y = lastPosI if i.mass > j.mass else lastPosJ
                        radius: float = (((pi * i.radius ** 2) + (pi * j.radius ** 2)) / pi) ** .5
                        pg.draw.circle(game.screen, (255, 255, 255), spacePosToScreenPos((x, y)), radius, 1)
                        futureCollided.append(i)
                        futureCollided.append(j)
                        c = Corps(i.mass + j.mass, radius, (x, y), (0, 0, 0), *mergeEnergy((i.mass, i.pos, lastPosI), (j.mass, j.pos, lastPosJ)))
                        space.append(
                            {
                            "pos": c.pos,
                            "velocity": c.velocity,
                            "mass": c.mass,
                            "corps": c
                            }
                        )
                        cache.append(c)

            for c in cache:
                poses[c] = []

        return
