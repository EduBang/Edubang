from proto import proto
from math import *

with proto("Physics") as Physics:
    @Physics
    def get_attraction(mass1, mass2, d):
        G = 6.67 * 10 ** -11
        if d == 0:
            return 0
        return G * (mass1 * mass2) / (d ** 2)


    def get_distance(corps1, corps2):
        return sqrt(((corps1.pos[0] - corps2.pos[0]) ** 2) + ((corps1.pos[1] - corps2.pos[1]) ** 2))
    
    def get_cinetic_energy(mass, velocity):
        cinetic_energy = 0.5 * mass * velocity ** 2
        return cinetic_energy
        
        