from copy import deepcopy

from proto import proto
import pygame as pg

from main import Game
from .Physics import Physics
from .Vectors import Vectors

with proto("Prediction") as Prediction:

    @Prediction
    def predict(self, game, n: int = 0) -> None:
        # n est le nombre l'itération à la prédiction
        return
