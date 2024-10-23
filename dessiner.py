from Dialogue import *

from divers import *

from CompteurEtoiles import *

from animations import *

import pygame
import math

class Image:
    def __init__(self, width=None, height=None, pyImage=None):
        """Les unités sont en blocs"""
        self.width = width
        self.height = height
        self.pyImage = pyImage #image est un objet pygame

    def drawAsForeground(self, etatDuJeu, x, y):
        """Affiche une image aux coordonnées (x, y) (coordonnées en blocs)
        Les coordonnées passées en paramètres sont relatives au niveau, pas
        à la fenêtre. On doit donc faire des conversions dans cette fonction.
        """
        tailleBloc = tailleBlocEnPixels(etatDuJeu)
        
        fenetre = etatDuJeu["fenetre"]
        joueurPosX = etatDuJeu["listeEntites"][0].box.pos.x
        fenetreWidth = fenetre.get_size()[0] / tailleBloc
        
        x =  x - joueurPosX + fenetreWidth/3
        #On rend les coordonnées relatives à la fenêtre
        #Le bloc (x, y) doit reculer quand la position du joueur augmente (donc on enlève joueurPosX)
        #et le bloc (0, 0) doit être tout à gauche de l'écran, et non au (-1)ième tiers, quand le
        #joueur est au premier tiers (donc on rajoute un tiers)
        
        fenetre.blit(self.pyImage, (x*tailleBloc, y*tailleBloc))
        #On multiplie par la taille des blocs en pixels, pour convertir les
        #coordonnées en pixels
    
    def drawAsBackground(self, etatDuJeu, numeroBackground):
        """Affiche le fond d'écran. Le premier fond d'écran a comme numéro 0,
        celui juste après a comme numéro 1, etc."""
        tailleBloc = tailleBlocEnPixels(etatDuJeu)
        
        fenetre = etatDuJeu["fenetre"]
        joueurPosX = etatDuJeu["listeEntites"][0].box.pos.x
        
        x = -joueurPosX*0.015
        
        fenetre.blit(self.pyImage, (x*tailleBloc + self.pyImage.get_width()*numeroBackground, 0))


def tailleBlocEnPixels(etatDuJeu):
    """Renvoie la taille d'un bloc en pixels"""
    fenetre = etatDuJeu["fenetre"]
    niveau = etatDuJeu["niveau"]
    
    longueurFenetre = fenetre.get_width()
    hauteurFenetre = fenetre.get_height()
    longueurNiveau = niveau.width
    hauteurNiveau = niveau.height
    
    
    return max(math.ceil(longueurFenetre*3 / longueurNiveau), math.ceil(hauteurFenetre / hauteurNiveau))

def drawBloc(etatDuJeu, x, y, typeBloc):
    """Affiche le bloc aux coordonnées (x, y) (coordonnées en blocs)
    Les coordonnées sont relatives au niveau, pas à la fenêtre ou au
    joueur.
    """
    
    nousSommesDansUnDesert = etatDuJeu["nNiveau"] in etatDuJeu["niveauxDesert"]
    nousSommesDansLaNeige = etatDuJeu["nNiveau"] in etatDuJeu["niveauxNeige"]
    nomImage = {
        1: "sable.png" if nousSommesDansUnDesert else "neige.png" if nousSommesDansLaNeige else "sol.jpg",
        2: "briques.png",
        3: "briques_fond.png",
        4: "briques_toit.png",
        5: "evacuer.png" if etatDuJeu["nTicks"]//25 % 2 == 0 else "decollage.png",    #On alterne toutes les demi-secondes
        6: "portail.png",
        7: "bienvenue.png",
        8: "fusee.png",
        
        9.1: "poubelle1.png",
        9.2: "poubelle2.png",
        9.3: "poubelle3.png",
        9.4: "poubelle4.png",
        9.5: "poubelle5.png",
        9.6: "poubelle6.png"
    }[typeBloc]
        
    etatDuJeu["dicoForeground"][nomImage].drawAsForeground(etatDuJeu, x, y)

def chargerLeForeground(etatDuJeu):
    """Met à jour etatDuJeu["dicoForeground"].

    dicoImages a comme clés les noms des images (par
    exemple "toto.png") et comme valeurs un objet Image,
    qui contient une longueur en blocs, une largeur
    en blocs, et un objet pygame.image.

    Cette fonction modifie les pygame.image selon la
    résolution de l'écran. On doit donc l'appeler à chaque
    fois que la résolution de la fenêtre change.
    """
    
    dicoForeground = etatDuJeu["dicoForeground"]
    tailleBloc = tailleBlocEnPixels(etatDuJeu)
    
    for nomImage in dicoForeground:
        image = dicoForeground[nomImage]
        #On récupère l'objet Image
        
        width  = image.width * tailleBloc
        height = image.height * tailleBloc
        #On calcule les dimensions de l'image en pixels par rapport
        # à ses dimensions en blocs et par rapport à la longueur des
        # blocs en pixels

        pyImage = pygame.image.load(cheminAbsolu("images", nomImage))
        #On charge l'objet pygame.image
        
        pyImage = pygame.transform.scale(pyImage, (width, height))
        #On lui donne les bonnes dimensions
        
        #On convertit (on ne met pas de transparence pour les blocs opaques)
        image.pyImage = pyImage.convert() if nomImage in ["sol.jpg", "briques.png", "briques_fond.png", "briques_toit.png"] else pyImage.convert_alpha()

def chargerLeBackground(etatDuJeu):
    """Fait comme chargerLeForeground, mais les
    objets Image n'ont pas de longueur et de
    largeur définie, car les longueurs et les
    largeurs ne servent qu'à décrire la taille en
    blocs."""
    
    dicoBackground = etatDuJeu["dicoBackground"]
    tailleBloc = tailleBlocEnPixels(etatDuJeu)
    niveau = etatDuJeu["niveau"]
    
    for nomImage in dicoBackground:
        image = dicoBackground[nomImage]
        #On récupère l'objet Image
        
        pyImage = pygame.image.load(cheminAbsolu("images", nomImage))
        #On charge l'objet pygame.image
        
    #On récupère la hauteur du background en pixels
        height  = tailleBloc * niveau.height
        #On récupère la longueur du background en pixels
        width = pyImage.get_width() * height / pyImage.get_height() 

        pyImage = pygame.transform.scale(pyImage, (width, height))
        #On lui donne les bonnes dimensions

        #On l'optimise en utilisant convert (mais il ne peut pas y avoir de transparent)
        #C'est pour ça qu'on n'optimise pas le foreground
        image.pyImage = pyImage.convert()

def dessine(etatDuJeu):
    
    niveau = etatDuJeu["niveau"]
    fenetre = etatDuJeu["fenetre"]
    listeEntites = etatDuJeu["listeEntites"]
    tickAnimation = etatDuJeu["tickAnimation"]
    joueur = etatDuJeu["listeEntites"][0]
    
    niveau.dessinerLesBackgrounds(etatDuJeu)
    
    #On calcule la longueur de la fenêtre en blocs
    widthFenetre = math.ceil(fenetre.get_width() / tailleBlocEnPixels(etatDuJeu))
    #On calcule la gauche de l'écran (ou 0 si c'est négatif)
    abscisseGauche = max(0, math.floor(joueur.box.pos.x - 1/3 * widthFenetre))
    for y in range(niveau.height):
        for x in range(max(0, abscisseGauche-7), min(abscisseGauche + widthFenetre + 1, niveau.width)):#-7 car les pancartes font 8 blocs de longueur
            #Si ce n'est pas de l'air, on dessine le bloc
            if niveau.getBloc(x, y)!=0:
                drawBloc(etatDuJeu, x, y, niveau.getBloc(x, y))
            
    for entite in listeEntites:
        if abscisseGauche - 10 < entite.box.pos.x < min(abscisseGauche + widthFenetre + 1, niveau.width) + 2: #-10 pour les susuwataris qui fuient
            entite.draw(etatDuJeu)
    
    
    #On gère les animations ici car on ne veut pas que
    #son texte soit couvert par les autres images
    gererLesAnimations(etatDuJeu)
    
    etatDuJeu["barreVie"].affichage(etatDuJeu)
    
    etatDuJeu["compteurEtoiles"].draw(etatDuJeu)
    
    niveau.gererLesDialogues(etatDuJeu)
    ticksDeFondNoir = 100
    #Quand le fond noir doit s'afficher
    if tickAnimation > 300 - ticksDeFondNoir:
        #On crée un rectangle supportant la transparence
        fondNoir = pygame.Surface((fenetre.get_width(), fenetre.get_height()))
        #On calcule l'opacité entre 0 et 255 (255 étant entièrement opaque)
        opacite = (tickAnimation - (300-ticksDeFondNoir)) / ticksDeFondNoir * 255
        #On applique l'opacité
        fondNoir.set_alpha(opacite)
        #On lui met la couleur noir
        fondNoir.fill((0,0,0))
        #On applique le fond noir
        fenetre.blit(fondNoir, (0, 0))
    
    
    
    pygame.display.flip()