from divers import *
import pygame

class CompteurEtoiles:
    def __init__(self, n=0):
        self.police = pygame.font.Font(cheminAbsolu("Kanit-Regular.ttf"), 18)
        self.setCompteur(n)

    def setCompteur(self, n):
        self.compteur = n
        self.surface = self.police.render(str(n), True, (0, 0, 0))
    
    def incrementer(self):
        self.setCompteur(self.compteur+1)
    
    def decrementer(self):
        self.setCompteur(self.compteur-1)
        
    def draw(self, etatDuJeu):
        fenetre = etatDuJeu["fenetre"]
        pyImageEtoile = etatDuJeu["dicoForeground"]["etoile_compteur.png"].pyImage
        
        #On affiche l'étoile
        fenetre.blit(pyImageEtoile, (fenetre.get_width() - pyImageEtoile.get_width(), 0))
        
        #On calcule le point central de l'étoile
        pointCentral = (fenetre.get_width() - pyImageEtoile.get_width()/2, pyImageEtoile.get_height()/2)
        
        #On place la surface du texte (pré-calculée) au centre de l'étoile
        fenetre.blit(self.surface, getCoinHautGauche(self.surface, pointCentral))