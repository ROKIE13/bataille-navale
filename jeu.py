import random

class Joueur:
    def __init__(self, id):
        self.id = id
        self.issue = False
        self.score = 0
        self.grillePerso = Grille()
        self.grilleAdv = Grille()
        for i in range(6):
            bateau = Bateau(random.randint(0, 9), random.randint(0, 9), random('H', 'V'), random.randint(1, 5))
            for j in range(0, len(bateau.pos()), 2):
                self.grillePerso[bateau.pos[j]][bateau.pos[j+1]] = "R"

            
                

    def tour_de_jeu(self, other):
        x = int(input("Choisir une colonne horizontale entre 1 et 10")) - 1
        y = int(input("Choisir une colonne verticale entre 1 et 10")) - 1
        self.grilleAdv[x][y] = "X"
        for i in range(6):
            other.bateaux[i].est_touche(x, y)
        coulement = []
        self.score = 0
        for i in range[6]:
            coulement.append(other.bateaux[i].est_coule)
            if coulement[i]:
                self.score += 1
        if self.score == 6:
            return True
        return False

joueur1 = Joueur(input("Quel est ton nom ?"))
joueur2 = Joueur(input("Quel est ton nom ?"))
while not joueur1.issue and not joueur2.issue:
    joueur1.tour_de_jeu(joueur2)
    if not joueur1.issue:
        joueur2.tour_de_jeu(joueur1)
