from pygame import Surface, draw

from .Gravitation import Gravitation
from .Position import Position
from .Vector import Vector
from .Enums import Color

class Corpse:
    def __init__(self, mass: int = 0, position: tuple[int, int] = (0, 0), radius: int = 0, orientation: int = 0) -> None:
        self.mass: int = mass
        self.position: Position = Position(position[0], position[1])
        self.radius: int = radius
        self.gravitation: Gravitation = Gravitation(self.mass * 10000 / self.radius ** 2)
        self.orientation: int = orientation
        self.image: Surface = None
        self.color: Color = (255, 255, 255)
        self.forces: Vector = Vector(0, 0, 0)
        return
    
    def __eq__(self, value: object) -> bool:
        return self.mass == value.mass and self.position == value.position and self.radius == value.radius and self.gravitation == value.gravitation and self.orientation == value.orientation
    
    def getDistance(self, corpse: object) -> float | int:
        return self.position.getDistance(corpse.position)
    
    def attract(self, object: object) -> None:
        d: float | int = self.getDistance(object)
        t: tuple[int, int] = self.gravitation.getAt(d)
        x = object.position.x - self.position.x
        y = object.position.y - self.position.y
        if x != 0 or y != 0:
            object.position -= Vector(x, y, t)
        return
    
    def update(self) -> None:
        self.position += self.forces
        return
    
    def draw(self, surface: Surface) -> None:
        if self.image:
            draw.circle(self.image, self.color, self.position(), self.radius)
        else:
            draw.circle(surface, self.color, self.position(), self.radius)
        return
    
    def addForce(self, force: Vector) -> None:
        self.forces += force
        return