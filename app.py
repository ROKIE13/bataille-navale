import random
from tkinter import *
from tkinter import messagebox

TAILLE_CASE = 40
NB_CASES = 10
MARGE = 40

class Grille:
    def __init__(self):
        self.tab = [[None for _ in range(NB_CASES)] for _ in range(NB_CASES)]

class Bateau:
    def __init__(self, x, y, orientation, taille):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.taille = taille
        self.positions = self.calcul_positions()
        self.touches = set()

    def calcul_positions(self):
        pos = []
        for i in range(self.taille):
            if self.orientation == "H":
                pos.append((self.x, self.y + i))
            else:
                pos.append((self.x + i, self.y))
        return pos

    def est_touche(self, x, y):
        if (x, y) in self.positions:
            self.touches.add((x, y))
            return True
        return False

    def est_coule(self):
        return len(self.touches) == self.taille


class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.grillePerso = Grille()
        self.grilleAdv = Grille()
        self.bateaux = []
        self.tailles_disponibles = [5, 4, 3, 3, 2]

    def placement_bateau(self, x, y, taille):
        orientation = random.choice(["H", "V"])
        bateau = Bateau(x, y, orientation, taille)

        # Vérification limites
        for i, j in bateau.positions:
            if i < 0 or j < 0 or i >= NB_CASES or j >= NB_CASES:
                return False
            if self.grillePerso.tab[i][j] == "R":
                return False

        self.bateaux.append(bateau)
        for i, j in bateau.positions:
            self.grillePerso.tab[i][j] = "R"
        return True

    def tour_de_jeu(self, other, x, y):
        if self.grilleAdv.tab[x][y] is not None:
            return "deja"

        self.grilleAdv.tab[x][y] = "X"

        for bateau in other.bateaux:
            if bateau.est_touche(x, y):
                if bateau.est_coule():
                    if all(b.est_coule() for b in other.bateaux):
                        return "victoire"
                    return "coule"
                return "touche"
        return "eau"


window = Tk()
window.title("Bataille Navale")

canvas_perso = Canvas(window, width=500, height=500, bg="white")
canvas_perso.grid(row=0, column=0)

canvas_attaque = Canvas(window, width=500, height=500, bg="white")
canvas_attaque.grid(row=0, column=1)

def dessiner_grille(canvas):
    for i in range(NB_CASES + 1):
        canvas.create_line(
            MARGE, MARGE + i * TAILLE_CASE,
            MARGE + NB_CASES * TAILLE_CASE, MARGE + i * TAILLE_CASE
        )
        canvas.create_line(
            MARGE + i * TAILLE_CASE, MARGE,
            MARGE + i * TAILLE_CASE, MARGE + NB_CASES * TAILLE_CASE
        )

dessiner_grille(canvas_perso)
dessiner_grille(canvas_attaque)

joueur1 = Joueur("Joueur 1")
joueur2 = Joueur("Joueur 2")

joueur_actif = joueur1
joueur_cible = joueur2
phase = "placement"


def clic_placement(event):
    global phase

    if not joueur_actif.tailles_disponibles:
        phase = "attaque"
        return

    x = (event.y - MARGE) // TAILLE_CASE
    y = (event.x - MARGE) // TAILLE_CASE

    if 0 <= x < NB_CASES and 0 <= y < NB_CASES:
        taille = joueur_actif.tailles_disponibles.pop(0)
        if joueur_actif.placement_bateau(x, y, taille):
            for bateau in joueur_actif.bateaux:
                for i, j in bateau.positions:
                    cx = MARGE + j * TAILLE_CASE + 20
                    cy = MARGE + i * TAILLE_CASE + 20
                    canvas_perso.create_rectangle(
                        cx - 15, cy - 15, cx + 15, cy + 15, fill="gray"
                    )
        else:
            joueur_actif.tailles_disponibles.insert(0, taille)


def clic_attaque(event):
    global joueur_actif, joueur_cible

    if phase != "attaque":
        return

    x = (event.y - MARGE) // TAILLE_CASE
    y = (event.x - MARGE) // TAILLE_CASE

    if 0 <= x < NB_CASES and 0 <= y < NB_CASES:
        resultat = joueur_actif.tour_de_jeu(joueur_cible, x, y)

        cx = MARGE + y * TAILLE_CASE + 20
        cy = MARGE + x * TAILLE_CASE + 20

        if resultat == "eau":
            canvas_attaque.create_text(cx, cy, text="X", fill="blue")

        elif resultat == "touche":
            canvas_attaque.create_text(cx, cy, text="X", fill="red")

        elif resultat == "coule":
            # on affiche TOUT le bateau en rouge foncé
            for bateau in joueur_cible.bateaux:
                if bateau.est_coule():
                    for i, j in bateau.positions:
                        cx = MARGE + j * TAILLE_CASE + 20
                        cy = MARGE + i * TAILLE_CASE + 20
                        canvas_attaque.create_text(cx, cy, text="X", fill="black")

        elif resultat == "victoire":
            messagebox.showinfo("Fin", f"{joueur_actif.nom} a gagné !")
            return

        joueur_actif, joueur_cible = joueur_cible, joueur_actif

canvas_perso.bind("<Button-1>", clic_placement)
canvas_attaque.bind("<Button-1>", clic_attaque)

window.mainloop()
