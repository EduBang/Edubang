#Projet : EduBang
#Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

def isColliding(corps1, corps2, distance: float | int) -> bool:
    """
    Fonction qui vérifie si un astre rentre en collision avec un autre
    
    Arguments:
        corps1 (Corps): Premier corps
        corps2 (Corps): Deuxième corps
        distance (float | int): La distance qui sépare ces corps
    
    Retourne:
        bool: La valeur qui vérifie la collision
    """
    return 2 * distance <= corps1.radius + corps2.radius
