from dessiner import *
from barreDeVie import *
from sauvegarder import *

import pygame

def gererLesEvenements(etatDuJeu):
    joueur = etatDuJeu["listeEntites"][0]
    barreVie = etatDuJeu["barreVie"]
    accelerationX = etatDuJeu["accelerationX"]
    tauxConservationVitesse = etatDuJeu["tauxConservationVitesse"]
    
    
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            etatDuJeu["jeuTourne"] = False
        elif evenement.type == pygame.VIDEORESIZE:
            chargerLeForeground(etatDuJeu)
            chargerLeBackground(etatDuJeu)
        elif evenement.type == pygame.KEYDOWN and etatDuJeu["nNiveau"] != 11 and not etatDuJeu["menuLance"]:
            if evenement.key == pygame.K_s:
                sauvegarder(etatDuJeu, 1)
            elif evenement.key == pygame.K_l:
                chargerSauvegarde(etatDuJeu, 1)
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            for bouton in etatDuJeu["dicoBoutons"].values():
                if bouton.estSurvole(etatDuJeu):
                    bouton.action(etatDuJeu)

        
    
    touchePressees = pygame.key.get_pressed()
    if etatDuJeu["tickAnimationBob"] == 0 and etatDuJeu["tickAnimation"] == 0:
        if touchePressees[pygame.K_LEFT]:
            joueur.box.vitesse.x -= accelerationX
            joueur.nomImage = "zKakuSourireGrisGauche.png"
        if touchePressees[pygame.K_RIGHT]:
            joueur.box.vitesse.x += accelerationX
            joueur.nomImage = "zKakuSourireGrisDroite.png"
        if touchePressees[pygame.K_UP]:
            joueur.sauteSiPossible(etatDuJeu)
    
    joueur.box.vitesse.x *= tauxConservationVitesse