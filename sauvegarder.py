from divers import *
from Niveau import *

def sauvegarder(etatDuJeu, n):
    """Sauvegarde le nom du niveau fichier sauvegarde_n.txt"""
    
    with open(cheminAbsolu("sauvegardes", f"sauvegarde_{n}.txt"), "w") as fd:
        #On écrit l'indice du niveau
        fd.write(str(etatDuJeu["nNiveau"]) + " ")
        
        #Si l'étoile a été attrapée dans ce niveau
        if etatDuJeu["niveau"].etoile.autresParametres["ticksTouchee"] == 30:
            #On ne la stocke pas (pour ne pas pouvoir avoir une
            #infinité d'étoiles en relançant le niveau
            fd.write(str(etatDuJeu["compteurEtoiles"].compteur - 1))
        else:
            #On stocke le nombre d'étoiles
            fd.write(str(etatDuJeu["compteurEtoiles"].compteur))
            

def chargerSauvegarde(etatDuJeu, n):
    """Procédure qui charge le contenu de sauvegarde_n.txt"""
    etatDuJeu["tickAnimation"] = 0
    etatDuJeu["tickAnimationBob"] = 0
    with open(cheminAbsolu("sauvegardes", f"sauvegarde_{n}.txt"), "r") as fd:
        #On récupère le contenu du fichier
        sauvegarde = fd.read().split()
        
        #Si le format est invalide
        if len(sauvegarde) != 2:
            reporterErreur([sauvegarde])
        
        [nNiveauACharger, nEtoiles] = int(sauvegarde[0]), int(sauvegarde[1])
        
        etatDuJeu["bobAParle"] = (etatDuJeu["nNiveau"] == nNiveauACharger)
        etatDuJeu["compteurEtoiles"].setCompteur(nEtoiles)
        chargerNiveau(etatDuJeu, nNiveauACharger)
        