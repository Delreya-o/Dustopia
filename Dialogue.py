from divers import *

import pygame

class Dialogue:
    def __init__(self, texte, nomPolice="Bob.ttf", xDebut=None, xFin=None):
        
        self.texte = texte
        #On stocke l'objet font directement pour éviter de le recalculer à chaque image
        self.police = pygame.font.Font(cheminAbsolu(nomPolice), 24)
        
        self.i = 0
        #Le nombre de lettres qui sont déjà affichées
        
        self.xDebut = xDebut
        self.xFin = xFin
        #L'intervalle dans le niveau où le dialogue est déclenché
        
        self.surfacePrecedente = None
        #Permet de, quand le texte est déjà entièrement chargé,
        #de ne pas avoir besoin de tout recalculer, car cela génère
        #beaucoup trop de lag.
    
    def parler(self, etatDuJeu):
        """Au premier appel de cette méthode, on affiche la première lettre.
        Au deuxième appel de cette méthode, on affiche une deuxième lettre.
        Si toutes les lettres ont déjà été affichées, on continue de tout
        afficher."""
        
        fenetre = etatDuJeu["fenetre"]
        
        #On calcule le point où l'on va afficher le texte
        pointCentral = (fenetre.get_width()/2, fenetre.get_height()*4/5)
        if etatDuJeu["nNiveau"] ==11 :
            pointCentral = (fenetre.get_width()/2, fenetre.get_height()/2)
        #Si l'on n'avait pas affiché toutes les lettres
        if self.i<len(self.texte):
            
            #On rajoute une lettre à afficher
            self.i += 1
            
            #On affiche le texte et on stocke le rendu
            self.surfacePrecedente = afficherTexte(etatDuJeu, self.texte[:self.i], self.police, None, pointCentral, (255, 255, 255))
            
        else:
            #On affiche directement le rendu déjà calculé
            fenetre.blit(self.surfacePrecedente, getCoinHautGauche(self.surfacePrecedente, pointCentral))

def afficherTexte(etatDuJeu, texte, police, taillePolice, pointCentral, rgb):
    """
    Affiche le texte (c'est donc une procédure).
    Mais on renvoie aussi la surface calculée.
    Les coordonnées en entrée sont en pixels.
    La taille de la police est en pts.
    
    La police peut soit être un string, soit un
    objet font. Il est préférable d'utiliser un
    objet font. Dans ce cas, il est possible de
    donner None en paramètre pour taillePolice.
    """
    
    #On récupère la fenêtre
    fenetre = etatDuJeu["fenetre"]
    
    if type(police) is str:
        #On récupère la police
        police = pygame.font.Font(cheminAbsolu(police), taillePolice)
    
    #On calcule le rendu
    rendu = police.render(texte, True, rgb)
    #On calcule le coin en haut à gauche
    coinHautGauche = getCoinHautGauche(rendu, pointCentral)
    #On l'applique à la fenêtre
    fenetre.blit(rendu, coinHautGauche)
    #On renvoie la surface calculée
    return rendu