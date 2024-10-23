#import sys
#sys.path.append('/Users/anouk/Library/Python/3.9/lib/python/site-packages')


from Niveau import *
from Box import *
from Entite import *
from Vecteur import *
from Bouton import *
from CompteurEtoiles import *



from divers import *
from dessiner import *
from evenements import *
from barreDeVie import *
from animations import *


from Generation import *

import pygame
import math
import os

def update(etatDuJeu):
    dateActuelle = pygame.time.get_ticks()
    listeEntites = etatDuJeu["listeEntites"]
    niveau = etatDuJeu["niveau"]
    joueur = listeEntites[0]
    
    for entite in listeEntites:
        entite.updateBox(etatDuJeu)
    
    if joueur.box.pos.y >= niveau.height:
        #Il faut se rappeler que l'ordonnée est contre-intuitive (Plus elle est grande, plus on est bas)
        etatDuJeu["barreVie"].estMort = True
    
    #Si le joueur a touché l'étoile ou qu'elle est encore là
    if joueur.toucheEtoile(etatDuJeu) or 0 < niveau.etoile.autresParametres["ticksTouchee"] < 30:
        etoile = niveau.etoile 
        
        #On dit qu'on a touché l'étoile pendant un tick de plus
        etoile.autresParametres["ticksTouchee"] += 1
        
        #Au bout de 30 ticks
        if etoile.autresParametres["ticksTouchee"] == 30:
            
            for (i, entite) in enumerate(listeEntites):
                if entite == etoile:
                    #On enlève l'étoile de la liste des entités
                    listeEntites.pop(i)
            
            #On incrémente le compteur d'étoiles de 1
            etatDuJeu["compteurEtoiles"].incrementer()
    


def main():
    pygame.init()
    pygame.display.set_caption("Dustopia")
    pygame.event.set_allowed([pygame.QUIT, pygame.VIDEORESIZE, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]) #N'autorise que les événements utilisés pour réduire le lag
    resolution = (900, 600)
    fenetre = pygame.display.set_mode(resolution, pygame.RESIZABLE | pygame.DOUBLEBUF)#DOUBLEBUF réduit le lag
    
    
    dicoForeground = {
        "sol.jpg" : Image(1, 1),
        "zkakuDeFace.png" : Image(1.3, 1.3),
        "zKakuSourireGrisGauche.png" : Image(1.3, 1.2),
        "zKakuSourireGrisDroite.png" : Image(1.3, 1.2),
        "etoile0.png" : Image(3, 3),
        "etoile1.png" : Image(3, 3),
        "etoile2.png" : Image(3, 3),
        "etoile3.png" : Image(3, 3),
        "poubelle1.png" : Image(1, 1),
        "poubelle2.png" : Image(1, 1),
        "poubelle3.png" : Image(1, 1),
        "poubelle4.png" : Image(1, 1),
        "poubelle5.png" : Image(1, 1),
        "poubelle6.png" : Image(1, 1),
        "balai.png" : Image(1.9, 2.6),
        "spray.png" : Image(1.5, 2.5),
        "aspi.png" : Image(2.5, 2.5), 
        "Bob.png" : Image(3, 24),
        "charbon.png" : Image(1,1),
        "sable.png" : Image(1, 1),
        "neige.png" : Image(1, 1),
        "etoile_compteur.png" : Image(1.5, 1.5),
        "briques.png" : Image(1, 1),
        "briques_fond.png" : Image(1, 1),
        "briques_toit.png" : Image(1, 1),
        "evacuer.png" : Image(8, 5),                #Pancarte
        "decollage.png" : Image(8, 5),              #Pancarte
        "portail.png" : Image(8, 5),                #Pancarte
        "bienvenue.png" : Image(8, 5),              #Pancarte
        "fusee.png" : Image(8, 16)
    }

    dicoBackground = {
        "anight.png" : Image(),
        "bNS.png": Image(),
        "cSR.png": Image(),
        "dSD.png": Image(),
        "jour.png": Image(),
        "middle-of-day-and-sunset.png": Image(),
        "suunset.png": Image(),
        "background_desert.png" : Image(),
        "background_neige.png" : Image(),
        "image_nebuleuse_1.png" : Image(),
        "image_etoiles.jpg" : Image()
    }
    
    dicoBruits = {
        "degat.wav" : pygame.mixer.Sound(cheminAbsolu("musiques", "degat.wav")),
        "bouton.wav" : pygame.mixer.Sound(cheminAbsolu("musiques", "bouton.wav")),
        "saut.wav" : pygame.mixer.Sound(cheminAbsolu("musiques", "saut.wav"))
    }
    
    dicoBoutons = {
        "Game Over Recommencer" : Bouton(0.25, 0.8, "Recommencer"),
        "Game Over Quitter" : Bouton(0.75, 0.8, "Quitter"),
        "Menu Jouer" : Bouton(0.5, 0.5, "Jouer"),
        "Menu Quitter" : Bouton(0.5, 0.75, "Quitter")
    }
    
    barreVie = BarreVie()
    joueur = Entite("Joueur", Box(None, 1.3, 1.2, None), "zKakuSourireGrisDroite.png")
    
    etatDuJeu = {
        "jeuTourne" : True,
        "listeEntites" : [joueur],
        "niveau" : None,
        "fenetre" : fenetre,
        "generateurs" : [],
        "dicoForeground" : dicoForeground,
        "dicoBackground" : dicoBackground,
        "barreVie" : barreVie,
        "dicoBoutons" : dicoBoutons,
        "musique" : None,
        "listeMonstre" : ["balai", "spray", "aspi"],
        "forceSaut" : 0.45,
        "accelerationX" : 0.03,                           #De combien la vitesse est augmentée quand la touche est maintenue
        "forceGravite" : 0.02,                            #De combien la vitesse est augmentée quand on tombe
        "tauxConservationVitesse" : 0.8,                  #Permet de simuler les frottements de l'air
        "tickAnimation" : 0,                              #Le nombre de ticks depuis le début de l'animation de fin
        "tickAnimationBob" : 0,
        "niveauSuivant" : False,                          #Dit si l'on doit aller au nivcau suivant
        "nNiveau" : 0,
        "niveauxDesert" : [6],                              #Contient les numéros des niveaux qui se déroulent dans le désert
        "niveauxNeige" : [7],
        "compteurEtoiles" : CompteurEtoiles(),
        "nTicks" : 0,                                     #Utile pour les pancartes
        "dicoBruits" : dicoBruits,
        "bobAParle" : False,
        "menuLance" : True                                #Le menu est lancé par défaut
    }
    
    chargerNiveau(etatDuJeu, 0)
    
    chargerLeForeground(etatDuJeu)
    chargerLeBackground(etatDuJeu)
    
    imagesParSeconde = 50
    dateDuDernierTick = -1
    dateInit = pygame.time.get_ticks()
    
    
    while etatDuJeu["jeuTourne"]:
        dateActuelle = pygame.time.get_ticks()
        if dateActuelle - dateDuDernierTick >= 1000 / imagesParSeconde:
            #Si le nombre de millisecondes depuis le dernier tick est plus grand ou égal au nombre de millisecondes à attendre
            dateDuDernierTick = dateActuelle
            
            etatDuJeu["nTicks"] +=1
            
            gererLesEvenements(etatDuJeu)
            
            if barreVie.estMort :
                barreVie.GameOver(etatDuJeu)
            elif etatDuJeu["menuLance"]:
                afficherMenu(etatDuJeu)
            else:
                
                listeEntites = etatDuJeu["listeEntites"]
                for entite in listeEntites[1:]:
                    if entite.nom in etatDuJeu["listeMonstre"]:
                        #Si on n'a plus de temps d'invincibilité
                        if barreVie.tempsInvincibilite < 0:
                            if joueur.box.heurteAutreBox(entite.box):
                                barreVie.degat(etatDuJeu)
                                barreVie.tempsInvincibilite = 50
                barreVie.tempsInvincibilite -= 1
                
                deplacementsMonstres(etatDuJeu)
                gererLesSusuwatarisQuiFuient(etatDuJeu)
                
                update(etatDuJeu)
                dessine(etatDuJeu)
                
            if etatDuJeu["niveauSuivant"]:
                nEtoiles = etatDuJeu["compteurEtoiles"].compteur
                #Si on est à la fin du niveau 5 et qu'on n'a pas 6 étoiles
                if etatDuJeu["nNiveau"] == 5 and nEtoiles < 6:
                    #On va au niveau de fuite
                    etatDuJeu["nNiveau"] = 8
                #Sinon, si on est au premier niveau bonus mais qu'on n'a pas récupéré l'étoile
                elif etatDuJeu["nNiveau"] == 6 and nEtoiles < 7:
                    #On va au niveau de fuite
                    etatDuJeu["nNiveau"] = 8
                else:
                    etatDuJeu["nNiveau"] += 1
                
                etatDuJeu["bobAParle"] = False
                chargerNiveau(etatDuJeu, etatDuJeu["nNiveau"])
                etatDuJeu["niveauSuivant"] = False
            

        tempsPasse = (dateActuelle - dateInit) // 1000
        regirGenerateurs(etatDuJeu, tempsPasse)

        


main()