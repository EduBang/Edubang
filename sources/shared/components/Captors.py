def isColliding(corps1, corps2, distance: float | int) -> bool:
    return 2 * distance <= corps1.radius + corps2.radius
