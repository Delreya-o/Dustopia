from Niveau import *

import pygame


"""dessinerLesBoutons(etatDuJeu) se trouve ici pour éviter les cycles d'importations"""
"""Pareil pour dessinerMenu"""


class Bouton:
    def __init__(self, x, y, texte="TexteVide"):
        """Les coordonnées sont en blocs, pour que quand on agrandit
        l'image, le bouton s'agrandisse"""

        #self.x et self.y sont en pourcentages de fenêtre (entre 0 et 1)
        self.x = x
        self.y = y
        
        #Le texte est une chaîne de caractères
        self.texte = texte

        #On calcule la widht et la height en pixels, on doit donc charger temporairement la police
        objet_font_tmp = pygame.font.Font(cheminAbsolu("RubikIso-Regular.ttf"), 34)
        (self.width, self.height) = objet_font_tmp.size(texte)

    def estSurvole(self, etatDuJeu):
        """Renvoie si le bouton est survolé
        (donc si il est affiché et qu'il
        touche la souris)"""
    
        fenetre = etatDuJeu["fenetre"]
        #On a la position du curseur en pixels
        positionCurseur = pygame.mouse.get_pos()

        #On calcule la position de self.x et de self.y en pixels sans les modifier
        x = self.x * fenetre.get_width()
        y = self.y * fenetre.get_height()


        distanceX = abs(positionCurseur[0] - x)
        distanceY = abs(positionCurseur[1] - y)

        return self.doitEtreAffiche(etatDuJeu) and distanceX <= self.width / 2 and distanceY <= self.height / 2

    def draw(self, etatDuJeu):
        fenetre = etatDuJeu["fenetre"]

        #On calcule la position de self.x et de self.y en pixels sans les modifier
        x = self.x * fenetre.get_width()
        y = self.y * fenetre.get_height()

        #On calcule le coin en haut à gauche en pixels
        coinHautGauche = (x - self.width / 2, y - self.height / 2)

        #On calcule le rectangle du bouton
        rect = pygame.Rect(coinHautGauche[0], coinHautGauche[1], self.width, self.height)

        #On l'applique à la fenêtre
        pygame.draw.rect(fenetre, (239, 139, 12), rect)

        #On affiche le texte
        pointCentral = (x, y)
        afficherTexte(etatDuJeu, self.texte, "RubikIso-Regular.ttf", 34, pointCentral, (0, 0, 0))

    def doitEtreAffiche(self, etatDuJeu):
        """Renvoie si le bouton doit être affiché ou non"""
        if self == etatDuJeu["dicoBoutons"]["Game Over Quitter"]:
            return etatDuJeu["barreVie"].estMort
        elif self == etatDuJeu["dicoBoutons"]["Game Over Recommencer"]:
            return etatDuJeu["barreVie"].estMort
        elif self == etatDuJeu["dicoBoutons"]["Menu Quitter"]:
            return etatDuJeu["menuLance"]
        elif self == etatDuJeu["dicoBoutons"]["Menu Jouer"]:
            return etatDuJeu["menuLance"]
        else:
            reporterErreur([self.texte])

    def action(self, etatDuJeu):
        """Il faut vérifier que le bouton est survolé pour appeler cette fonction"""
        assert self.estSurvole(etatDuJeu)
        
        dicoBoutons = etatDuJeu["dicoBoutons"]
    
    
        #On fait un bruit de bouton
        bruit_bouton = etatDuJeu["dicoBruits"]["bouton.wav"]
        bruit_bouton.play()
        
        if self.texte == "Quitter":
            etatDuJeu["jeuTourne"] = False
            
        elif self.texte == "Recommencer":
            chargerNiveau(etatDuJeu, etatDuJeu["nNiveau"])
            barreVie = etatDuJeu["barreVie"]
            barreVie.vie = 3
            barreVie.estMort = False
            
        elif self.texte == "Jouer":
            etatDuJeu["menuLance"] = False
            
        else:
            reporterErreur([self.texte])

def dessinerLesBoutons(etatDuJeu):
    dicoBoutons = etatDuJeu["dicoBoutons"]
    
    for bouton in dicoBoutons.values():
        if bouton.doitEtreAffiche(etatDuJeu):
            bouton.draw(etatDuJeu)

def afficherMenu(etatDuJeu):
    fenetre = etatDuJeu["fenetre"]
    fenetre.fill((255,179,83))
    pointCentral = (fenetre.get_width()/2, fenetre.get_height()/2)
    haut = (fenetre.get_width()/2, fenetre.get_height()/4)
    
    dessinerLesBoutons(etatDuJeu)

    text = "DUSTOPIA"
    afficherTexte(etatDuJeu, text, "Boba Cups.ttf", 34, haut, (0, 0, 0))#"Boba Cups.ttf"

    pygame.display.flip()
    
