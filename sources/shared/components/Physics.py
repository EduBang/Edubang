from math import sqrt
from proto import proto

gravitation_constant = 6.67e-11

with proto("Physics") as Physics:
    @Physics
    def get_attraction(self, mass1, mass2, d):
        G = 6.67 * 10 ** -11
        if d == 0:
            return 0
        return G * (mass1 * mass2) / (d ** 2)
    
    @Physics
    def get_velocity(self, pos_init, pos_final, dt):
        velocity_vector = (pos_final[0] - pos_init[0], pos_final[1] - pos_init[1])
        norm_velocity_vector = sqrt(velocity_vector[0] ** 2 + velocity_vector[1] ** 2)
        if dt != 0:
            velocity = norm_velocity_vector / dt
        else:
            velocity = 0
        return velocity
        
    
    @Physics
    def get_cinetic_energy(self, mass, velocity):
        cinetic_energy = 0.5 * mass * velocity ** 2 
        return cinetic_energy
    

 
        