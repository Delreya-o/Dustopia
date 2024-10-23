from Box import *

from divers import *

import random

class Entite:
    def __init__(self, nom, box, nomImage, autresParametres={}):
        self.nom = nom
        self.box = box
        self.nomImage = nomImage
        self.autresParametres=autresParametres
        #Par exemple, un autre paramètre est "ticksTouchee"
        # qui dit le nombre de ticks depuis que l'étoile a
        #été touchée
    
    def __str__(self):
        return f"Entite('{self.nom}', {self.box})"
    
    def updateBox(self, etatDuJeu):
        """Met à jour la box de l'entité"""
        if "Etoile" not in self.nom:
            self.box.updatePos(etatDuJeu)
    
    def getBox(self):
        return self.box
    
    def draw(self, etatDuJeu):
        x, y = self.box.getCoin(0).x, self.box.getCoin(0).y
        
        #On fait pivoter l'étoile
        if "etoile" in self.nomImage:
            self.nomImage = "etoile" + str(self.autresParametres["ticksTouchee"]//4%4) + ".png"
        
        etatDuJeu["dicoForeground"][self.nomImage].drawAsForeground(etatDuJeu, x, y)
    
    def toucheEtoile(self, etatDuJeu):
        """Renvoie si l'entité touche l'étoile.
        Renvoie toujours False si l'étoile est déjà
        attrapée"""
        etoile = etatDuJeu["niveau"].etoile
        return self.box.heurteAutreBox(etoile.box) and etoile.autresParametres["ticksTouchee"]!=30

    def saute(self, etatDuJeu):
        """Fait un saut, même si il n'y a pas de sol sous l'entité"""
        #L'entité saute
        self.box.vitesse.y = -etatDuJeu["forceSaut"]
        #Elle fait un bruit de saut
        bruit_saut = pygame.mixer.Sound(cheminAbsolu("musiques", "saut.wav"))
        bruit_saut.play()
    
    def sauteSiPossible(self, etatDuJeu):
        """Fait un saut ssi il y a du sol sous l'entité"""
        
        #Si l'entité touche le sol
        if "Bas" in self.box.alignementsPrecedents:
            #Elle saute
            self.saute(etatDuJeu)
    
    def sauteSansBruit(self, etatDuJeu):
        #L'entité saute
        self.box.vitesse.y = -etatDuJeu["forceSaut"]
    
    def sauteSiPossibleSansBruit(self, etatDuJeu):
        #Si l'entité touche le sol
        if "Bas" in self.box.alignementsPrecedents:
            #Elle saute sans bruit
            self.sauteSansBruit(etatDuJeu)

def creerEntiteCorrespondantAImage(etatDuJeu, nomImage, nom, x, y):
    """Prend un objet de la classe Image, un nom, une
    abscisse, une ordonnée, et renvoie une entité
    correspondante. Cette entité est aussi mise dans
    la liste des entités. Cette fonction sert à ne pas
    avoir besoin de spécifier deux fois les dimensions
    de l'image en blocs."""
    
    if nomImage in etatDuJeu["dicoForeground"]:
        image = etatDuJeu["dicoForeground"][nomImage]
    else:
        print("Erreur, creerEntiteCorrespondantAImage a été appelée avec le nom")
        print("d'une image n'étant pas dans dicoForeground. Le but de cette fo-")
        print("nction est de spécifier les dimensions de l'image en blocs une  ")
        print("seule fois (dans dicoForeground). Si l'image n'a pas été chargée")
        print(", alors cette information n'a pas été donnée                    ")
        assert False
    
    if "etoile" in nomImage:
        vitesse = None
    else:
        vitesse = Vecteur(0, 0)


    box = Box(Vecteur(x, y), image.width, image.height, vitesse)
    entite = Entite(nom, box, nomImage)
    
    etatDuJeu["listeEntites"].append(entite)
    
    return entite

def gererLesSusuwatarisQuiFuient(etatDuJeu):
    """Peut être appelée dans la boucle main() sans faire de conditions"""
    listeEntites = etatDuJeu["listeEntites"]
    
    #Si on est dans le niveau où il y a des susuwataris qui fuient
    if etatDuJeu["nNiveau"] == 8:
        
        #Aléatoirement
        if random.randint(0, 15) == 0:
            #On crée un susuwatari qui fuit (il est automatiquement mis dans la liste des entités)
            #Ce susuwatari commence sous le niveau, et va sauter dessus
            susuwatariQuiFuit = creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari qui fuit", -2, etatDuJeu["niveau"].height + 1)
            
            #Il saute sur le niveau (malgré le fait qu'il n'y ait pas de blocs sous lui)
            susuwatariQuiFuit.sauteSansBruit(etatDuJeu)
        
        #Pour chaque entité
        for i, entite in enumerate(listeEntites):
            #Si c'est un susuwatari qui fuit
            if entite.nom == "Susuwatari qui fuit":
                #Il saute si possible
                entite.sauteSiPossibleSansBruit(etatDuJeu)
                
                #il court
                entite.box.vitesse.x = 0.11
                
                #Si il est à la fusée
                if entite.box.pos.x > 140:
                    #Il disparaît
                    listeEntites.pop(i)