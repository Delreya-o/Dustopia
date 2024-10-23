from divers import *

import math

class Vecteur:
    """Représente un vecteur ou un point (les deux sont équivalents)"""
    
    def __init__(self, x=None, y=None, nom=""):
        self.x = x
        self.y = y
        self.nom = nom
    
    def __str__(self):
        return f"Vecteur({self.x}, {self.y})"
    
    def getAdd(self, vecteur):#Renvoie le vecteur représentant l'addition entre self et vecteur
        return Vecteur(self.x + vecteur.x, self.y + vecteur.y)
    
    def coeff(self, coeff):
        return Vecteur(self.x * coeff, self.y * coeff)
    
    def add(self, vecteur):#Ajouter vecteur à self
        self.x += vecteur.x
        self.y += vecteur.y
    
    def distance(self, point):
        return math.sqrt((self.x-point.x)**2 + (self.y-point.y)**2)
    
    def pointLePlusProche(self, T):
        """Renvoie le point le plus proche"""
        if T==[]:
            reporterErreur([T])
        
        distanceMin = None
        for point in T:
            dist = self.distance(point)
            if distanceMin==None or distanceMin > dist:
                distanceMin = dist
                pointPlusProche = point
        
        return pointPlusProche
    
    def heurtera(self, etatDuJeu, vitesse):
        """Renvoie si le point heurtera un bloc si il avance selon vitesse"""
        niveau = etatDuJeu["niveau"]
        
        if not(0<= self.x + vitesse.x <niveau.width and 0 <= self.y + vitesse.y < niveau.height):
            return False
        
        return niveau.getBlocParVecteur(self.getAdd(vitesse)) not in [0, 3, 5, 6, 7, 8]#Ce n'est ni du sol, ni des briques de fond, ni une pancarte