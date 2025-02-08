# Projet : EduBang
# Auteurs : Anaël Chevillard, Sacha Fréguin, Néji Lim

from math import exp, sqrt

from proto import proto

G: float = 6.6743e-11
c: int = 299_792_458 # m/s
UA: float = 149_597_870.7 # km, Selon l'Union Astronomique Internationale en 2012

with proto("Physics") as Physics:
    @Physics
    def getRelativeVelocity(self, v1: tuple[float, float], v2: tuple[float, float]) -> float:
        """
        Fonction qui récupère la vélocité relative entre deux vélocités
        
        Arguments:
            v1 (tuple[float, float]): Première vélocité
            v2 (tuple[float, float]): Deuxième vélocité
            
        Rertourne:
            float: La vélocité relative
        """
        v1: float = sqrt(v1[0] ** 2 + v1[1] ** 2)
        v2: float = sqrt(v2[0] ** 2 + v2[1] ** 2)
        return sqrt(v1 ** 2 + v2 ** 2)

    @Physics
    def get_attraction(self, mass1: float, mass2: float, d: float, v1: tuple[float, float], v2: tuple[float, float], cutDistance: float | int = 120 * UA) -> float:
        """
        Fonction qui détermine la norme de l'attraction entre 2 astres
        
        Arguments:
            mass1 (float): La première masse
            mass2 (float): La deuxième masse
            d (float): La distance qui sépare les astres
            v1 (tuple[float, float]): La vélocité du premier astre
            v2 (tuple[float, float]): La vélocité du second astre
            cutDistance (float): Distance limite qui détermine la distance de "coupe", c'est-à-dire qu'au delà de cette distance, la norme n'est plus calculée
        
        Retourne:
            float: La norme de l'attraction
        """
        if 0 < d < cutDistance:
            attenuation: float = exp(-d / cutDistance)
            relative: float = (1 + (self.getRelativeVelocity(v1, v2) ** 2) / (c ** 2))
            force: float = G * (mass1 * mass2) / (d ** 2)
            return force * relative * attenuation
        return .0
    
    @Physics
    def get_velocity(self, pos_init: tuple[float, float], pos_final: tuple[float, float], dt: float) -> float | int:
        """
        Fonction qui récupère la vélocité à partir de deux position selon une différence de temps
        
        Arguments:
            pos_init (tuple[float, float]): La première position
            pos_final (tuple[float, float]): La deuxième position
            dt (float): La différence de temps
            
        Retourne:
            float: La vélocité calculée
        """
        velocity: float | int = 0
        if dt != 0:
            #print("test")
            #print(pos_final, pos_init)
            velocity_vector = (pos_final[0] - pos_init[0], pos_final[1] - pos_init[1])
            norm_velocity_vector = sqrt(velocity_vector[0] ** 2 + velocity_vector[1] ** 2)
            velocity = norm_velocity_vector / dt
            #print(f"velo : {velocity}")
        return velocity
        
    
    @Physics
    def get_cinetic_energy(self, mass: float, velocity: float) -> float:
        """
        Fonction qui calcule l'énergie cinétique
        
        Arguments:
            mass (float): La masse
            velocity (float): La vélocité
        
        Retourne:
            float: L'énergie cinétique en N
        """
        return 0.5 * mass * velocity ** 2 
