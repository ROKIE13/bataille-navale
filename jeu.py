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
    def __init__(self, nom, simulation=False):
        self.simulation=simulation
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

nb_joueurs=messagebox.askquestion("Choix des Joueurs", "Voulez vous jouer à 2 ?")
if nb_joueurs=='yes':
    joueur2 = Joueur("Joueur 2")
else:
    joueur2 = Joueur("Joueur 2", True)

joueur_actif = joueur1
joueur_cible = joueur2
phase = "placement"
choix_placement = messagebox.askquestion("Mode placement", "Voulez-vous le placement automatique ?")
if choix_placement == 'yes':
    test = "auto"
else:
    test = "manu"

def demander_noms_joueurs():
    fen = Toplevel(window)
    fen.title("Noms des joueurs")
    fen.geometry("300x200")
    fen.transient(window)
    fen.grab_set()

    nom1 = StringVar()
    nom2 = StringVar()

    def valider():
        global joueur1, joueur2, joueur_actif, joueur_cible, phase
        if nom1.get().strip() == "":
            messagebox.showwarning("Erreur", "Veuillez entrer le nom du joueur 1")
            return

        if not joueur2.simulation and nom2.get().strip() == "":
            messagebox.showwarning("Erreur", "Veuillez entrer le nom du joueur 2")
            return

        joueur1 = Joueur(nom1.get())
        if not joueur2.simulation:
            joueur2 = Joueur(nom2.get())
        else:
            joueur2.nom = "Ordinateur"

        joueur_actif = joueur1
        joueur_cible = joueur2
        phase = "placement"

        fen.destroy()
        afficher_frame(frame_j1)
        messagebox.showinfo("Placement", f"{joueur1.nom}, placez vos bateaux")

    Label(fen, text="Nom du joueur 1").pack(pady=5)
    Entry(fen, textvariable=nom1).pack()

    if not joueur2.simulation:
        Label(fen, text="Nom du joueur 2").pack(pady=5)
        Entry(fen, textvariable=nom2).pack()
    
    Button(fen, text="Lancer la partie", command=valider).pack(pady=15)


def placement_automatique(test, joueur, canvas, e):
    global phase

    if test == "auto":
        placements = [
            (2, 3, 'H', 5),
            (1, 0, 'V', 4),
            (5, 5, 'H', 3),
            (7, 1, 'V', 3),
            (4, 2, 'H', 2)
        ]

        for x, y, orientation, taille in placements:
            ok = joueur.placement_bateau(x, y, orientation, taille)
            if ok:
                bateau = joueur.bateaux[-1]
                for i, j in bateau.positions:
                    cx = MARGE + j * TAILLE_CASE + 20
                    cy = MARGE + i * TAILLE_CASE + 20
                    canvas.create_rectangle(
                        cx-15, cy-15, cx+15, cy+15, fill="gray"
                    )

        if joueur == joueur1:
            afficher_frame(frame_j2)
        else:
            phase = "attaque"
            afficher_frame(frame_j1)
    else : 
        clic_placement(joueur, canvas, e)

def clic_placement(joueur, canvas, event):
    global phase

    if joueur.simulation:
        while joueur.tailles_disponibles:
            taille = joueur.tailles_disponibles[0]
            # On essaye de placer ce bateau tant qu'on n'y arrive pas
            place_ok = False
            while not place_ok:
                x = random.randint(0, NB_CASES - 1)
                y = random.randint(0, NB_CASES - 1)
                orientation = random.choice(["H", "V"])
                
                if joueur.placement_bateau(x, y, orientation, taille):
                    place_ok = True
                    joueur.tailles_disponibles.pop(0)

        # Une fois tous les bateaux placés, on dessine tout d'un coup (pour le debug/visu)
        # Mais comme c'est l'ordi, on peut choisir de ne pas les montrer ou les montrer en gris
        for bateau in joueur.bateaux:
            for i, j in bateau.positions:
                cx = MARGE + j * TAILLE_CASE + 20
                cy = MARGE + i * TAILLE_CASE + 20
                canvas.create_rectangle(cx-15, cy-15, cx+15, cy+15, fill="gray")

    else:
        # Logique joueur humain
        if not joueur.tailles_disponibles:
            return

        x = (event.y - MARGE) // TAILLE_CASE
        y = (event.x - MARGE) // TAILLE_CASE

        # Vérification si le clic est bien dans la grille
        if not (0 <= x < NB_CASES and 0 <= y < NB_CASES):
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
            # Si le joueur 2 est une simulation, on lance son placement auto tout de suite
            if joueur2.simulation:
                clic_placement(joueur2, canvas_perso_2, None)
        else:
            messagebox.showinfo("Début", "Début de la phase d'attaque")
            afficher_frame(frame_j1)
            global phase
            phase = "attaque"

frame_boutons = Frame(frame_j1)
frame_boutons.grid(row=10, column=0, columnspan=4, pady=10)

def affichage_couleur(joueur, canvas):
    canvas.config(bg="lightblue")
    # On efface uniquement les anciens rectangles de bateaux
    canvas.delete("bateau")

    for bateau in joueur.bateaux:
        for (x, y) in bateau.positions:
            cx = MARGE + y * TAILLE_CASE + TAILLE_CASE // 2
            cy = MARGE + x * TAILLE_CASE + TAILLE_CASE // 2

            # Couleur selon l'état
            if (x, y) in bateau.touches:
                if bateau.est_coule():
                    couleur = "black"   # bateau coulé
                else:
                    couleur = "red"   # bateau touché
            else:
                couleur = "pink"    # bateau intact

            canvas.create_rectangle(
                cx - 15, cy - 15,
                cx + 15, cy + 15,
                fill=couleur,
                tags="bateau"
            )


def clic_attaque(event):
    global joueur_actif, joueur_cible
    if phase != "attaque":
        return

    # Masquer les canvas persos
    if joueur_actif == joueur1:
        affichage_couleur (joueur_actif, canvas_perso_1)
    else:
        affichage_couleur (joueur_actif, canvas_perso_2)
    

    # Bouton grille pour canvas_attaque_1

    canvas_perso = canvas_perso_1 if joueur_actif == joueur1 else canvas_perso_2
    canvas = canvas_attaque_1 if joueur_actif == joueur1 else canvas_attaque_2
    canva_adv = canvas_attaque_2 if joueur_actif == joueur1 else canvas_attaque_1
    canvas_perso_adv = canvas_perso_2 if joueur_actif == joueur1 else canvas_perso_1
    if joueur_actif.simulation:
        while True:
            x = random.randint(0, NB_CASES - 1)
            y = random.randint(0, NB_CASES - 1)
            if joueur_actif.grilleAdv.tab[x][y] is None:
                break
    else:
        x = (event.y - MARGE) // TAILLE_CASE
        y = (event.x - MARGE) // TAILLE_CASE

    if 0 <= x < NB_CASES and 0 <= y < NB_CASES:
        resultat = joueur_actif.tour_de_jeu(joueur_cible, x, y)
        
        if resultat == "deja":
             messagebox.showinfo("Attention", "Vous avez déjà tiré ici !")
             return

        cx = MARGE + y * TAILLE_CASE + 20
        cy = MARGE + x * TAILLE_CASE + 20

        if resultat == "eau":
            canvas.create_text(cx, cy, text="X", fill="blue")
            canvas_perso.itemconfigure("all", state="hidden")
            canvas.itemconfigure("all", state="hidden")
        elif resultat == "touche":
            canvas.create_text(cx, cy, text="X", fill="red")
            canvas_perso.itemconfigure("all", state="hidden")
            canvas.itemconfigure("all", state="hidden")
            messagebox.showinfo("Touché", f"{joueur_actif.nom} a touché un bateau cible de " f"{joueur_cible.nom}")
        elif resultat == "coule":
            for bateau in joueur_cible.bateaux:
                if bateau.est_coule():
                    for i, j in bateau.positions:
                        cx = MARGE + j * TAILLE_CASE + 20
                        cy = MARGE + i * TAILLE_CASE + 20
                        canvas.create_text(cx, cy, text="X", fill="black")
            canvas.itemconfigure("all", state="hidden")
            canvas_perso.itemconfigure("all", state="hidden")
            messagebox.showinfo("Coulé", f"{joueur_actif.nom} a coulé un bateau cible de " f" {joueur_cible.nom}")
        elif resultat == "victoire":
            messagebox.showinfo("Fin", f"{joueur_actif.nom} a gagné !")
            window.destroy()
            return
        
        joueur_actif, joueur_cible = joueur_cible, joueur_actif
        
        # Mettre à jour l'affichage des bateaux du nouveau joueur actif (celui qui vient de subir l'attaque)
        if joueur_actif == joueur1:
            affichage_couleur(joueur_actif, canvas_perso_1)
        else:
            affichage_couleur(joueur_actif, canvas_perso_2)

        canva_adv.itemconfigure("all", state="normal")
        canvas_perso_adv.itemconfigure("all", state="normal")
        messagebox.showinfo("Tour", "Au tour de " f"{joueur_cible.nom}")
        afficher_frame(frame_j1 if joueur_actif == joueur1 else frame_j2)
        # Si c'est au tour de l'ordi, on déclenche son attaque automatiquement après 1s
        if joueur_actif.simulation:
            window.after(1000, lambda: clic_attaque(None))



canvas_perso_1.bind("<Button-1>", lambda e: placement_automatique(test, joueur1, canvas_perso_1, e))
canvas_perso_2.bind("<Button-1>", lambda e: placement_automatique(test, joueur2, canvas_perso_2, e))

canvas_attaque_1.bind("<Button-1>", clic_attaque)
canvas_attaque_2.bind("<Button-1>", clic_attaque)

afficher_frame(frame_j1)
window.after(100, demander_noms_joueurs)
window.mainloop()
