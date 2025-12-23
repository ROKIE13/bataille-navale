from tkinter import *

TAILLE_CASE = 40
NB_CASES = 10
MARGE = 40

class Grille:
    def __init__(self):
        self.tab = [[None for _ in range(10)] for _ in range(10)]

    def tirer(self, ligne, colonne):
        if self.tab[ligne][colonne] is None:
            self.tab[ligne][colonne] = "O"
            return "eau"
        return "deja"

def clic(event):
    x = event.x - MARGE
    y = event.y - MARGE

    if 0 <= x < NB_CASES * TAILLE_CASE and 0 <= y < NB_CASES * TAILLE_CASE:
        colonne = x // TAILLE_CASE
        ligne = y // TAILLE_CASE

        resultat = grille.tirer(ligne, colonne)

        cx = MARGE + colonne * TAILLE_CASE + TAILLE_CASE // 2
        cy = MARGE + ligne * TAILLE_CASE + TAILLE_CASE // 2

        if resultat == "eau":
            canvas.create_text(cx, cy, text="O", fill="blue", font=("Arial", 18, "bold"))

grille = Grille()

window = Tk()
window.title("Bataille navale")

canvas = Canvas(window, width=500, height=500, bg="white")
canvas.pack()

# Grille graphique
for i in range(NB_CASES + 1):
    canvas.create_line(MARGE,
                        MARGE + i * TAILLE_CASE,
                       MARGE + NB_CASES * TAILLE_CASE,
                       MARGE + i * TAILLE_CASE)

    canvas.create_line(MARGE + i * TAILLE_CASE,
                        MARGE,
                       MARGE + i * TAILLE_CASE,
                       MARGE + NB_CASES * TAILLE_CASE)

canvas.bind("<Button-1>", clic)

window.mainloop()
