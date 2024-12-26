from .Physics import c

type Real = float | int

def lorentzFactor(v: Real) -> float:
    """
    Calcule de facteur de Lorentz

    Arguments:
        v (Real): La vitesse de l'objet
    
    Retourne:
        float: Le facteur de Lorentz
    """
    return 1 / (1 - (v ** 2 / c ** 2)) ** .5

def momentum(m: Real, v: Real) -> float:
    """
    Calcule le moment relativiste

    Arguments:
        m (Real): La masse de l'objet
        v (Real): La vitesse de l'objet
    
    Retourne:
        float: Le moment relativiste
    """
    gamma: float = lorentzFactor(v)
    return gamma * m * v

def totalEnergy(m: Real, v: Real) -> float:
    """
    Calcule l'énergie totale de l'objet
    
    Arguments:
        m (Real): La masse de l'objet
        v (Real): La vitesse de l'objet
    
    Retourne:
        float: L'énergie totale de l'objet
    """
    gamma: float = lorentzFactor(v)
    return gamma * m * c ** 2

def kineticEnergy(m: Real, v:Real) -> float:
    """
    Calcule l'énérgie cinétique de l'objet

    Arguments:
        m (Real): La masse de l'objet
        v (Real): La vitesse de l'objet
    
    Retourne:
        float: L'énergie cinétique de l'objet
    """
    gamma: float = lorentzFactor(v)
    return (gamma - 1) * m * c ** 2