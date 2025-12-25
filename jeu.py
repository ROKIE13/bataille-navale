import random

# =======================
# GRILLE
# =======================
class Grille:
    def __init__(self):
        self.largeur = 10
        self.longueur = 10
        self.tab = [[None for _ in range(10)] for _ in range(10)]

    def afficher(self):
        for ligne in self.tab:
            print(" ".join(str(c) if c else "." for c in ligne))
        print()


# =======================
# BATEAU
# =======================
class Bateau:
    def __init__(self, x, y, orientation, taille):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.taille = taille
        self.taille_grille = 10
        self.positions = self.position()
        self.touches = set()

    def position(self):
        pos = []
        for i in range(self.taille):
            if self.orientation == "H":
                x = self.x
                y = self.y + i
            else:
                x = self.x + i
                y = self.y

            if x < 0 or y < 0 or x >= self.taille_grille or y >= self.taille_grille:
                return None

            pos.append((x, y))
        return pos

    def est_touche(self, x, y):
        if (x, y) in self.positions:
            self.touches.add((x, y))
            return True
        return False

    def est_coule(self):
        return len(self.touches) == self.taille


# =======================
# JOUEUR
# =======================
class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.issue = False
        self.grillePerso = Grille()
        self.grilleAdv = Grille()
        self.bateaux = []

        self.tailles_disponibles = [5, 4, 3, 3, 2]

        while self.tailles_disponibles:
            taille = self.tailles_disponibles.pop(
                random.randint(0, len(self.tailles_disponibles) - 1)
            )

            bateau = Bateau(
                random.randint(0, 9),
                random.randint(0, 9),
                random.choice(["H", "V"]),
                taille
            )

            # placement invalide → on remet la taille
            if bateau.positions is None:
                self.tailles_disponibles.append(taille)
                continue

            # vérifie le chevauchement
            if any(self.grillePerso.tab[x][y] == "R" for x, y in bateau.positions):
                self.tailles_disponibles.append(taille)
                continue

            # placement valide
            self.bateaux.append(bateau)
            for x, y in bateau.positions:
                self.grillePerso.tab[x][y] = "R"

    def tour_de_jeu(self, other):
        print(f"\nTour de {self.nom}")
        x = int(input("Colonne (1-10) : ")) - 1
        y = int(input("Ligne (1-10) : ")) - 1

        self.grilleAdv.tab[x][y] = "X"

        for bateau in other.bateaux:
            bateau.est_touche(x, y)

        if all(bateau.est_coule() for bateau in other.bateaux):
            self.issue = True
            print(f"\n🎉 {self.nom} a gagné !")

        return self.issue


# =======================
# JEU
# =======================
joueur1 = Joueur(input("Nom du joueur 1 : "))
joueur2 = Joueur(input("Nom du joueur 2 : "))

while not joueur1.issue and not joueur2.issue:
    joueur1.tour_de_jeu(joueur2)
    if not joueur1.issue:
        joueur2.tour_de_jeu(joueur1)
