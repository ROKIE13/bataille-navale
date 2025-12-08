class Grille:
    def __init__ (self):
        self.largeur=10
        self.longueur=10
        self.tab=[[None for j in range(10)] for i in range(10)]
        if self.longueur*self.largeur<=0 :
            return print("Le tableau doit être positif")
        

