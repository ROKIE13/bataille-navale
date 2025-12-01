from tkinter import *

def coordonnees(event):
    xe = event.x
    ye = event.y
    print("On clique en x = {} et y = {}".format(xe,ye))

window = Tk()
window.title("My Application")
window.geometry("1080x720")
window.minsize(480, 360)
window.config(background='#5CACF2')

label_title = Label(window, text="Bataille navale")
label_title.pack()

boutton = Button(text = "Confirmer")
boutton.pack()

image = PhotoImage(file="grille.png").room(35).subsample(32)
canvas  = Canvas(window, width = 720, height = 180)
canvas.pack()

window.bind('<Button-1>',coordonnees)

window.mainloop()