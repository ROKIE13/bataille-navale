class Joueur:
    def __init__(self, couleur):
        self.couleur = couleur
        self.score = 0
        self.grillePerso = Grille()
        self.grilleAdv = Grille()
    def remplissage(self):
        bateauxPerso = []
        for i in range(6):
            #ligne ou l on place dans l'interface les coordonnées x et y du bateau/case
            bateau = Bateau()
            bateauxPerso.append(bateau)

    def tour_de_jeu(self):
        

    matrice = [[None for _ in range(3)] for _ in range(4)]
        