
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
        self.orientation = orientation
        self.taille = taille
        self.positions = self.calcul_positions(x, y)
        self.touches = set()
    

    def calcul_positions(self, x, y):
        pos = []
        for i in range(self.taille):
            if self.orientation == "H":
                pos.append((x, y + i))
            else:
                pos.append((x + i, y))
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

    def placement_bateau(self, x, y, orientation, taille):
        bateau = Bateau(x, y, orientation, taille)

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
window.geometry("1050x520")

frame_j1 = Frame(window)
frame_j2 = Frame(window)

frame_j1.grid(row=0, column=0, sticky="nsew")
frame_j2.grid(row=0, column=0, sticky="nsew")

def afficher_frame(frame):
    frame.tkraise()



def creer_canvas(frame):
    c1 = Canvas(frame, width=500, height=500, bg="white")
    c2 = Canvas(frame, width=500, height=500, bg="white")
    c1.grid(row=0, column=0)
    c2.grid(row=0, column=1)
    return c1, c2

canvas_perso_1, canvas_attaque_1 = creer_canvas(frame_j1)
canvas_perso_2, canvas_attaque_2 = creer_canvas(frame_j2)



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

for c in [canvas_perso_1, canvas_attaque_1, canvas_perso_2, canvas_attaque_2]:
    dessiner_grille(c)



joueur1 = Joueur("Joueur 1")
joueur2 = Joueur("Joueur 2")

joueur_actif = joueur1
joueur_cible = joueur2
phase = "placement"

def clic_placement(joueur, canvas, event):
    global phase

    if not joueur.tailles_disponibles:
        return

    taille = joueur.tailles_disponibles.pop(0)
    if taille == 5:
        messagebox.showinfo("Placement", "placez votre Porte-avions")
    elif taille == 4:
        messagebox.showinfo("Placement", "placez votre Croiseur")
    elif taille == 3:
        messagebox.showinfo("Placement", "placez votre Contre-torpilleur")
    elif taille == 2:
        messagebox.showinfo("Placement", "placez votre Torpilleur")

    x = (event.y - MARGE) // TAILLE_CASE
    y = (event.x - MARGE) // TAILLE_CASE

    if 0 <= x < NB_CASES and 0 <= y < NB_CASES:
        reponse = messagebox.askquestion("Choix d'orientation", "voulez vous le placer de façon horizontale ?")
        if reponse == 'yes':
            orientation = "H"
        else:
            orientation = "V"
        if joueur.placement_bateau(x, y, orientation, taille):
            for i, j in joueur.bateaux[-1].positions:
                cx = MARGE + j * TAILLE_CASE + 20
                cy = MARGE + i * TAILLE_CASE + 20
                canvas.create_rectangle(cx-15, cy-15, cx+15, cy+15, fill="gray")
        else:
            joueur.tailles_disponibles.insert(0, taille)
            messagebox.showinfo("Attention", "Vous ne pouvez pas le placer ici pour cause de débordement")

    if not joueur.tailles_disponibles:
        if joueur == joueur1:
            messagebox.showinfo("Placement", "Au tour du Joueur 2")
            afficher_frame(frame_j2)
        else:
            messagebox.showinfo("Début", "Début de la phase d'attaque")
            afficher_frame(frame_j1)
            global phase
            phase = "attaque"

def clic_attaque(event):
    global joueur_actif, joueur_cible
    canvas_perso_1.itemconfigure("all", state="hidden")
    bt_blue = Button(window, text="Blue", command=lambda: can.config(bg="blue"))
    bt_blue_w = canvas_attaque_1.create_window(40, 20, window=bt_blue)
    bt_red = Button(window, text="Blue", command=lambda: can.config(bg="red"))
    bt_red_w = canvas_attaque_2.create_window(40, 20, window=bt_red)
    if phase != "attaque":
        return

    canvas = canvas_attaque_1 if joueur_actif == joueur1 else canvas_attaque_2

    x = (event.y - MARGE) // TAILLE_CASE
    y = (event.x - MARGE) // TAILLE_CASE

    if 0 <= x < NB_CASES and 0 <= y < NB_CASES:
        resultat = joueur_actif.tour_de_jeu(joueur_cible, x, y)

        cx = MARGE + y * TAILLE_CASE + 20
        cy = MARGE + x * TAILLE_CASE + 20

        if resultat == "eau":
            canvas.create_text(cx, cy, text="X", fill="blue")
        elif resultat == "touche":
            canvas.create_text(cx, cy, text="X", fill="red")
            messagebox.showinfo("Touché", f"{joueur_actif.nom} a touché un bateau cible de" f"{joueur_cible.nom}")
        elif resultat == "coule":
            for bateau in joueur_cible.bateaux:
                if bateau.est_coule():
                    for i, j in bateau.positions:
                        cx = MARGE + j * TAILLE_CASE + 20
                        cy = MARGE + i * TAILLE_CASE + 20
                        canvas.create_text(cx, cy, text="X", fill="black")
            messagebox.showinfo("Coulé", f"{joueur_actif.nom} a coulé un bateau cible de " f" {joueur_cible.nom}")
        elif resultat == "victoire":
            messagebox.showinfo("Fin", f"{joueur_actif.nom} a gagné !")
            window.destroy()
            return

        joueur_actif, joueur_cible = joueur_cible, joueur_actif
        afficher_frame(frame_j1 if joueur_actif == joueur1 else frame_j2)



canvas_perso_1.bind("<Button-1>", lambda e: clic_placement(joueur1, canvas_perso_1, e))
canvas_perso_2.bind("<Button-1>", lambda e: clic_placement(joueur2, canvas_perso_2, e))

canvas_attaque_1.bind("<Button-1>", clic_attaque)
canvas_attaque_2.bind("<Button-1>", clic_attaque)

afficher_frame(frame_j1)
window.mainloop()
