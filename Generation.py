import pygame

from divers import *
from Vecteur import *

import Box as boite
import Entite as ent

import random as rd

class Generateur :
    def __init__(self, coordonnes, typeMonstre,  nbGenereMax, intervalleTemps):
        self.coordonnes = coordonnes                    #couple d'entiers, coordonnes du generateur
        self.typeMonstre = typeMonstre                  #chaine de caractere, type de monstre genere
        self.nbGenereMax = nbGenereMax                  #entier, nombre maximum de generation
        self.intervalleTemps = intervalleTemps          #reel,  temps en secondes correspondant au temps entre chaque generation de monstre
        self.derniereGeneration = 0                     #secondes, temps en econdes correspondant au moment ou le dernier monstre a ete genere (/!\ dernier mais pas final)
        self.nbMonstresGeneres = 0                      #entier, nombre de monstres deja generes

    def genereMonstre(self, etatDuJeu, coordonnees, typeM):
        #Procedure : genere un type de monstre selon la position d'un generateur
        #@param :
        #    - etatDuJeu : dictionnaire, contenant les information de l'etat actuel du jeu
        #    - generateur : couple d'entier, correspond aux coordonnees (x,y) du generateur
        #    - typeM : chaine de caractere, type de monstre : type1 (balais), type2 (eponge/plumeau)
        mImage = self.typeMonstre + ".png"
        mWidth, mHeight =  etatDuJeu["dicoForeground"][mImage].width , etatDuJeu["dicoForeground"][mImage].height

        #creation d'un monstre aux coordoonees (x,y), soit a droite d'un generateur 
        x, y = coordonnees[0] + 1, coordonnees[1] - mHeight/2
        monstre = ent.Entite(self.typeMonstre, boite.Box(Vecteur(x, y), mWidth, mHeight, Vecteur(0, 0)), mImage, {"direction" : ""})
        etatDuJeu["listeEntites"].append(monstre)
    
    
    def generation(self, etatDuJeu, tempsPasse):
        #vérifie si :
        #   -le nombre de monstre généré par le générateur n'a pas dépassé le nombre maximal de génération
        #   -le générateur ne vient pas de générer un monstre
        #   -la différence entre l'instant où la fonction a été appelée 
        #       et celui de sa dernière génération est bien égale à l'intervalle de temps du générateur
        if self.nbMonstresGeneres < self.nbGenereMax and tempsPasse != self.derniereGeneration and (tempsPasse % self.intervalleTemps) == 0:
            self.genereMonstre(etatDuJeu, self.coordonnes, self.typeMonstre)
            self.derniereGeneration = tempsPasse
            self.nbMonstresGeneres += 1
            

def initialiserGenerateurs(etatDuJeu) :
    #creation des objets Generateurs en utilisant les coordonnees des generateurs du niveau,
    #l'intervalle entre chaque generation de monstre et le nombre maximal de geeration est aleatoire
    niveau = etatDuJeu["niveau"]
    for y in range(niveau.height):
        for x in range(niveau.width):
            if niveau.getBloc(x, y) == 9.1 :
                intervalleT = rd.choice(range(9, 15))
                nbGMax = rd.choice(range(2, 5)) if etatDuJeu["nNiveau"] != 7 else 1
                etatDuJeu["generateurs"].append(Generateur((x, y), rd.choice(etatDuJeu["listeMonstre"]), nbGMax, intervalleT))


def regirGenerateurs(etatDuJeu, tempsPasse) :
    #pour chaque generateur de la liste, lancer la méthode generation de l'objet Generation.py
    for generateur in etatDuJeu["generateurs"] :
        generateur.generation(etatDuJeu, tempsPasse)

def deplacementsMonstres(etatDuJeu):  #la vitesse peut etre changee en fonction de la difficulte du niveau, pour l'instant elle est de 0,02
    #en utilisant l'attribut "autresParametres" de l'objet entite, on donne la direction du monstre
    for monstre in etatDuJeu["listeEntites"] :
        if monstre.nom in etatDuJeu["listeMonstre"] :
            #si Droite : vitesse = -0,02, sinon 0,02

            
            #Quand on heurte un bloc vers la gauche ou que l'on n'a pas de direction définie
            if "Gauche" in monstre.box.alignementsPrecedents or monstre.autresParametres["direction"] == "":
                monstre.autresParametres["direction"] = "Gauche"
            #Quand on heurte un bloc vers la droite
            elif "Droite" in monstre.box.alignementsPrecedents :
                monstre.autresParametres["direction"] = "Droite"
            
            if monstre.autresParametres["direction"] == "Droite":
                monstre.box.vitesse.x = -0.02
            elif monstre.autresParametres["direction"] == "Gauche":
                monstre.box.vitesse.x = 0.02
            else:
                reporterErreur([monstre.box.alignementsPrecedents, monstre.autresParametres["direction"]])