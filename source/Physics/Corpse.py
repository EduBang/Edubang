from pygame import Surface, draw

from .Gravitation import Gravitation
from .Position import Position

class Corpse:
    def __init__(self, mass: int = 0, position: Position = Position(), radius: int = 0, gravitation: Gravitation = Gravitation(), orientation: int = 0) -> None:
        self.mass: int = mass
        self.position: Position = position
        self.radius: int = radius
        self.gravitation: Gravitation = gravitation
        self.orientation: int = orientation
        self.image: Surface = None
        return
    
    def __eq__(self, value: object) -> bool:
        return self.mass == value.mass and self.position == value.position and self.radius == value.radius and self.gravitation == value.gravitation and self.orientation == value.orientation
    
    def getDistance(self, corpse: object) -> float | int:
        return self.position.getDistance(corpse)
    
    def attract(self, object: object) -> None:
        d: float | int = self.getDistance(object.position)
        t: tuple[int, int] = self.gravitation.getAt(d)
        return
    
    def draw(self, surface: Surface, color: tuple[int, int, int] = (255, 255, 255)) -> None:
        if self.image:
            draw.circle(self.image, color, self.position(), self.radius)
        else:
            draw.circle(surface, color, self.position(), self.radius)
        return