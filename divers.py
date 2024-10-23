import os

def reporterErreur(T):
    print("Erreur, voici les paramètres :")
    for e in T:
        print(e)
    raise Exception

def cheminAbsolu(*args):
    """Prend un chemin relatif par rapport à ce fichier,
    et renvoie le chemin absolu correspondant. Par exemple,
    si l'on veut C:/Users/johndoe/Dustopia/images/toto.png,
    alors on fait cheminAbsolu("images", "toto.png")
    Cette fonction est censé marcher pour Windows et Linux,
    qui utilisent des caractères différents pour les chemins"""
    chemin = os.path.dirname(__file__)
    for arg in args:
        chemin = os.path.join(chemin, arg)
        #Pour chaque argument, on met le bon séparateur de chemin
    
    return chemin

def getCoinHautGauche(surface, pointCentral):
    """Renvoie le coin en haut à gauche d'une
    surface sachant un point central. Utile
    pour les textes."""
    return (pointCentral[0] - surface.get_width()/2, pointCentral[1] - surface.get_height()/2)

def mettreMouvementsParDefaut(etatDuJeu):
    etatDuJeu["forceSaut"] = 0.45
    etatDuJeu["forceGravite"] = 0.02
    etatDuJeu["tauxConservationVitesse"] = 0.8
    etatDuJeu["accelerationX"] = 0.03