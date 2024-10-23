from divers import *
from Dialogue import *
from Box import *
from dessiner import *
from CompteurEtoiles import *
from Bouton import *


import pygame


class BarreVie:
    def __init__(self,vie=3):
        self.vie = vie
        self.tempsInvincibilite = -1
        self.estMort = False
        self.heurteAutreBox = False

    def degat(self, etatDuJeu):
        if self.vie > 1:
            self.vie -= 1
            
            #On fait un bruit de dégât
            bruit_degat = etatDuJeu["dicoBruits"]["degat.wav"]
            bruit_degat.play()
        else:
            self.estMort = True
        
        
    def affichage(self, etatDuJeu):
        fenetre = etatDuJeu["fenetre"]
        pyImageCharbon = etatDuJeu["dicoForeground"]["charbon.png"].pyImage 
        
        #On calcule la taille d'une image charbon en pixels
        width = pyImageCharbon.get_width()
        height = pyImageCharbon.get_height()
        
        #On calcule le rectangle de la barre de vie
        rect = pygame.Rect(0,0,self.vie * width, height)
        
        #on l'applique à la fenêtre
        pygame.draw.rect(fenetre, (255,255,255), rect)
        
        for i in range(self.vie):
            fenetre.blit(pyImageCharbon, (i * width, 0))
        #x, y = self.box(0,0).x, self.box.fenetre.get_height.y
    

    def GameOver(self, etatDuJeu):
        fenetre = etatDuJeu["fenetre"]
        fenetre.fill((255,179,83))

        premiertiers = (fenetre.get_width()/2, fenetre.get_height()/4)
        pointCentral = (fenetre.get_width()/2, fenetre.get_height()/2)
        deuxiemetiers = (fenetre.get_width()/2, fenetre.get_height()/3)
        texte = "Mince alors, tu t'es fait capturer" 
        texte1 = "Tu n'as pas pu sauver tes amis"
        texte2 = "Veux tu recommencer ?"

        afficherTexte(etatDuJeu, texte, "Boba Cups.ttf", 34, premiertiers, (0, 0, 0))
        afficherTexte(etatDuJeu, texte1, "Boba Cups.ttf", 34, deuxiemetiers, (0, 0, 0))
        afficherTexte(etatDuJeu, texte2, "Boba Cups.ttf", 34, pointCentral, (0, 0, 0))

        dessinerLesBoutons(etatDuJeu)

        pygame.display.flip()
        
        #Si la musique actuelle n'est pas musique_mort
        if etatDuJeu["musique"][1] == "Ce n'est pas la musique de mort":
            #On arrête la musique actuelle
            etatDuJeu["musique"][0].stop()
            #On charge la musique de mort
            musique_mort = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_mort.wav"))
            #On joue la musique de mort une fois
            musique_mort.play()
            #On met à jour etatDuJeu
            etatDuJeu["musique"] = (musique_mort, "C'est la musique de mort")
        
        
        #Si on avait récupéré l'étoile dans ce niveau
        if etatDuJeu["niveau"].etoile.autresParametres["ticksTouchee"] == 30:
            #On la perd
            etatDuJeu["compteurEtoiles"].decrementer()
            #On dit qu'on a touché l'étoile pendant 0 ticks
            etatDuJeu["niveau"].etoile.autresParametres["ticksTouchee"] = 0