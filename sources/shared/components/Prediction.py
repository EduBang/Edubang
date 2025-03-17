# Projet : EduBang
# Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

from math import pi, sqrt

import pygame as pg

from ..utils.utils import spacePosToScreenPos, mergeEnergy
from .Vectors import Vectors
from .Physics import Physics
from .Captors import isColliding
from .Corps import Corps

def predict(game, n: int = 0, k: int = 100) -> None:
    """
    Prédit les trajectoire des astres

    Arguments:
        game (Game): Le prototype de Game
        n (int): Le nombre d'itération
        k (int): le pas de temps

    Retourne:
        None
    """
    if game.timeScale == 0: return

    space: list = [{"pos": tuple(i.pos), "velocity": list(i.velocity), "mass": float(i.mass), "corps": i} for i in game.space]

    k *= (5e-2 if game.timeScale > 0 else -5e-2)

    poses: dict = {item["corps"]: [] for item in space}
    futureCollided: list = []

    for i in range(n):
        cache = []
        for a in space:
            if a["corps"] in futureCollided: continue
            velocity = a["velocity"]
            x, y = pos = a["pos"]
            mass = a["mass"]

            # x += velocity[0] / k
            # y += velocity[1] / k

            for b in space:
                if b["corps"] in futureCollided or a == b: continue

                distance: float = Vectors.get_distance(pos, b["pos"])
                attraction: float = Physics.get_attraction(mass, b["mass"], distance, velocity, b["velocity"]) 
                unitVector: tuple[float, float] = Vectors.get_unit_vector(pos, b["pos"])
                acc: tuple[float, float] = (unitVector[0] * attraction / mass, unitVector[1] * attraction / mass)

                velocity[0] += acc[0] * k
                velocity[1] += acc[1] * k
                    
                x += velocity[0] * k
                y += velocity[1] * k

            poses[a["corps"]].append((x, y))

            startPos = spacePosToScreenPos(pos)
            endPos = spacePosToScreenPos((x, y))
            if -1e2 < startPos[0] < 1e4 and -1e2 < startPos[1] < 1e4 and -1e2 < endPos[0] < 1e4 and -1e2 < endPos[1] < 1e4:
                pg.draw.line(game.screen, (155, 155, 155), startPos, endPos, 2)

            a["pos"] = (x, y)

        for i in poses:
            if i in futureCollided: continue
            lastPosI: tuple[float, float] = poses[i][-1]
            for j in poses:
                if j in futureCollided or i == j: continue
                lastPosJ: tuple[float, float] = poses[j][-1]
                d: float = Vectors.get_distance(lastPosI, lastPosJ)
                if isColliding(i, j, d):
                    x, y = lastPosI if i.mass > j.mass else lastPosJ
                    radius: float = sqrt(((pi * i.radius ** 2) + (pi * j.radius ** 2)) / pi)
                    pg.draw.circle(game.screen, (255, 255, 255), spacePosToScreenPos((x, y)), radius * game.Camera.zoom, 1)
                    futureCollided.append(i)
                    futureCollided.append(j)
                    c = Corps(i.mass + j.mass, radius, (x, y), (0, 0, 0), mergeEnergy((i.mass, i.pos, lastPosI), (j.mass, j.pos, lastPosJ)))
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
