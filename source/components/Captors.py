from proto import proto
from math import *
# si la distance est >= somme rayon --> collision

with proto("Captors") as Captors:
    
    @Captors
    def collide(self, corps1, corps2, distance):
        return 2 * distance <= corps1.radius + corps2.radius
    
    
    