"""
Une partie de l'animation (le fond noir) se fait dans dessine()
"""

def gererLesAnimations(etatDuJeu):
    """Détecte si une animation doit être active, et la fait.
    Chaque tick de l'animation incrémente etatDuJeu['tickAnimation'].
    À la fin de l'animation, cette variable est remise à 0.
    Pendant l'animation, la vitesse horizontale du joueur est nulle."""
    listeEntites = etatDuJeu["listeEntites"]
    niveau = etatDuJeu["niveau"]
    joueur = listeEntites[0]
    
    #Pour chaque entité
    for entite in listeEntites:
        #Si le joueur est assez proche de cette entité
        if abs(joueur.box.pos.x - entite.box.pos.x) < 3:
            
            if entite.nom == "Susuwatari à sauver":
                animationFinNiveau(etatDuJeu, entite)
            
    if etatDuJeu["nNiveau"] not in [10, 11] and not etatDuJeu["bobAParle"]:
        animationBob(etatDuJeu, niveau.Bob)
    
    #Si on est aux crédits et que l'on n'est pas à l'animation de fin de niveau
    if etatDuJeu["nNiveau"] == 11 and etatDuJeu["tickAnimation"] == 0:
        animationFinale(etatDuJeu)

def animationFinNiveau(etatDuJeu, susuwatariASauver):
    listeEntites = etatDuJeu["listeEntites"]
    joueur = listeEntites[0]
    
    
    #Si l'animation a commencé il y a moins de 300 ticks
    if etatDuJeu['tickAnimation']<300:
        #Le joueur ne peut plus bouger horizontalement
        joueur.box.vitesse.x = 0
        #Je joueur saute si possible
        joueur.sauteSiPossible(etatDuJeu)
        #Si l'animation a commencé depuis plus de 20 ticks
        #(cela permet d'asynchroniser les sauts entre les deux susuwataris).
        if etatDuJeu['tickAnimation']>20:
            #Il saute si possible
            susuwatariASauver.sauteSiPossible(etatDuJeu)
        
        #On passe au prochain tick
        etatDuJeu['tickAnimation']+=1

    elif etatDuJeu["nNiveau"] != 11: #Sinon, si ce n'est pas le dernier niveau
        #L'animation a terminé
        etatDuJeu['tickAnimation'] = 0
        etatDuJeu["niveauSuivant"] = True

def animationBob(etatDuJeu, Bob):
    """Voici Bob"""
    listeEntites = etatDuJeu["listeEntites"]
    joueur = listeEntites[0]
    
    #On calcule le temps que devrait prendre l'animation
    #tout en cherchant quel dialogue afficher
    tempsDebutDialogue = 0
    tempsEntreDialogues = 120
    for dialogue in Bob.autresParametres["dialogues"]:
        tempsQuePrendCeDialogue = len(dialogue.texte) + tempsEntreDialogues
        
        #Si le temps de l'animation est entre le début et la fin de ce dialogue
        if tempsDebutDialogue <= etatDuJeu["tickAnimationBob"] < tempsDebutDialogue + tempsQuePrendCeDialogue:
            #On l'affiche
            dialogue.parler(etatDuJeu)
        
        tempsDebutDialogue += tempsQuePrendCeDialogue
    
    etatDuJeu['tickAnimationBob']+=1
    
    #Si c'est la fin du dernier dialogue
    if etatDuJeu["tickAnimationBob"] == tempsDebutDialogue:
        #Bob remonte (il ne fait pas Bob.saute() car c'est le saut des susuwataris)
        Bob.box.vitesse.y = -1
    
    #Si c'est la fin de l'animation
    if etatDuJeu["tickAnimationBob"] == tempsDebutDialogue + 30:
        #On enlève Bob de la liste des entités car il fait trop de lag ce méchant pas beaus
        for i, entite in enumerate(listeEntites):
            if entite == Bob:
                listeEntites.pop(i)
        
        etatDuJeu["tickAnimationBob"] = 0
        etatDuJeu["bobAParle"] = True
    

def animationFinale(etatDuJeu):
    joueur = etatDuJeu["listeEntites"][0]
    joueur.box.vitesse.x = 0.05
    joueur.sauteSiPossible(etatDuJeu)