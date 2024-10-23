from Niveau import *
from Vecteur import *

from dessiner import *
from divers import *

import math

class Box:
    """Les instances de cette classe sont des boîtes représentant des entités."""

    def __init__(self, pos, width, height, vitesse=None, alignementsPrecedents=[]):
        """Les dimensions doivent être données en coordonnées internes (un bloc = une unité)"""
        self.pos = pos
        self.width = width
        self.height = height
        self.vitesse = vitesse
        self.alignementsPrecedents = alignementsPrecedents
        
        
    
    def __str__(self):
        return f"Box({self.pos}, {self.width}, {self.height}, {self.vitesse}, {self.alignementsPrecedents})"
    
    def getCoin(self, i):
        """Renvoie le coin de la box (0 pour le coin en haut à gauche, puis continue dans le sens horaire)"""
        #On calcule le vecteur entre le centre et le coin, puis on renvoie l'addition entre ce vecteur et le centre
        if i==0:    vecteurCentreCoin = Vecteur(-self.width/2, -self.height/2)
        elif i==1:    vecteurCentreCoin = Vecteur(self.width/2, -self.height/2)
        elif i==2:    vecteurCentreCoin = Vecteur(self.width/2, self.height/2)
        elif i==3:    vecteurCentreCoin = Vecteur(-self.width/2, self.height/2)
        else:        assert False
        
        return self.pos.getAdd(vecteurCentreCoin)
    
    def getPosSiNonHeurt(self):
        """Renvoie le centre futur de la box si elle ne heurtait rien"""
        return self.pos.getAdd(self.vitesse)
    
    def getCoinSiNonHeurt(self, i):
        """Renvoie le coin i de la box si elle ne heurtait rien"""
        return self.getCoin(i).getAdd(self.vitesse)
    
    def coinHeurtera(self, i, etatDuJeu):
        """Renvoie si la position future du coin i heurte un bloc"""
        return self.getCoin(i).heurtera(etatDuJeu, self.vitesse)

    def getPosAlignee(self, nomFace):
        """Aligne le centre de la box selon la face qui touche un bloc.
        Si la face est déjà alignée, il faut que rien ne change."""
        posFuture = self.getPosSiNonHeurt()
        if nomFace=="Haut":
            j = math.ceil(self.getCoinSiNonHeurt(0).y)
            r = self.height/2
            
            return Vecteur(posFuture.x, j+r, nomFace)
        
        elif nomFace=="Bas":
            j = math.floor(self.getCoinSiNonHeurt(2).y)
            r = self.height/2
        
            return Vecteur(posFuture.x, j-r, nomFace)
        
        elif nomFace=="Gauche":
            i = math.ceil(self.getCoinSiNonHeurt(0).x)
            r = self.width/2
            
            return Vecteur(i+r, posFuture.y, nomFace)
        
        elif nomFace=="Droite":
            i = math.floor(self.getCoinSiNonHeurt(2).x)
            r = self.width/2
            
            return Vecteur(i-r, posFuture.y, nomFace)
        else:
            reporterErreur([nomFace])
    
    def faceHeurtera(self, nomFace, etatDuJeu):
        """Renvoie si la face nomFace heurtera un bloc, à l'aide d'une liste des alignements précédents pendant la même update.
        La liste des alignements précédents contient le nom des faces auxquelles on s'est aligné.
        
        Ici, lorsque l'on aligne la box selon une face, il se peut que la face par rapport à laquelle on a aligné reste dans
        le bloc, à cause des erreurs d'arrondis. J'ai refusé d'ajouter des epsilons, car ceux-ci rendront le programme moins
        précis. À la place, si la face a déjà été alignée, je renvoie False, peu importe si les points de la face heurteront
        un bloc. Aussi, si l'une des extrémités de la face appartient à une face déjà alignée, je ne prend pas en compte ce point.
        """
        #Si la face a déjà été alignée, on renvoie False
        if nomFace in self.alignementsPrecedents:
            return False
        
        #Sinon
        else:
            
            #Si l'un des points n'étant pas un coin heurtera, alors on renvoie True
            for point in self.getFaceSansLesCoins(nomFace[0]):#On n'a besoin que de la première lettre de la face
                if point.heurtera(etatDuJeu, self.vitesse):
                    return True
            
            #Si la face est celle du haut, alors on renvoie si l'une de ses deux extrémités heurte
            if nomFace=="Haut":
                extremite1Heurtera = "Gauche" not in self.alignementsPrecedents and self.getCoin(0).heurtera(etatDuJeu, self.vitesse)
                extremite2Heurtera = "Droite"  not in self.alignementsPrecedents and self.getCoin(1).heurtera(etatDuJeu, self.vitesse)
            elif nomFace=="Bas":
                extremite1Heurtera = "Gauche" not in self.alignementsPrecedents and self.getCoin(3).heurtera(etatDuJeu, self.vitesse)
                extremite2Heurtera = "Droite"  not in self.alignementsPrecedents and self.getCoin(2).heurtera(etatDuJeu, self.vitesse)
            elif nomFace=="Gauche":
                extremite1Heurtera = "Bas" not in self.alignementsPrecedents and  self.getCoin(3).heurtera(etatDuJeu, self.vitesse)
                extremite2Heurtera = "Haut" not in self.alignementsPrecedents and self.getCoin(0).heurtera(etatDuJeu, self.vitesse)
            elif nomFace=="Droite":
                extremite1Heurtera = "Bas" not in self.alignementsPrecedents and self.getCoin(2).heurtera(etatDuJeu, self.vitesse)
                extremite2Heurtera = "Haut" not in self.alignementsPrecedents and self.getCoin(1).heurtera(etatDuJeu, self.vitesse)
                
            else:
                reporterErreur([nomFace])
            
            return extremite1Heurtera or extremite2Heurtera
        
    def heurtera(self, etatDuJeu):
        return True in [self.faceHeurtera(nomFace, etatDuJeu) for nomFace in ["Haut", "Bas", "Gauche", "Droite"]]
    
    def estValide(self, etatDuJeu, point):
        heurtera = False
        vitesse = Vecteur(point.x - self.pos.x, point.y - self.pos.y)
        for i in range(5):
            box = Box(point, self.width, self.height, vitesse.coeff(i/4), self.alignementsPrecedents + [point.nom])
            heurtera = heurtera or box.heurtera(etatDuJeu)
        return not heurtera

    def updatePos(self, etatDuJeu):
        """Met à jour la position précédente"""
        self.vitesse.y = min(0.3, self.vitesse.y + etatDuJeu["forceGravite"])
        
        """On doit prendre en compte les alignements que l'on fait pendant cette update, mais aussi les alignements du tick précédent, mais seulement dans le cas où l'alignement est toujours valide, donc quand on n'a pas bougé, donc quand la
        vitesse est nulle. Même si la vitesse verticale ici ne peut pas être nulle à cause de la gravité, je la teste quand même au cas où on voudrait créer des niveaux sans gravité."""
        tmp = []
        if self.vitesse.y == 0:
            if "Haut" in self.alignementsPrecedents:
                tmp.append("Haut")
            if "Bas" in self.alignementsPrecedents:
                tmp.append("Bas")
        if self.vitesse.x == 0:
            if "Gauche" in self.alignementsPrecedents:
                tmp.append("Gauche")
            if "Droite" in self.alignementsPrecedents:
                tmp.append("Droite")
        self.alignementsPrecedents = tmp
        
        if self.heurtera(etatDuJeu):
            for i in range(4):
                
                pointsATester = []
                #pointsATester contient les alignements possibles
                
                for nomFace in [e for e in ["Haut", "Bas", "Gauche", "Droite"] if e not in self.alignementsPrecedents]:
                    if self.faceHeurtera(nomFace, etatDuJeu):
                        pointsATester.append(self.getPosAlignee(nomFace))
                
                #pointsValides = [point for point in pointsATester if self.estValide(etatDuJeu, point)]
                pointsValides = [point for point in pointsATester if self.estValide(etatDuJeu, point) and self.pos.distance(point)<0.5]
                
                if pointsATester!=[]:
                    pointLePlusProche = self.pos.pointLePlusProche(pointsValides if len(pointsValides) != 0 else pointsATester)
                    self.alignementsPrecedents.append(pointLePlusProche.nom)
                    self.vitesse = Vecteur(pointLePlusProche.x - self.pos.x, pointLePlusProche.y - self.pos.y)
        
        self.pos.add(self.vitesse)
        
    def getFaceSansLesCoins(self, nomFace):
        """Crée des points entre les coins. Ces points sont donc sur les faces de la box. Sur les faces horizontales,
        il y aura int(width) points entre les coins, tandis que sur les faces verticales, il y aura int(height)
        points entre les deux coins.
        
        Cette fonction est appelée vraiment, vraiment, vraiment énormément de fois.
        Donc au lieu de comparer les chaînes de caractères entières, je ne compare que le premier caractère
        Haut Bas Gauche Droite -> H B G D
        Et je fais le moins de divisions que possible
        """
        nomFace = nomFace[0]
        
        nPoints = math.floor(self.width)
        division = self.width/(nPoints+1)
        
        if nomFace=="H" or nomFace=="B":
            coin = self.getCoin(0 if nomFace=="H" else 3)
            face = [Vecteur(coin.x + (i+1)*division, coin.y) for i in range(nPoints)]
        else:
            coin = self.getCoin(3 if nomFace=="G" else 2)
            face = [Vecteur(coin.x, coin.y - (i+1)*division) for i in range(nPoints)]
            #Ces points sont de bas en haut
        
        return face
    
    def heurteAutreBox(self, autreBox):
        """Appelons A la box actuelle (self) et B l'autre box.
        
        On cherche si un coin de A est dans B, ou si un coin de
        B est dans A.
        
        Pour qu'un coin de A soit dans B, il faut que l'abscisse
        et l'ordonnée correspondent.
        
        L'abscisse correspond quand la partie gauche de A est entre
        la partie gauche et droite de B, ou que la partie droite de
        A est entre la partie gauche et droite de B."""
        
        hautA   = self.getCoin(0).y
        basA    = self.getCoin(2).y
        gaucheA = self.getCoin(0).x
        droiteA = self.getCoin(2).x
        
        hautB   = autreBox.getCoin(0).y
        basB    = autreBox.getCoin(2).y
        gaucheB = autreBox.getCoin(0).x
        droiteB = autreBox.getCoin(2).x
        
        xFaitQueAPeutEtreDansB = gaucheB < gaucheA < droiteB or gaucheB < droiteA < droiteB
        yFaitQueAPeutEtreDansB = hautB < hautA < basB or hautB < basA < basB
        coinDeAEstDansB = xFaitQueAPeutEtreDansB and yFaitQueAPeutEtreDansB
        
        xFaitQueBPeutEtreDansA = gaucheA < gaucheB < droiteA or gaucheA < droiteB < droiteA
        yFaitQueBPeutEtreDansA = hautA < hautB < basA or hautA < basB < basA
        coinDeBEstDansA = xFaitQueBPeutEtreDansA and yFaitQueBPeutEtreDansA
        
        return coinDeAEstDansB or coinDeBEstDansA