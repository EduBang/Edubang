from math import exp, sqrt

from proto import proto

G: float = 6.6743e-11
c: int = 299_792_458 # m/s
UA: float = 149_597_870.7 # km, Selon l'Union Astronomique Internationale en 2012

type Velocity = tuple[float, float]

with proto("Physics") as Physics:
    @Physics
    def getRelativeVelocity(self, v1: Velocity, v2: Velocity) -> float:
        v1: float = sqrt(v1[0] ** 2 + v1[1] ** 2)
        v2: float = sqrt(v2[0] ** 2 + v2[1] ** 2)
        return sqrt(v1 ** 2 + v2 ** 2)

    @Physics
    def get_attraction(self, mass1, mass2, d, v1, v2, cutDistance: float | int = 120 * UA) -> float:
        if 0 < d < cutDistance:
            attenuation: float = exp(-d / cutDistance)
            relative: float = (1 + (self.getRelativeVelocity(v1, v2) ** 2) / (c ** 2))
            force: float = G * (mass1 * mass2) / (d ** 2)
            return force * relative * attenuation
        return .0
    
    @Physics
    def get_velocity(self, pos_init, pos_final, dt) -> float | int:
        velocity: float | int = 0
        if dt != 0:
            velocity_vector = (pos_final[0] - pos_init[0], pos_final[1] - pos_init[1])
            norm_velocity_vector = sqrt(velocity_vector[0] ** 2 + velocity_vector[1] ** 2)
            velocity = norm_velocity_vector / dt
        return velocity
        
    
    @Physics
    def get_cinetic_energy(self, mass, velocity) -> float:
        return 0.5 * mass * velocity ** 2 
