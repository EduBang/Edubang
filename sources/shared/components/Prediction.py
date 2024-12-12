from copy import deepcopy
from math import pi

from proto import proto
import pygame as pg

from ..utils.utils import spacePosToScreenPos, mergeEnergy, mergeColor
from .Vectors import Vectors
from .Physics import Physics
from .Captors import Captors
from .Corps import Corps

with proto("Prediction") as Prediction:

    @Prediction
    def predict(self, game, n: int = 0, k: int = 100) -> None:
        space = [{"pos": i.pos, "velocity": i.velocity, "mass": i.mass, "corps": i} for i in deepcopy(game.space)]

        dt = 5e-2 * (1 if game.timeScale > 0 else 0 if game.timeScale == 0 else -1)

        poses: dict = {}
        futureCollided: list = []

        for i in space:
            poses[i["corps"]] = []

        for i in range(n):
            cache = []
            for a in space:
                if a["corps"] in futureCollided: continue
                velocity = a["velocity"]
                pos = a["pos"]
                mass = a["mass"]
                x, y = pos
                for b in space:
                    if b["corps"] in futureCollided: continue
                    if a == b: continue
                    
                    distance: float = Vectors.get_distance(pos, b["pos"])
                    attraction: float = Physics.get_attraction(mass, b["mass"], distance)
                    unitVector: tuple[float, float] = Vectors.get_unit_vector(pos, b["pos"])

                    accA: tuple[float, float] = (unitVector[0] * attraction / mass, unitVector[1] * attraction / mass)

                    velocity[0] += accA[0] * dt * k
                    velocity[1] += accA[1] * dt * k
                    
                    x += velocity[0] * dt * k
                    y += velocity[1] * dt * k

                startX, startY = spacePosToScreenPos(pos)
                endX, endY = spacePosToScreenPos((x, y))

                poses[a["corps"]].append((x, y))

                pg.draw.line(game.screen, (155, 155, 155), (startX, startY), (endX, endY), 2)

                a["pos"] = (x, y)

            for i in poses:
                if i in futureCollided: continue
                data: dict = poses[i]
                lastPosI: tuple[float, float] = data[-1]
                for j in poses:
                    if j in futureCollided: continue
                    if i == j: continue
                    lastPosJ: tuple[float, float] = poses[j][-1]
                    d = Vectors.get_distance(lastPosI, lastPosJ)
                    if Captors.collide(i, j, d):
                        x, y = lastPosI if i.mass > j.mass else lastPosJ
                        radius = (((pi * i.radius ** 2) + (pi * j.radius ** 2)) / pi) ** .5
                        color = mergeColor(i, j)
                        pg.draw.circle(game.screen, (255, 255, 255), spacePosToScreenPos((x, y)), radius, 1)
                        futureCollided.append(i)
                        futureCollided.append(j)
                        c = Corps(i.mass + j.mass, radius, (x, y), color, *mergeEnergy((i.mass, i.pos, lastPosI), (j.mass, j.pos, lastPosJ)))
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
