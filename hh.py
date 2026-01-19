fenetre_attaque = Toplevel(window)
canvas_attaque_1 = Canvas(fenetre_attaque)
canvas_attaque_1.grid(...)
frame_boutons = Frame(fenetre_attaque)
frame_boutons.grid(row=3, column=0, columnspan=2, pady=10)
Button(
    frame_boutons,
    text="Grille J1",
    command=lambda: (
        canvas_attaque_1.itemconfigure("grille", state="normal"),
        fenetre_attaque.after(
            2000,
            lambda: canvas_attaque_1.itemconfigure("grille", state="hidden")
        )
    )
).grid(row=0, column=0, padx=5)
Button(
    frame_boutons,
    text="Grille J1",
    command=lambda: (
        canvas_attaque_1.itemconfigure("grille", state="normal"),
        fenetre_attaque.after(
            2000,
            lambda: canvas_attaque_1.itemconfigure("grille", state="hidden")
        )
    )
).grid(row=0, column=0, padx=5)
window = Tk()
window2 = Toplevel(window)
