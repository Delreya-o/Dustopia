from Dialogue import *
from Entite import *
from TableauNiveaux import *
from Generation import *

from divers import *

class Niveau:
    def __init__(self, nom, T, susuwatariASauver, etoile, Bob, dialogues, backgrounds):
        """T est un tableau en deux dimensions
        Pour des exemples, voir les fonctions
        chargerNiveau ci-dessous"""
        self.nom = nom
        self.T = T                                    #Tableau de tableaux de chiffres représentant les blocs
        self.width = 0 if T==[] else len(T[0])
        self.height = len(T)
        self.susuwatariASauver = susuwatariASauver    #Entite
        self.etoile = etoile                          #Entite
        self.Bob = Bob                                #Bob est une entité
        self.dialogues = dialogues                    #Tableau de Dialogues
        self.backgrounds = backgrounds                #Tableaux de noms d'images
    
    def __str__(self):
        return f"Niveau('{self.nom}', {self.T})"
        
    def getBloc(self, x, y):
        return self.T[int(y)][int(x)]
        
    def getBlocParVecteur(self, vecteur):
        return self.getBloc(vecteur.x, vecteur.y)
    
    def gererLesDialogues(self, etatDuJeu):
        posXJoueur = etatDuJeu["listeEntites"][0].box.pos.x

        if etatDuJeu["tickAnimationBob"] == 0 :
            for dialogue in self.dialogues:
                if dialogue.xDebut <= posXJoueur <= dialogue.xFin:
                    dialogue.parler(etatDuJeu)
    
    def dessinerLesBackgrounds(self, etatDuJeu):
        for i, nomImage in enumerate(self.backgrounds): #Pour chaque élément et son indice (c'est la syntaxe officielle que je recommande de se souvenir)
            etatDuJeu["dicoBackground"][nomImage].drawAsBackground(etatDuJeu, i)


def dechargerNiveau(etatDuJeu):
    etatDuJeu["listeEntites"] = [etatDuJeu["listeEntites"][0]]
    etatDuJeu["generateurs"] = []
    
    #On arrête la musique actuelle
    if etatDuJeu["musique"] is not None:
        etatDuJeu["musique"][0].stop()

def chargerNiveau(etatDuJeu, n):
    """Charge le niveau n dans etatDuJeu["niveau"]
    Fait des effets de bord sur la position et la
    vitesse du joueur, la liste des entités, la
    liste des générateurs, et etatDuJeu["nNiveau"]"""
    
    etatDuJeu["nNiveau"] = n
    
    dechargerNiveau(etatDuJeu)
    joueur = etatDuJeu["listeEntites"][0]
    etatDuJeu["barreVie"].vie = 3
    
    susuwatariASauver = creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari à sauver", None, None)
    etoile = creerEntiteCorrespondantAImage(etatDuJeu, "etoile0.png", "Etoile", None, None)
    etoile.autresParametres = {"ticksTouchee" : 0}
    if n not in [10, 11] and not etatDuJeu["bobAParle"]:
        Bob = creerEntiteCorrespondantAImage(etatDuJeu, "Bob.png", "Bob", 10, -10)
    else:
        Bob = None
    
    dialogues = []
    dialoguesBob = []
    
    #Utile quand le joueur recharge un niveau "normal" lorsqu'il est dans un niveau avec une gravité différente
    mettreMouvementsParDefaut(etatDuJeu)
    
    if n == 0:
        joueur.box.pos = Vecteur(3, 3)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(100, 7)
        etoile.box.pos = Vecteur(58, 1)
        dialogues = [Dialogue("Appuyez sur les flèches de gauche et de droite pour vous déplacer", "Kanit-Regular.ttf", 0, 8),
                    Dialogue("Appuyez sur la flèche du haut pour sauter", "Kanit-Regular.ttf", 10, 20),
        ]
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_basique.wav"))
        dialoguesBob = [
            Dialogue("Bienvenue sur Terre, petit susuwatari !"),
            Dialogue("Justement, tu tombes bien..."),
            Dialogue("Nous, les humains, manquons de Dust."),
            Dialogue("Heureusement, tes amis et toi faites partie de la solution."),
            Dialogue("Il suffit juste que vous nous laissiez vous exterminer.")
        ]
        backgrounds = ["anight.png"]
        T = TD
    
    elif n == 1:
        joueur.box.pos = Vecteur(3, 1)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(145, 3)
        etoile.box.pos = Vecteur (1, 13)
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_basique.wav"))
        dialoguesBob = [
            Dialogue("Donc du coup, tu comptes sauver tes amis ?"),
            Dialogue("Ne sois pas ridicule..."),
        ]
        backgrounds = ["bNS.png"]
        T = TB
    
    elif n == 2:
        joueur.box.pos = Vecteur(3, 10)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(144, 7)
        etoile.box.pos = Vecteur(27, 2)
        dialogues = [Dialogue("Appuyer sur la touche S pour sauvegarder et L pour charger la dernière sauvegarde","Kanit-Regular.ttf", 0, 13)]
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_basique.wav"))
        dialoguesBob = [
            Dialogue("Ne vois tu pas les avantages..."),
            Dialogue("Qu'apporte votre extinction pour ma civilisation ?"),
            Dialogue("Nous avons besoin de votre Dust."),
            Dialogue("Sinon, comment pourrais-je alimenter mon entreprise ?")
        ]
        backgrounds = ["cSR.png"]
        T = TA
    
    elif n == 3:
        joueur.box.pos = Vecteur(3, 3)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(146,2)
        etoile.box.pos = Vecteur(106, 1)
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_basique.wav"))
        dialoguesBob = [
            Dialogue("Tu me cours vraiment sur le haricot."),
            Dialogue("Ne peux-tu pas mourir comme les autres susuwataris ?")
        ]
        backgrounds = ["dSD.png"]
        T = TF
    
    elif n == 4:
        joueur.box.pos = Vecteur(3, 10)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(140, 3)
        etoile.box.pos = Vecteur(7, 4)
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_basique.wav"))
        dialoguesBob = [
            Dialogue("Bonne chance pour celui-ci !"),
            Dialogue("Tu ne vas faire que mourir."),
            Dialogue("Encore... et encore... et encore..."),
            Dialogue("Tout cela pour quoi ?"),
            Dialogue("Pour de vulgaires animaux en cage ?"),
        ]
        backgrounds = ["jour.png"]
        T = TC
    
    elif n == 5:
        joueur.box.pos = Vecteur(3, 10)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(150, 3)
        etoile.box.pos = Vecteur(100, 1)
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_basique.wav"))
        dialoguesBob = [
            Dialogue("Je ne peux pas t'en vouloir..."),
            Dialogue("Tu ne peux pas comprendre..."),
            Dialogue("Ton cerveau n'est pas assez puissant."),
            Dialogue("Tu n'es... qu'un susuwatari."),
        ]
        backgrounds = ["middle-of-day-and-sunset.png", "suunset.png"]
        T = TE
    
    elif n == 6:
        etatDuJeu["forceSaut"] = 0.4#On diminue la force de saut
        joueur.box.pos = Vecteur(3, 14)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(125, 7)
        etoile.box.pos = Vecteur(94, 8)
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_bonus.wav"))
        dialogues = [Dialogue("Bloqué.e ? Il serait temps de penser en dehors de la boîte …","Kanit-Regular.ttf", 100, 110)]
        dialoguesBob = [
            Dialogue("Est-ce que... tu me voles mes etoiles ?"),
            Dialogue("Pour la peine, voici ta punition."),
            Dialogue("Tu vas faire un petit tour dans le desert."),
            Dialogue("Estime cela comme un niveau bonus.")
        ]
        backgrounds = ["background_desert.png"]
        T = TG
    
    elif n == 7:
        etatDuJeu["forceSaut"] = 0.45#On remet la force de saut comme avant
        joueur.box.pos = Vecteur(3, 16)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(145, 7)
        etoile.box.pos = Vecteur(33, 1)
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_bonus.wav"))
        dialoguesBob = [
            Dialogue("Et tu continues de me voler des etoiles ?"),
            Dialogue("Dans ce cas, encore un niveau bonus !"),
        ]
        backgrounds = ["background_neige.png"]
        T = TH
    
    elif n == 8:
        joueur.box.pos = Vecteur(3, 15)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(145, 7)
        etoile.box.pos = Vecteur(100, 10)
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_evacuation.wav"))
        dialoguesBob = [
            Dialogue("Ah ah ! Tu pensais vraiment..."),
            Dialogue("OH MER*E ILS FONCENT VERS MOI !")
        ]
        backgrounds = ["suunset.png"]
        T = TI
    
    elif n == 9:
        etatDuJeu["forceSaut"] = 0.12#On est dans l'espace
        etatDuJeu["forceGravite"] = 0.001
        etatDuJeu["tauxConservationVitesse"] = 0.96
        etatDuJeu["accelerationX"] = 0.005
        
        joueur.box.pos = Vecteur(3, 15)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(140, 5)
        etoile.box.pos = Vecteur(95, 3)
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_evacuation_espace.wav"))
        dialoguesBob = [
            Dialogue("Attends, je tombe... Ne bouge pas entre temps !"),
            Dialogue("Ah ah ! Tu pensais vraiment pouvoir organiser une escapade ?"),
            Dialogue("... Tu avais probablement raison."),
            Dialogue("Mais tu vas ruiner mon industrie !"),
            Dialogue("Qu'est-ce que je vais faire moi maintenant ?"),
            Dialogue("Je n'ai plus pouvoir produire de pommades par ta faute !"),
            Dialogue("Oh, je sais ce que je vais faire..."),
            Dialogue("Je vais me reconvertir dans l'industrie agro-alimentaire"),
            Dialogue("Au revoir les susuwataris ! Bonjour les poulets !"),
            Dialogue("Allez, bye bye !")
        ]
        backgrounds = ["image_nebuleuse_1.png"]
        T = TJ
    
    elif n == 10:
        etatDuJeu["forceSaut"] = 0.12#On est dans l'espace
        etatDuJeu["forceGravite"] = 0.001
        etatDuJeu["tauxConservationVitesse"] = 0.96
        etatDuJeu["accelerationX"] = 0.005
        
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 18, 14)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 15, 7)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 30, 15)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 32, 15)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 38, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 54, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 62, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 72, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 73, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 74, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 90, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 92, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 94, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 100, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 102, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 105, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 107, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 115, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 116, 8)
        creerEntiteCorrespondantAImage(etatDuJeu, "zkakuDeFace.png", "Susuwatari villageois", 117, 8)
        
        
        joueur.box.pos = Vecteur(3, 15)
        joueur.box.vitesse = Vecteur(0, 0)
        susuwatariASauver.box.pos = Vecteur(145, 7)
        etoile.box.pos = Vecteur(106, 7)
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_espace.wav"))
        backgrounds = ["image_etoiles.jpg"]
        T = TK

    elif n==11 :
        etatDuJeu["forceSaut"] = 0.10 #On est dans l'espace
        etatDuJeu["forceGravite"] = 0.001
        etatDuJeu["tauxConservationVitesse"] = 0.96
        etatDuJeu["accelerationX"] = 0.005

        joueur.box.pos = Vecteur(3, 15)
        joueur.box.vitesse = Vecteur(0,0)
        susuwatariASauver.box.pos = Vecteur(155, 7)
        etoile.box.pos = Vecteur(150, 14)
        musique = pygame.mixer.Sound(cheminAbsolu("musiques", "musique_espace.wav"))
        dialogues = [
            Dialogue("Merci d'avoir participé à cette aventure avec Kaku !","Kanit-Regular.ttf", 3, 10),
            Dialogue("Ce projet a été réalisé dans le cadre d'un travail de groupe","Kanit-Regular.ttf", 13, 20),
            Dialogue("À la Faculté des sciences de Montpellier","Kanit-Regular.ttf", 21, 28),
            Dialogue("Avec la participation de :","Kanit-Regular.ttf", 31, 38),
            Dialogue("TERRISSE Lysandre","Kanit-Regular.ttf", 39, 44),
            Dialogue("ROGET Elora","Kanit-Regular.ttf", 45, 50),
            Dialogue("OMS Anouk","Kanit-Regular.ttf", 51, 56),
            Dialogue("Ce jeu a été codé en Python,","Kanit-Regular.ttf", 59, 66),
            Dialogue("En s'aidant de la bibliothèque Pygame","Kanit-Regular.ttf", 67, 74),
            Dialogue("Nous avons utilisé les sites internet et applications :","Kanit-Regular.ttf", 77, 84),
            Dialogue("PixilArt et GIMP pour les graphismes","Kanit-Regular.ttf", 85, 92),
            Dialogue("La documentation Pygame","Kanit-Regular.ttf", 93, 100),
            Dialogue("Signal pour éditer le format MIDI","Kanit-Regular.ttf", 101, 108),
            Dialogue("Stack Overflow lorsqu'on a eu des problèmes de code","Kanit-Regular.ttf",109, 116),
            Dialogue("Google Fonts, DaFont et wFonts pour les polices d'écriture","Kanit-Regular.ttf",117, 124),
            Dialogue("Le site de la NASA et de PublicDomainPictures","Kanit-Regular.ttf",127, 134),
            Dialogue("Pour les images de l'espace","Kanit-Regular.ttf",135, 142),
            Dialogue("Tous les contenus utilisés sont libres de droit","Kanit-Regular.ttf",145, 152)
        ]
        backgrounds = ["image_etoiles.jpg"]
        T = T0
    
    if n not in [10, 11] and not etatDuJeu["bobAParle"]:
        Bob.autresParametres = {"dialogues" : dialoguesBob}
    etatDuJeu["niveau"] = Niveau("Niveau " + str(n), T, susuwatariASauver, etoile, Bob, dialogues, backgrounds)
    

    #On répète indéfiniment la musique
    musique.play(-1)
    etatDuJeu["musique"] = (musique, "Ce n'est pas la musique de mort")
    
    initialiserGenerateurs(etatDuJeu)
    
    #On met à jour la taille des images (puisque la taille du niveau peut changer
    chargerLeForeground(etatDuJeu)
    chargerLeBackground(etatDuJeu)